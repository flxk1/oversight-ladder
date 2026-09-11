# SPDX-License-Identifier: Apache-2.0
"""The biometric two-person add-on is separable: the core ladder works
without it, and it works without any rung."""
from pathlib import Path

from oversight_ladder.biometric import ART_14_5_CITE, biometric_addon_path
from oversight_ladder.obligations import lg_path, rung_table
from oversight_ladder.validator import validate_file


def test_addon_is_its_own_file_not_folded_into_any_rung():
    addon = biometric_addon_path()
    assert addon.name == "biometric-two-person.lg"
    for rung in rung_table():
        assert Path(lg_path(rung)).resolve() != addon.resolve()


def test_no_rung_lg_file_references_the_addon_or_art_14_5():
    """The core ladder must not depend on the add-on: none of the L0-L6
    patches may name its gate/kind or cite Art. 14(5)."""
    for rung in rung_table():
        text = lg_path(rung).read_text()
        assert "biometric" not in text.lower()
        assert "14(5)" not in text


def test_addon_declares_no_grade_so_it_binds_to_no_rung_by_default():
    """Statement-level check (comments stripped): no `.lg` line in the
    add-on carries a `grade` clause. The word appears in the file's own
    explanatory comments (by design -- it says why there's no grade), so
    the check must ignore everything after `#`, matching the language's
    own comment rule (SYNTAX.md §2)."""
    lines = biometric_addon_path().read_text().splitlines()
    statements = [ln.split("#", 1)[0] for ln in lines]
    assert not any("grade" in stmt for stmt in statements)


def test_addon_compiles_standalone_without_any_rung_loaded():
    result = validate_file(biometric_addon_path(), engine="ref")
    assert result.well_formed, result.reason
    node_ids = {n["id"] for n in result.projection["nodes"]}
    assert "biometric-id" in node_ids
    assert not (node_ids & set(rung_table()))  # no rung id leaks in


def test_addon_metadata_cites_art_14_5_distinctly_from_the_core_measures():
    assert ART_14_5_CITE == "Art. 14(5)"
    for rung, ob in rung_table().items():
        assert ob.art14 != ART_14_5_CITE
