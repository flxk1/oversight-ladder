# SPDX-License-Identifier: Apache-2.0
"""The per-rung human-oversight obligation standard.

One :class:`RungObligation` per L0-L6 rung, authored against the ratified
mapping (contract, "Build" section) and cross-referenced to:

* the ``.lg`` file that expresses it as loomground declarations (``lg/``);
* the AI Act Art. 14(4) measure it corresponds to (grounding, not a claim of
  legal satisfaction — see the loomground spec's own disclaimer, §1);
* the oversight-certificate facet names RVND's ``rvnd-pack/commons/
  commons.json`` (``meaningful-oversight``) already ships, cited by name only
  — this module composes nothing and reimplements no certificate logic.

Rung tokens themselves are never hardcoded here: :func:`rung_table` builds
its keys from :func:`oversight_ladder.ladder.grade_levels`, so a change to
grades.json (a new rung, a rename) surfaces as a missing/extra key rather
than silently drifting from this table.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple

from .ladder import grade_levels

_LG_DIR = Path(__file__).resolve().parents[2] / "lg"

# The three facet names RVND's commons.json ships under "meaningful-oversight"
# (rvnd-pack/commons/commons.json). Cited, not recomputed: this module names
# which facets a rung's human-facing obligation point should satisfy when
# exercised; whether they are in fact satisfied is a host/RVND concern.
CERTIFICATE_FACETS: Tuple[str, ...] = (
    "human-authorship-attestation",
    "reasoned-rationale",
    "considered-record",
)

# adopted: loomground names no L1/L4 meaning of its own and
# RVND's action_gate.py/test_autonomy_ladder_iso.py name only L0/L2/L3/L5/L6
# (see grounding strings below) — L1 and L4's meanings are this layer's own
# ratified-but-refinable working adoption (contract, "Ratified decisions").
_REFINABLE = frozenset({"L1", "L4"})


@dataclass(frozen=True)
class RungObligation:
    rung: str
    label: str
    status: str                    # "adopted"
    art14: str                     # AI Act citation this rung's measure grounds in
    summary: str
    lg_file: str
    certificate_facets: Tuple[str, ...] = ()
    grounding: str = ""            # where the RVND-authoritative meaning is named


_TABLE: dict[str, RungObligation] = {
    "L0": RungObligation(
        rung="L0", label="operator-controlled", status="adopted",
        art14="Art. 14(4)(d)",
        summary="Per-step approval: every action is referred to a human "
                 "operator, unconditionally.",
        lg_file="L0.lg",
        certificate_facets=CERTIFICATE_FACETS,
        grounding="RVND action_gate.py: 'L0 operator-controlled (a human "
                   "approves every step)'",
    ),
    "L1": RungObligation(
        rung="L1", label="propose/notify", status="adopted",
        art14="Art. 14(4)(a)",
        summary="After-the-fact notify obligation on every action; auto-"
                 "release restricted to reversible effects — an irreversible "
                 "effect is referred to a human overseer instead.",
        lg_file="L1.lg",
        certificate_facets=CERTIFICATE_FACETS,
        grounding="Not named by RVND's action_gate.py/test_autonomy_ladder_"
                   "iso.py (which name L0/L2/L3/L5/L6, not L1); this "
                   "layer's own ratified working meaning.",
    ),
    "L2": RungObligation(
        rung="L2", label="partial", status="adopted",
        art14="Art. 14(4)(c)",
        summary="Required grade L2 on the source gate (below it, withheld "
                 "pending oversight); any consequential-effect action is "
                 "reserved to a human reviewer before it takes effect.",
        lg_file="L2.lg",
        certificate_facets=CERTIFICATE_FACETS,
        grounding="RVND action_gate.py: 'L2 partial (clears PII/security-"
                   "control footprints)'",
    ),
    "L3": RungObligation(
        rung="L3", label="standby-conditional", status="adopted",
        art14="Art. 14(4)(d)+(e)",
        summary="Financial, irreversible, and external-publish footprints "
                 "clear only via reservation to a standby human operator "
                 "(sign-off), never through the grade comparison alone.",
        lg_file="L3.lg",
        certificate_facets=CERTIFICATE_FACETS,
        grounding="RVND action_gate.py: 'L3 standby-conditional (financial/"
                   "irreversible/external-publish clear only as CONDITIONAL/"
                   "sign-off)'",
    ),
    "L4": RungObligation(
        rung="L4", label="supervised automation", status="adopted",
        art14="Art. 14(4)(b)+(e)",
        summary="Unattended action under continuous-monitoring and "
                 "intervention/stop obligations; a separate control-change "
                 "gate requires quorum (two distinct parties) so no actor "
                 "approves the widening of its own permissions.",
        lg_file="L4.lg",
        certificate_facets=CERTIFICATE_FACETS,
        grounding="Not named by RVND's action_gate.py/test_autonomy_ladder_"
                   "iso.py (which name L0/L2/L3/L5/L6, not L4); this "
                   "layer's own ratified working meaning (unattended + "
                   "active monitoring + real intervention/stop).",
    ),
    "L5": RungObligation(
        rung="L5", label="full automation", status="adopted",
        art14="Art. 26",
        summary="Auto-releases with an ex-post audit and kill-switch "
                 "obligation; every high-stakes footprint (personal-data, "
                 "security-control, financial, irreversible, external-"
                 "publish) is prohibited outright, not merely reserved.",
        lg_file="L5.lg",
        certificate_facets=CERTIFICATE_FACETS,
        grounding="RVND action_gate.py: 'L5 full automation (the former "
                   "\"silent publish\"); never carries high-stakes "
                   "footprints'",
    ),
    "L6": RungObligation(
        rung="L6", label="self-governing", status="adopted",
        art14="—",
        summary="No meaningful human oversight is possible at this rung: "
                 "every action is prohibited, unconditionally. Never "
                 "granted.",
        lg_file="L6.lg",
        certificate_facets=(),
        grounding="RVND action_gate.py/test_autonomy_ladder_iso.py: "
                   "'self-governing autonomy (L6) is never permitted' "
                   "(the always-refused ceiling)",
    ),
}


def rung_table() -> dict[str, RungObligation]:
    """The per-rung table, keyed exactly by grades.json's current levels.

    Raises if the ladder and this table have drifted apart — a rung added or
    renamed upstream surfaces here rather than silently reading a stale
    obligation, or worse, reading none.
    """
    levels = grade_levels()
    missing = set(levels) - set(_TABLE)
    extra = set(_TABLE) - set(levels)
    if missing or extra:
        raise KeyError(
            f"rung_table() out of sync with grades.json: missing={missing} "
            f"extra={extra}")
    return dict(_TABLE)


def obligation_for(rung: str) -> RungObligation:
    """The oversight obligation for one rung. Raises KeyError off the ladder."""
    table = rung_table()
    if rung not in table:
        raise KeyError(f"{rung!r} is not on the active ladder: {grade_levels()}")
    return table[rung]


def lg_path(rung: str) -> Path:
    return _LG_DIR / obligation_for(rung).lg_file
