# SPDX-License-Identifier: Apache-2.0
"""escalation ceiling -> rung -> obligation, through loomground_escalation's
own ceiling()/autonomy_verdict() -- no ceiling calculus reimplemented here."""
from oversight_ladder.escalation_bridge import resolve, resolve_with_escalation
from oversight_ladder.ladder import _import_escalation


def test_unassessed_factor_caps_at_floor_and_resolves_to_l0():
    le = _import_escalation()
    factors = [le.Factor("reversibility")]  # ceiling=None -> unassessed
    ob = resolve(factors, delegated="L5")
    assert ob.rung == "L0"
    assert ob.label == "operator-controlled"


def test_assessed_factor_caps_below_delegation_resolves_to_that_rung():
    le = _import_escalation()
    factors = [le.Factor("reversibility", ceiling="L3", why="irreversible effect")]
    ob = resolve(factors, delegated="L5")
    assert ob.rung == "L3"
    assert ob.label == "standby-conditional"


def test_no_factor_below_delegation_resolves_to_the_delegated_rung():
    ob = resolve([], delegated="L2")
    assert ob.rung == "L2"


def test_ceiling_never_exceeds_delegation_even_with_no_factors():
    ob, escalation = resolve_with_escalation([], delegated="L1")
    assert ob.rung == "L1"
    assert escalation.granted == "L1"
    assert escalation.binding == ()


def test_l6_reachable_only_by_explicit_delegation_never_by_escalation_alone():
    """Nothing in the escalation calculus can ESCALATE a rung upward -- it
    only ever lowers (loomground_escalation.ceiling's own docstring). L6 is
    reached here only because it was the delegated grade, never because a
    factor raised anything toward it."""
    ob = resolve([], delegated="L6")
    assert ob.rung == "L6"
    assert ob.summary.startswith("No meaningful human oversight")


def test_binding_names_the_capping_factor_for_a_supervisor_to_read():
    le = _import_escalation()
    factors = [
        le.Factor("risk", ceiling="L4", why="high risk"),
        le.Factor("reversibility", ceiling="L2", why="irreversible"),
    ]
    ob, escalation = resolve_with_escalation(factors, delegated="L5")
    assert ob.rung == "L2"
    assert escalation.binding == ("reversibility",)
