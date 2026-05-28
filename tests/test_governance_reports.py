from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.governance_reports import (
    BROAD_LANGUAGE_NEUTRAL_INTENTS,
    build_duplicate_claim_report,
    parse_specpm_claims,
)

EXPECTED_BROAD_LANGUAGE_NEUTRAL_INTENTS = (
    "intent.api.contract_surface",
    "intent.developer.tooling_surface",
    "intent.documentation.knowledge_base",
    "intent.metadata.schema_validation",
    "intent.package.public_repository_metadata",
    "intent.workflow.automation_pipeline",
)


def test_build_duplicate_claim_report_merges_accepted_and_candidates(tmp_path: Path) -> None:
    accepted_root = tmp_path / "accepted"
    candidates_root = tmp_path / "candidates"
    accepted_root.mkdir(parents=True)
    candidates_root.mkdir(parents=True)

    write_manifest(
        accepted_root / "alpha" / "0.1.0" / "specpm.yaml",
        "example.alpha",
        "0.1.0",
        intents=["intent.package.utility", "intent.package.workflow"],
        capabilities=["cap.alpha.main", "cap.shared"],
    )
    write_manifest(
        accepted_root / "beta" / "0.2.0" / "specpm.yaml",
        "example.beta",
        "0.2.0",
        intents=["intent.package.utility"],
        capabilities=["cap.shared"],
    )
    write_manifest(
        candidates_root / "gamma" / "1.0.0" / "specpm.yaml",
        "example.gamma",
        "1.0.0",
        intents=["intent.package.utility", "intent.package.editor"],
        capabilities=["cap.gamma.main"],
    )

    report = build_duplicate_claim_report(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
    )

    assert report["summary"]["records"] == 3
    assert report["summary"]["duplicateIntentCount"] == 1
    assert report["summary"]["duplicateCapabilityCount"] == 1

    intent_duplicate = report["duplicates"]["intent"][0]
    assert intent_duplicate["claim"] == "intent.package.utility"
    assert intent_duplicate["count"] == 3
    assert {item["source"] for item in intent_duplicate["claimants"]} == {
        "accepted",
        "candidate",
    }

    capability_duplicate = report["duplicates"]["capability"][0]
    assert capability_duplicate["claim"] == "cap.shared"
    assert capability_duplicate["count"] == 2


def test_build_duplicate_claim_report_treats_broad_language_neutral_intents_as_record_only(
    tmp_path: Path,
) -> None:
    candidates_root = tmp_path / "candidates"
    candidates_root.mkdir(parents=True)

    write_manifest(
        candidates_root / "docs-a" / "1.0.0" / "specpm.yaml",
        "example.docs_a",
        "1.0.0",
        intents=EXPECTED_BROAD_LANGUAGE_NEUTRAL_INTENTS,
        capabilities=["cap.docs_a"],
    )
    write_manifest(
        candidates_root / "docs-b" / "1.0.0" / "specpm.yaml",
        "example.docs_b",
        "1.0.0",
        intents=EXPECTED_BROAD_LANGUAGE_NEUTRAL_INTENTS,
        capabilities=["cap.docs_b"],
    )

    report = build_duplicate_claim_report(candidates_root=candidates_root)

    assert report["summary"]["records"] == 2
    assert report["summary"]["duplicateIntentCount"] == 0
    assert report["duplicates"]["intent"] == []
    assert BROAD_LANGUAGE_NEUTRAL_INTENTS == EXPECTED_BROAD_LANGUAGE_NEUTRAL_INTENTS
    assert all(
        set(EXPECTED_BROAD_LANGUAGE_NEUTRAL_INTENTS).issubset(record["intents"])
        for record in report["records"]
    )


def test_build_duplicate_claim_report_keeps_specific_intent_duplicates(tmp_path: Path) -> None:
    candidates_root = tmp_path / "candidates"
    candidates_root.mkdir(parents=True)

    write_manifest(
        candidates_root / "web-a" / "1.0.0" / "specpm.yaml",
        "example.web_a",
        "1.0.0",
        intents=["intent.web.framework_surface", "intent.api.contract_surface"],
        capabilities=["cap.web_a"],
    )
    write_manifest(
        candidates_root / "web-b" / "1.0.0" / "specpm.yaml",
        "example.web_b",
        "1.0.0",
        intents=["intent.web.framework_surface", "intent.api.contract_surface"],
        capabilities=["cap.web_b"],
    )

    report = build_duplicate_claim_report(candidates_root=candidates_root)

    assert report["summary"]["duplicateIntentCount"] == 1
    duplicate = report["duplicates"]["intent"][0]
    assert duplicate["claim"] == "intent.web.framework_surface"
    assert duplicate["count"] == 2


def test_parse_specpm_claims_rejects_missing_metadata(tmp_path: Path) -> None:
    manifest = tmp_path / "missing-specpm.yaml"
    manifest.write_text("kind: SpecPackage\nindex: {}\n", encoding="utf-8")

    try:
        parse_specpm_claims(manifest, "candidate")
    except ValueError as exc:
        assert "metadata.id and metadata.version" in str(exc)
    else:
        raise AssertionError("Expected ValueError for missing metadata")


def test_parse_specpm_claims_reads_provides_intents(tmp_path: Path) -> None:
    manifest = tmp_path / "specpm.yaml"
    write_manifest(
        manifest,
        "demo.core",
        "1.0.0",
        intents=["intent.package.workflow", "intent.package.utility"],
        capabilities=["cap.workflow"],
        nested_provides_intents=True,
    )

    record = parse_specpm_claims(manifest, "candidate")

    assert record.intents == ("intent.package.utility", "intent.package.workflow")
    assert record.capabilities == ("cap.workflow",)


def test_cli_governance_report_emits_json(tmp_path: Path) -> None:
    candidates_root = tmp_path / "candidates"
    accepted_root = tmp_path / "accepted"
    candidates_root.mkdir()
    accepted_root.mkdir()
    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        "demo",
        "1.0.0",
        intents=["intent.package.workflow"],
        capabilities=["cap.workflow"],
    )

    exit_code = main(
        [
            "governance-report",
            "--candidates-root",
            str(candidates_root),
            "--accepted-root",
            str(accepted_root),
        ]
    )

    assert exit_code == 0


def test_cli_governance_report_writes_output_file(tmp_path: Path) -> None:
    accepted_root = tmp_path / "accepted"
    output = tmp_path / "governance.json"
    accepted_root.mkdir()
    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        "demo",
        "1.0.0",
        intents=["intent.package.workflow"],
        capabilities=["cap.workflow"],
    )

    exit_code = main(
        [
            "governance-report",
            "--accepted-root",
            str(accepted_root),
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["summary"]["records"] == 1


def write_manifest(
    path: Path,
    package_id: str,
    version: str,
    intents: list[str],
    capabilities: list[str],
    nested_provides_intents: bool = False,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    intents_block = (
        "    intents:\n" + "".join(f"      - {intent}\n" for intent in intents)
        if nested_provides_intents
        else "  intents:\n" + "".join(f"    - {intent}\n" for intent in intents)
    )
    path.write_text(
        (
            "apiVersion: specpm.dev/v0.1\n"
            "kind: SpecPackage\n"
            "metadata:\n"
            f"  id: {package_id}\n"
            f"  name: Demo package\n"
            f"  version: {version}\n"
            "index:\n"
            "  provides:\n"
            "    capabilities:\n"
            + "".join(f"      - {capability}\n" for capability in capabilities)
            + intents_block
        ),
        encoding="utf-8",
    )
