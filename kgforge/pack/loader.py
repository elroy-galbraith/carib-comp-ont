"""Load a DomainPack from a pack directory containing pack.yaml.

Phase A only loads + validates YAML. Hook-module discovery is wired in
during Phase B (when the engine actually consults hooks).
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from kgforge.pack.model import DomainPack

# The compliance pack ships inside the package.
BUILTIN_DIR = Path(__file__).parent / "builtin"


def load_pack(pack_dir: str | Path) -> DomainPack:
    """Load and validate the DomainPack at <pack_dir>/pack.yaml.

    Raises pydantic.ValidationError with field locations on bad config.
    """
    pack_dir = Path(pack_dir).resolve()
    yaml_path = pack_dir / "pack.yaml"
    if not yaml_path.exists():
        raise FileNotFoundError(f"pack.yaml not found in {pack_dir}")

    raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    pack = DomainPack.model_validate(raw)
    pack.pack_dir = pack_dir
    return pack


@lru_cache(maxsize=8)
def load_builtin(name: str) -> DomainPack:
    """Convenience: load a pack shipped under kgforge/pack/builtin/<name>/."""
    return load_pack(BUILTIN_DIR / name)
