"""Settings — API key, model overrides, paths."""
from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from kgforge.project import projects_dir, repo_root
from kgforge.ui.helpers import get_active_project, project_chip

st.set_page_config(page_title="Settings · kgforge", layout="wide")
project_chip()

st.title("⚙ Settings")
st.caption("Per-session overrides. To make settings persistent, edit `.env` or `pack.yaml` directly.")

# ── API key ──────────────────────────────────────────────────────────────────

st.subheader("Anthropic API key")
have = bool(os.environ.get("ANTHROPIC_API_KEY"))
st.markdown(
    f"Currently {'✅ **set**' if have else '❌ **not set**'} "
    f"({'from environment / .env' if have else 'no value'})"
)
new_key = st.text_input(
    "Override for this session",
    type="password",
    placeholder="sk-ant-…",
    help="Setting this overrides the environment for the current Streamlit session only. "
         "For persistence, write it to `.env` at the repo root.",
)
if st.button("Apply API key", disabled=not new_key):
    os.environ["ANTHROPIC_API_KEY"] = new_key
    st.success("API key set for this session.")
    st.rerun()

# ── Active project models ────────────────────────────────────────────────────

project = get_active_project()
if project is not None:
    st.divider()
    st.subheader(f"Models · {project.label}")
    st.caption("These come from the pack. To change permanently, edit `pack.yaml`.")
    cols = st.columns(2)
    with cols[0]:
        st.markdown(f"**Extractor model:** `{project.pack.models.extractor}`")
    with cols[1]:
        st.markdown(f"**Ask model:** `{project.pack.models.ask}`")

# ── Paths ────────────────────────────────────────────────────────────────────

st.divider()
st.subheader("Paths")
st.markdown(f"**Repo root:** `{repo_root()}`")
st.markdown(f"**Projects directory:** `{projects_dir()}`")
if project is not None:
    st.markdown(f"**Active project dir:** `{project.project_dir}`")
    st.markdown(f"**Vault:** `{project.vault_dir}`")
    st.markdown(f"**Inbox:** `{project.inbox_dir}`")

# ── Pack reload ──────────────────────────────────────────────────────────────

st.divider()
st.subheader("Cache")
if st.button("🔄 Reload all packs / projects"):
    # Clear pack-loader memoisation and the per-session project cache.
    from kgforge.pack.loader import load_builtin
    load_builtin.cache_clear()
    st.session_state.pop("_project_cache", None)
    st.cache_resource.clear()
    st.success("Cleared loader caches. Reload other pages to refresh.")

# ── About ────────────────────────────────────────────────────────────────────

st.divider()
st.subheader("About")
st.markdown(
    """
- `kgforge` v0.1.0 — see [`pyproject.toml`](.) for dependencies.
- Source: pack & engine in `kgforge/`, scripts in `scripts/`, projects in `projects/`.
- Phase status: A (config), B (engine + approval), C (UI) — current.
"""
)
