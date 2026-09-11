# SPDX-License-Identifier: Apache-2.0
"""Validate a .lg patch against loomground's own checker(s). Read-only
consumption; this module ships no parser and no semantics of its own.

Two engines are available:

* ``"ref"`` (default) — loomground-ref's ``loomground.py``, the current
  second conformance implementation (its GRADES table already carries the
  ratified L0-L6 ladder).
* ``"skill"`` — the loomground-governance skill's bundled/cached
  ``loomground.py`` (the same validator the loomground skill uses for skill
  governance blocks). At the time this repo was built that cached copy's
  GRADES table still reads ``{"L0","L1","L2","L3","L4"}`` — five rungs, not
  the seven grades.json now publishes — so it correctly REJECTS any patch
  declaring L5 or L6. That is a staleness in the cached copy, not a defect in
  these patches; see README.md's caveats. This module still runs both engines
  on request so the discrepancy is demonstrated rather than hidden.
"""
from __future__ import annotations

import importlib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from ._paths import loomground_repos_dir, ref_impl_dir

_SKILL_DIR = (
    Path.home() / ".claude" / "plugins" / "cache" / "loomground"
    / "loomground-governance" / "0.1.0" / "skills" / "loomground"
)


@dataclass(frozen=True)
class ValidationResult:
    engine: str
    well_formed: bool
    reason: str = ""
    projection: Optional[dict] = None


def _load_engine(engine: str):
    if engine == "ref":
        d = str(ref_impl_dir())
    elif engine == "skill":
        d = str(_SKILL_DIR)
    else:
        raise ValueError(f"unknown engine {engine!r}; use 'ref' or 'skill'")
    if not Path(d).is_dir():
        raise FileNotFoundError(f"{engine} engine directory not found: {d}")
    # Force a fresh import from the requested directory: both engines define
    # a top-level module literally named `loomground`, so whichever loaded
    # first would otherwise shadow the other for the rest of the process.
    sys.modules.pop("loomground", None)
    if d not in sys.path:
        sys.path.insert(0, d)
    else:
        sys.path.remove(d)
        sys.path.insert(0, d)
    mod = importlib.import_module("loomground")
    return importlib.reload(mod)


def validate_text(src: str, *, engine: str = "ref") -> ValidationResult:
    L = _load_engine(engine)
    try:
        patch = L.check(L.parse(src))
    except L.Reject as e:
        return ValidationResult(engine=engine, well_formed=False, reason=str(e))
    return ValidationResult(engine=engine, well_formed=True, projection=L.project(patch))


def validate_file(path: Path, *, engine: str = "ref") -> ValidationResult:
    return validate_text(Path(path).read_text(), engine=engine)
