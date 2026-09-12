# SPDX-License-Identifier: Apache-2.0
"""Every rung's declaration compiles WELL-FORMED to .lg.

Validated against loomground-ref (loomground-ref/loomground.py), the current
second conformance implementation whose GRADES table already carries the
ratified L0-L6 ladder. Cross-checked against the loomground-governance
skill's own cached/bundled validator where that engine's ladder covers the
rung (L0-L4); L5/L6 are cross-checked separately in
test_skill_engine_staleness_is_isolated, which demonstrates -- rather than
hides -- that the cached copy has not caught up with grades.json.
"""
import pytest

from oversight_ladder.obligations import lg_path, rung_table
from oversight_ladder.validator import _SKILL_DIR, validate_file

skill_engine = pytest.mark.skipif(
    not _SKILL_DIR.is_dir(),
    reason=f"the skill engine is a host plugin cache, absent here: {_SKILL_DIR}")

RUNGS = list(rung_table())


@pytest.mark.parametrize("rung", RUNGS)
def test_rung_compiles_well_formed_ref_engine(rung):
    result = validate_file(lg_path(rung), engine="ref")
    assert result.well_formed, result.reason
    assert result.projection is not None


@pytest.mark.parametrize("rung", ["L0", "L1", "L2", "L3", "L4"])
@skill_engine
def test_rung_compiles_well_formed_skill_engine_where_ladder_covers_it(rung):
    result = validate_file(lg_path(rung), engine="skill")
    assert result.well_formed, result.reason


@skill_engine
def test_skill_engine_staleness_is_isolated_to_l5_l6():
    """The plugin-cached skill validator's bundled loomground.py still
    carries a five-rung GRADES table (L0..L4) rather than grades.json's
    current seven. It correctly rejects L5/L6 patches for that reason, not
    because the patches are ill-formed -- loomground-ref (which does carry
    L0-L6) accepts them (see test_rung_compiles_well_formed_ref_engine).
    This is recorded as a finding for the skill's maintainer, not routed
    around silently: see README.md's caveats."""
    for rung in ("L5", "L6"):
        skill_result = validate_file(lg_path(rung), engine="skill")
        ref_result = validate_file(lg_path(rung), engine="ref")
        assert not skill_result.well_formed
        assert "not a level of the active ladder" in skill_result.reason
        assert ref_result.well_formed, ref_result.reason


@skill_engine
def test_biometric_addon_compiles_well_formed_both_engines():
    from oversight_ladder.biometric import biometric_addon_path

    for engine in ("ref", "skill"):
        result = validate_file(biometric_addon_path(), engine=engine)
        assert result.well_formed, (engine, result.reason)
