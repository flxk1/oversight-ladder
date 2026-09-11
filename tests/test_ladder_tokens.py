# SPDX-License-Identifier: Apache-2.0
"""Ladder tokens are read from grades.json, never hardcoded."""
from oversight_ladder.ladder import autonomy_ladder, grade_levels, ladder_info


def test_ladder_is_the_ratified_seven_rungs():
    assert grade_levels() == ("L0", "L1", "L2", "L3", "L4", "L5", "L6")


def test_ladder_info_carries_grades_json_grounding():
    info = ladder_info()
    assert info.order == "L0 < L1 < L2 < L3 < L4 < L5 < L6"
    assert "ISO/IEC 22989" in info.grounding


def test_autonomy_ladder_is_loomground_escalation_type():
    ladder = autonomy_ladder()
    assert type(ladder).__module__.startswith("loomground_escalation")
    assert ladder.levels == ("L0", "L1", "L2", "L3", "L4", "L5", "L6")
    assert ladder.floor == "L0"
    assert ladder.top == "L6"


def test_no_second_ladder_hardcoded_in_this_package():
    """AST-level guard: no source file in the package contains a code literal
    (tuple/list/set) spelling out four-or-more consecutive rung strings
    outside ladder.py's own read of grades.json -- a regrown ladder would be
    a literal like that. Prose in docstrings/comments (e.g. validator.py's
    note on the stale skill engine's own GRADES table) is not code and is
    not what this guards against."""
    import ast
    from pathlib import Path

    RUNGS = ("L0", "L1", "L2", "L3", "L4", "L5", "L6")
    pkg_dir = Path(__file__).resolve().parents[1] / "src" / "oversight_ladder"

    def literal_strings(node):
        if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
            return [e.value for e in node.elts
                    if isinstance(e, ast.Constant) and isinstance(e.value, str)]
        return []

    for f in pkg_dir.glob("*.py"):
        if f.name == "ladder.py":
            continue
        tree = ast.parse(f.read_text(), filename=str(f))
        for node in ast.walk(tree):
            strs = literal_strings(node)
            for i in range(len(strs) - 3):
                window = tuple(strs[i:i + 4])
                assert window != RUNGS[:4], (
                    f"{f} hardcodes the ladder in a code literal; "
                    "read it from ladder.py instead")
