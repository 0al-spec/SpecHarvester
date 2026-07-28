from __future__ import annotations

import json
from pathlib import Path


def test_p53_t7_scale_out_decision_is_machine_readable_and_wave_bounded() -> None:
    path = Path("SPECS/INPROGRESS/P53-T7_Scale_Out_Decision.json")
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["apiVersion"] == "spec-harvester.p53-scale-out-decision/v0"
    assert payload["task"] == "P53-T7"
    assert payload["status"] == "passed"
    assert payload["decision"] == "unlock_wave-2_only"
    assert payload["fromWave"] == "wave-1"
    assert payload["toWave"] == "wave-2"
    assert payload["sourceWaveReport"]["task"] == "P53-T6"
    assert len(payload["sourceWaveReport"]["sha256"]) == 64
    assert len(payload["humanReview"]["reviewedRepositoryIds"]) == 5
    assert payload["qualityMetrics"]["unsupportedClaimRate"] <= 0.02
    assert "wave-3_unlock" in payload["nonGoals"]


def test_p53_t9_scale_out_decision_is_machine_readable_and_wave_bounded() -> None:
    path = Path("SPECS/INPROGRESS/P53-T9_Scale_Out_Decision.json")
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["apiVersion"] == "spec-harvester.p53-scale-out-decision/v0"
    assert payload["task"] == "P53-T9"
    assert payload["status"] == "passed"
    assert payload["decision"] == "unlock_wave-3_only"
    assert payload["fromWave"] == "wave-2"
    assert payload["toWave"] == "wave-3"
    assert payload["sourceWaveReport"]["task"] == "P53-T8"
    assert len(payload["sourceWaveReport"]["sha256"]) == 64
    assert len(payload["humanReview"]["reviewedRepositoryIds"]) == 3
    assert payload["qualityMetrics"]["unsupportedClaimRate"] <= 0.02
    assert payload["qualityMetrics"]["terminalFailureCount"] == 0
    assert payload["correctionDisposition"]["repositoryId"] == "bitcoin-bitcoin"
    assert "wave-4_unlock" in payload["nonGoals"]
