# SPDX-License-Identifier: Apache-2.0
"""rung -> oversight obligation lookup."""
import pytest

from oversight_ladder.ladder import grade_levels
from oversight_ladder.obligations import (
    CERTIFICATE_FACETS, obligation_for, rung_table,
)


def test_rung_table_keys_match_the_ladder_exactly():
    assert set(rung_table()) == set(grade_levels())


def test_l1_and_l4_are_marked_adopted_refinable():
    assert obligation_for("L1").status == "adopted (refinable)"
    assert obligation_for("L4").status == "adopted (refinable)"


def test_other_rungs_are_plain_adopted_not_candidate():
    for rung in ("L0", "L2", "L3", "L5", "L6"):
        status = obligation_for(rung).status
        assert status == "adopted", (rung, status)
        assert "CANDIDATE" not in status


def test_l6_carries_no_certificate_facets_never_exercised():
    assert obligation_for("L6").certificate_facets == ()


@pytest.mark.parametrize("rung", ["L0", "L1", "L2", "L3", "L4", "L5"])
def test_human_facing_rungs_cite_the_rvnd_certificate_facets(rung):
    assert obligation_for(rung).certificate_facets == CERTIFICATE_FACETS


def test_unknown_rung_raises_off_the_ladder():
    with pytest.raises(KeyError):
        obligation_for("L99")


def test_every_rung_cites_an_art14_measure_or_explicit_dash():
    for rung, ob in rung_table().items():
        assert ob.art14, rung
