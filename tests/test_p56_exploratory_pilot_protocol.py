from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_v2_keeps_v1_protocol_and_benchmark_identity() -> None:
    old = json.loads((ROOT / "SPECS/EVIDENCE/P56-T1/benchmark.json").read_text())
    expected = "1f38cc0fe26003400440212fe5a8be2bea71dada6dcd08b025f814cd39a3b230"
    assert old.pop("benchmarkSha256") == expected
    canonical = json.dumps(old, sort_keys=True, separators=(",", ":")).encode()
    assert hashlib.sha256(canonical).hexdigest() == expected
    assert hashlib.sha256((ROOT / old["protocolPath"]).read_bytes()).hexdigest() == (
        "57e179b59967ddaa64193f76fc8b247f850893ba1330a97d960cff9abe064da2"
    )


def test_v2_targets_preserve_all_five_pins_and_scopes() -> None:
    old = json.loads((ROOT / "SPECS/EVIDENCE/P56-T1/benchmark.json").read_text())
    protocol = (ROOT / "docs/P56_T3A_Exploratory_Pilot_Protocol.md").read_text()
    rows = [line for line in protocol.splitlines() if line.startswith("| ")][1:]
    assert len(rows) == 5
    for source in old["repositories"]:
        assert f"| {source['repository']} | `{source['revision']}` | {source['scope']} |" in rows


def test_v2_is_explicit_exploration_not_relabelled_v1_success() -> None:
    text = " ".join((ROOT / "docs/P56_T3A_Exploratory_Pilot_Protocol.md").read_text().split())
    for required in (
        "p56-exploratory-authoring/v2",
        "gpt-5.6-luna",
        "reasoning `medium`",
        "not a controlled model comparison",
        "not a proven filesystem/network sandbox",
        "One initial authoring attempt",
        "at most one repair",
        "No automatic transport retry",
        "ten-minute operator-observed generation timebox",
        "absent usage/cost is unavailable, not zero",
        "twenty minutes",
        "supported, partial, missing or incorrect",
        "Missing human review leaves the decision pending",
        "P56-T3 and draft PR #372 are deferred",
    ):
        assert required in text
    workplan = (ROOT / "SPECS/Workplan.md").read_text()
    assert "**Deferred under v2.**" in workplan
    assert "[ ] `P56-T3`" in workplan
    assert "P56-T3A" in workplan
    for task in (
        "P56-T4` Generate Five Exploratory Candidate Packages",
        "P56-T5` Prepare Side-by-Side Package Review",
        "P56-T6` Review Five Packages for Practical Utility",
        "P56-T7` Summarize Pilot Failures and Observed Effort",
        "P56-T8` Record Exploratory Pilot Exit Decision",
    ):
        assert task in workplan
