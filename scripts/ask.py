#!/usr/bin/env python3
"""
ask.py — Natural-language QA over the compliance ontology.

Pipeline:
    question + schema + entity catalog + few-shot CQs
        → Claude synthesises one SPARQL query (tool-use)
        → query runs against schema + vault.ttl in pyoxigraph
        → Claude summarises the rows in plain prose, with citations.

Usage:
    python scripts/ask.py "Which obligations apply to a data controller?"
    python scripts/ask.py "What does the DPA say about biometric data?" --show-sparql
    python scripts/ask.py "List every defined term" --build-vault

Environment:
    ANTHROPIC_API_KEY — required (loaded from .env at repo root if present).

Dependencies:
    pip install anthropic pyoxigraph PyYAML python-dotenv
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env", override=True)
except ImportError:
    pass

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic not installed. Run: pip install anthropic", file=sys.stderr)
    sys.exit(1)

try:
    import pyoxigraph
except ImportError:
    print("ERROR: pyoxigraph not installed. Run: pip install pyoxigraph", file=sys.stderr)
    sys.exit(1)

REPO_ROOT  = Path(__file__).parent.parent
SCHEMA_TTL = REPO_ROOT / "schema" / "carib_compliance.ttl"
VAULT_TTL  = REPO_ROOT / "vault"  / "vault.ttl"
SPARQL_DIR = REPO_ROOT / "sparql"

DEFAULT_MODEL = "claude-sonnet-4-6"
ENTITY_PREFIX = "https://ontology.carib-comp.org/compliance/entity/"


# ── Store + catalog ──────────────────────────────────────────────────────────

def load_store() -> pyoxigraph.Store:
    store = pyoxigraph.Store()
    for ttl in (SCHEMA_TTL, VAULT_TTL):
        if not ttl.exists():
            print(f"[ask] WARNING: {ttl} not found — skipping", file=sys.stderr)
            continue
        store.load(ttl.read_bytes(), pyoxigraph.RdfFormat.TURTLE,
                   base_iri=str(ttl.as_uri()))
    return store


def entity_catalog(store: pyoxigraph.Store) -> str:
    """Compact list of every named entity: ccoe-prefix · class · label."""
    q = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?s ?label ?cls WHERE {
        ?s a ?cls ;
           rdfs:label ?label .
    }
    ORDER BY ?cls ?label
    """
    rows = list(store.query(q))
    lines = []
    for r in rows:
        iri = str(r["s"]).strip("<>")
        if not iri.startswith(ENTITY_PREFIX):
            continue
        local = iri[len(ENTITY_PREFIX):]
        cls   = str(r["cls"]).rsplit("/", 1)[-1].rstrip(">")
        label = str(r["label"]).split('"')[1] if '"' in str(r["label"]) else str(r["label"])
        lines.append(f"  ccoe:{local}  ({cls})  — {label}")
    return "\n".join(lines) if lines else "  (vault is empty)"


def few_shot_examples() -> str:
    blocks = []
    for cq in sorted(SPARQL_DIR.glob("cq*.rq")):
        blocks.append(f"# {cq.stem}\n{cq.read_text(encoding='utf-8').strip()}")
    return "\n\n".join(blocks) if blocks else "(no example queries available)"


# ── Claude calls ─────────────────────────────────────────────────────────────

def synthesize_sparql(client: anthropic.Anthropic, model: str, question: str,
                      schema: str, catalog: str, examples: str) -> tuple[str, str]:
    system = dedent("""\
        You are a SPARQL expert helping a researcher query a small RDF graph
        about Caribbean data-protection law. Generate exactly one SPARQL SELECT
        query that answers the user's question.

        Rules:
          • Use the prefixes shown in the schema and examples.
          • Always SELECT rdfs:label for any entity you return, so a human can
            read the result.
          • Use OPTIONAL for properties that may be absent.
          • Prefer label-based or class-based matches over hard-coded IRIs when
            the question is generic — that way new entities show up too.
          • If the question is open-ended, return the entity IRI plus its label
            and class, ordered by class then label.
    """)
    user = dedent(f"""\
        # Schema
        ```turtle
        {schema}
        ```

        # Entities currently in the graph
        ```
        {catalog}
        ```

        # Example queries (the project's competency questions)
        {examples}

        # Question
        {question}

        Use the `submit_sparql` tool to return your query and a one-sentence rationale.
    """)
    resp = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system,
        tools=[{
            "name": "submit_sparql",
            "description": "Submit the final SPARQL query that answers the question.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "sparql":    {"type": "string",
                                  "description": "Complete SPARQL query, including PREFIX lines."},
                    "rationale": {"type": "string",
                                  "description": "One sentence explaining how the query answers the question."},
                },
                "required": ["sparql", "rationale"],
                "additionalProperties": False,
            },
        }],
        tool_choice={"type": "tool", "name": "submit_sparql"},
        messages=[{"role": "user", "content": user}],
    )
    for block in resp.content:
        if block.type == "tool_use":
            return block.input["sparql"], block.input["rationale"]
    raise RuntimeError("model did not return a SPARQL query")


def summarise(client: anthropic.Anthropic, model: str, question: str,
              sparql: str, rationale: str, results: dict) -> str:
    system = dedent("""\
        You are a legal-research assistant summarising SPARQL query results in
        plain prose for a researcher. Cite each entity as
        [Label](vault/<local-iri>.md), where <local-iri> is the part of the IRI
        after .../entity/. Be honest about empty results — say so directly. Keep
        the answer under 150 words.
    """)
    user = dedent(f"""\
        Question: {question}

        Generated SPARQL ({rationale}):
        ```sparql
        {sparql}
        ```

        Results (JSON):
        ```json
        {json.dumps(results, indent=2)}
        ```

        Answer the question.
    """)
    resp = client.messages.create(
        model=model,
        max_tokens=600,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(b.text for b in resp.content if b.type == "text").strip()


# ── SPARQL execution ─────────────────────────────────────────────────────────

def run_sparql(store: pyoxigraph.Store, sparql: str) -> dict:
    results = store.query(sparql)
    if isinstance(results, pyoxigraph.QuerySolutions):
        variables = [str(v) for v in results.variables]
        rows = []
        for sol in results:
            row = {}
            for v in results.variables:
                term = sol[v]
                row[str(v)] = str(term) if term is not None else None
            rows.append(row)
        return {"kind": "select", "variables": variables, "rows": rows}
    if isinstance(results, bool):
        return {"kind": "ask", "value": results}
    return {"kind": "graph", "triples": [str(t) for t in results]}


def print_results(results: dict) -> None:
    if results["kind"] == "select":
        rows = results["rows"]
        if not rows:
            print("  (no rows)")
            return
        cols = results["variables"]
        widths = {c: max(len(c), max(len(str(r[c] or "")) for r in rows)) for c in cols}
        print("  " + "  ".join(c.ljust(widths[c]) for c in cols))
        print("  " + "  ".join("-" * widths[c] for c in cols))
        for r in rows:
            print("  " + "  ".join(str(r[c] or "").ljust(widths[c]) for c in cols))
        print(f"\n  {len(rows)} row(s)")
    elif results["kind"] == "ask":
        print(f"  ASK → {results['value']}")
    else:
        for t in results["triples"]:
            print(f"  {t}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ask natural-language questions about the ontology.")
    parser.add_argument("question", nargs="+",
                        help="The question to ask (quote it).")
    parser.add_argument("--show-sparql", action="store_true",
                        help="Print the generated SPARQL and the result table.")
    parser.add_argument("--build-vault", action="store_true",
                        help="Run to_turtle.py first to refresh vault/vault.ttl.")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Anthropic model (default: {DEFAULT_MODEL}).")
    args = parser.parse_args()

    question = " ".join(args.question)

    if args.build_vault:
        print("[ask] regenerating vault/vault.ttl ...")
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "to_turtle.py")],
            cwd=REPO_ROOT, capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            sys.exit(1)

    store   = load_store()
    schema  = SCHEMA_TTL.read_text(encoding="utf-8")
    catalog = entity_catalog(store)
    examples = few_shot_examples()
    client  = anthropic.Anthropic()

    print(f"[ask] question: {question}")
    print(f"[ask] synthesising SPARQL with {args.model} ...")
    sparql, rationale = synthesize_sparql(
        client, args.model, question, schema, catalog, examples)

    if args.show_sparql:
        print("\n--- SPARQL ---")
        print(sparql)
        print(f"\nRationale: {rationale}")

    print("[ask] executing query ...")
    try:
        results = run_sparql(store, sparql)
    except Exception as e:
        print(f"[ask] query failed: {e}", file=sys.stderr)
        print("\nThe generated SPARQL was:")
        print(sparql)
        sys.exit(2)

    if args.show_sparql:
        print("\n--- Results ---")
        print_results(results)

    print(f"[ask] summarising with {args.model} ...")
    answer = summarise(client, args.model, question, sparql, rationale, results)

    print("\n" + "=" * 60)
    print("ANSWER")
    print("=" * 60)
    print(answer)
    print()


if __name__ == "__main__":
    main()
