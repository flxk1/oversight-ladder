# SPDX-License-Identifier: Apache-2.0
"""The ladder, read — never minted.

Reads `levels`, `order`, and grounding straight off loomground-governance's
`standard/vocabulary/grades.json` and hands them to loomground-escalation's
`Ladder`. If grades.json ever changes (a new rung, a reordering), this module
changes with it automatically; nothing here hardcodes "L0".."L6".
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from ._paths import escalation_src_dir, governance_standard_dir


def _grades_json() -> dict:
    path = governance_standard_dir() / "vocabulary" / "grades.json"
    return json.loads(path.read_text())


def grade_levels() -> Tuple[str, ...]:
    """The ladder's levels, in order, read from grades.json."""
    return tuple(_grades_json()["levels"])


def grade_grounding() -> str:
    return _grades_json().get("grounding", "")


def _import_escalation():
    """Import loomground_escalation from its source checkout without pip
    installing it — read-only consumption, no parallel copy grown here."""
    src = str(escalation_src_dir())
    if src not in sys.path:
        sys.path.insert(0, src)
    import loomground_escalation  # noqa: PLC0415
    return loomground_escalation


def autonomy_ladder():
    """A loomground_escalation.Ladder built from grades.json's levels.

    This is the one place the two are wired together: the levels are
    loomground-governance's; the ordered-ceiling type is loomground-
    escalation's. Neither is re-derived.
    """
    le = _import_escalation()
    return le.Ladder(grade_levels())


@dataclass(frozen=True)
class LadderInfo:
    levels: Tuple[str, ...]
    order: str
    grounding: str


def ladder_info() -> LadderInfo:
    d = _grades_json()
    return LadderInfo(levels=tuple(d["levels"]), order=d["order"], grounding=d["grounding"])
