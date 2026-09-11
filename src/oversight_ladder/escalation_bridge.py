# SPDX-License-Identifier: Apache-2.0
"""escalation -> rung -> obligation.

Feeds loomground-escalation's ``ceiling()`` the Ladder read from grades.json
(via :mod:`oversight_ladder.ladder`) and a caller-supplied set of Factors,
then looks the resulting granted rung up in :mod:`oversight_ladder.
obligations`. This module ships no ceiling calculus of its own — ``ceiling``,
``Factor``, and ``autonomy_verdict`` are all loomground_escalation's; this is
only the wiring from its output to this layer's obligation table.
"""
from __future__ import annotations

from typing import Iterable

from .ladder import _import_escalation, autonomy_ladder
from .obligations import RungObligation, obligation_for


def resolve(factors: Iterable, *, delegated: str) -> RungObligation:
    """The oversight obligation the escalated (granted) rung carries.

    ``factors`` are loomground_escalation.Factor instances (unassessed ones
    cap at the ladder floor, fail-closed, exactly as escalation.ceiling
    already guarantees — see its docstring). ``delegated`` is the actor's
    standing grade before any factor is applied.
    """
    ladder = autonomy_ladder()
    escalation = _import_escalation().ceiling(
        factors, delegated=delegated, ladder=ladder)
    return obligation_for(escalation.granted)


def resolve_with_escalation(factors: Iterable, *, delegated: str):
    """Like :func:`resolve`, but also returns the Escalation itself, so a
    caller can read ``.why()`` / ``.binding`` / ``.unassessed`` without a
    second call into loomground_escalation."""
    ladder = autonomy_ladder()
    escalation = _import_escalation().ceiling(
        factors, delegated=delegated, ladder=ladder)
    return obligation_for(escalation.granted), escalation
