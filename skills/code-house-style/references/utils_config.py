"""
:module: references/utils_config.py (benz-skills code-house-style)
:purpose: load_config + get_cfg, copied VERBATIM from das_ani/src/utils.py (2026-11-09). Copy these two functions verbatim
          into every new repo's src/utils.py: the identical signature across repos is the point (das_ani CLAUDE.md sect. 5.3).
:gotcha: a YAML key set to null returns None, NOT the default -> write get_cfg(...) or fallback where null is legal.
"""
from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


def load_config(path: str | Path) -> dict[str, Any]:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(p)

    suf = p.suffix.lower()
    if suf in {".yaml", ".yml"}:
        try:
            import yaml
        except ImportError as e:
            raise ImportError("YAML config requested but PyYAML is not installed. Run: pip install pyyaml") from e
        with p.open("r") as f:
            cfg = yaml.safe_load(f)
            if not isinstance(cfg, dict):
                raise ValueError("Config root must be a mapping/dict.")
            return cfg

    if suf == ".json":
        with p.open("r") as f:
            cfg = json.load(f)
            if not isinstance(cfg, dict):
                raise ValueError("Config root must be a mapping/dict.")
            return cfg

    raise ValueError(f"Unsupported config extension: {suf} (use .yaml/.yml/.json)")

def get_cfg(cfg: Mapping[str, Any], keys: Sequence[str], default: Any = None, *, required: bool = False) -> Any:
    cur: Any = cfg
    for k in keys:
        if not isinstance(cur, Mapping) or k not in cur:
            if required:
                raise KeyError(f"Missing config key: {'.'.join(keys)}")
            return default
        cur = cur[k]
    return cur
