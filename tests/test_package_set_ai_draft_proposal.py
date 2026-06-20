from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.package_set_ai_draft_proposal import (
    PACKAGE_SET_AI_DRAFT_API_VERSION,
    PACKAGE_SET_AI_DRAFT_KIND,
    PackageSetAIDraftProposalOptions,
    build_package_set_ai_draft_proposal,
    model_request_record,
    proposal_from_model_output,
)


def test_package_set_ai_draft_request_contains_compact_topology(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    checkout = write_checkout(tmp_path)

    request = model_request_record(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            source_checkout=checkout,
        )
    )

    assert request["apiVersion"] == PACKAGE_SET_AI_DRAFT_API_VERSION
    assert request["packageSet"]["id"] == "demo.workspace"
    assert request["packageSet"]["packageInventoryCount"] == 4
    assert "workspace-inventory.json" in request["allowedEvidencePaths"]
    assert "packages/core/package.json" in request["allowedEvidencePaths"]
    assert "README.md" in request["allowedEvidencePaths"]
    package_ids = {item["packageId"] for item in request["packages"]}
    assert package_ids == {
        "demo.workspace",
        "demo.core",
        "demo.fixture",
        "demo.cli",
    }
    assert "Use only packageIds" in " ".join(request["constraints"])


def test_package_set_ai_draft_request_uses_source_package_fallback_when_inventory_is_empty(
    tmp_path: Path,
) -> None:
    inventory = write_source_backed_empty_package_inventory(tmp_path)

    request = model_request_record(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
        )
    )

    assert request["packageSet"]["id"] == "demo.workspace"
    assert request["packageSet"]["packageInventoryCount"] == 1
    assert request["packages"] == [
        {
            "ecosystem": "",
            "inventoryRole": "member_package",
            "manifestPath": "",
            "name": "demo.workspace",
            "packageId": "demo.workspace",
            "packageManager": "",
            "sourceTargetPath": ".",
            "version": "",
        }
    ]


def test_package_set_ai_draft_wraps_external_model_output(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    assert report["apiVersion"] == PACKAGE_SET_AI_DRAFT_API_VERSION
    assert report["kind"] == PACKAGE_SET_AI_DRAFT_KIND
    assert report["status"] == "completed"
    assert report["authority"] == "proposal_only_not_registry_acceptance"
    assert report["stopPolicySummary"]["decision"] == "stop_for_author_review"
    assert report["stopPolicySummary"]["subjectCount"] == 2
    assert report["validationGuard"] == {
        "authority": "producer_deterministic_pre_normalization_validation",
        "status": "passed",
        "diagnosticCount": 0,
        "errorCount": 0,
        "warningCount": 0,
        "diagnostics": [],
    }
    assert report["packageSet"]["packageId"] == "demo.workspace"
    assert report["provider"]["execution"] == "not_run_by_spec_harvester"
    assert report["summary"] == {
        "errorCount": 0,
        "excludedPackageCount": 1,
        "relationCount": 2,
        "selectedMemberCount": 2,
        "warningCount": 0,
    }
    assert [item["packageId"] for item in report["selectedMembers"]] == [
        "demo.cli",
        "demo.core",
    ]
    assert report["excludedPackages"][0]["packageId"] == "demo.fixture"
    assert {item["targetPackageId"] for item in report["relations"]} == {
        "demo.cli",
        "demo.core",
    }
    assert report["privacy"]["rawModelResponsesPersisted"] is False
    assert "SpecPM remains" in " ".join(report["trustBoundary"])


def test_package_set_ai_draft_reports_unsupported_evidence_paths(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    payload["selectedMembers"][0]["evidencePaths"].append("private/notes.md")
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    assert report["status"] == "warning"
    assert report["stopPolicySummary"]["decision"] == "continue_generation"
    assert "model_evidence_path_unsupported" in {item["code"] for item in report["diagnostics"]}
    core = next(item for item in report["selectedMembers"] if item["packageId"] == "demo.core")
    assert core["evidencePaths"] == [
        "packages/core/package.json",
        "workspace-inventory.json",
    ]


def test_package_set_ai_draft_ignores_blank_evidence_paths(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    payload["selectedMembers"][0]["evidencePaths"].extend(["", "  "])
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    assert report["status"] == "completed"
    assert "model_evidence_path_unsupported" not in {item["code"] for item in report["diagnostics"]}


def test_package_set_ai_draft_fails_package_set_id_mismatch(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    payload["packageSet"]["packageId"] = "demo.renamed_workspace"
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    assert report["status"] == "failed"
    assert report["stopPolicySummary"]["decision"] == "blocked_until_inputs_change"
    assert report["packageSet"]["packageId"] == "demo.workspace"
    assert "package_set_id_mismatch" in {item["code"] for item in report["diagnostics"]}


def test_package_set_ai_draft_infers_missing_package_set_id_without_warning(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    del payload["packageSet"]["packageId"]
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    assert report["status"] == "completed"
    assert report["packageSet"]["packageId"] == "demo.workspace"
    assert report["validationGuard"]["status"] == "passed"
    assert report["validationGuard"]["diagnosticCount"] == 0
    assert "package_set_id_missing" not in {item["code"] for item in report["diagnostics"]}


def test_package_set_ai_draft_warns_when_package_set_object_is_missing(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    del payload["packageSet"]
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    assert report["status"] == "warning"
    assert report["packageSet"]["packageId"] == "demo.workspace"
    assert "package_set_subject_metadata_missing" in {
        item["code"] for item in report["diagnostics"]
    }


def test_package_set_ai_draft_fails_when_subject_identity_is_unrecoverable(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)
    request = model_request_record(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
        )
    )
    request["packageSet"]["id"] = ""
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    del payload["packageSet"]["packageId"]
    payload["relations"] = []

    report = proposal_from_model_output(
        request=request,
        model_output=payload,
        provider={"kind": "test_provider", "execution": "unit_test"},
        provider_receipt={"execution": "unit_test"},
    )

    codes = {item["code"] for item in report["diagnostics"]}
    guard_codes = {item["code"] for item in report["validationGuard"]["diagnostics"]}
    assert report["status"] == "failed"
    assert report["validationGuard"]["status"] == "failed"
    assert report["validationGuard"]["errorCount"] == 1
    assert "package_set_subject_identity_missing" in codes
    assert "package_set_subject_identity_missing" in guard_codes


def test_package_set_ai_draft_normalizes_selected_member_path_to_inventory(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    payload["selectedMembers"][0]["sourceTargetPath"] = "private/override"
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    core = next(item for item in report["selectedMembers"] if item["packageId"] == "demo.core")
    assert report["status"] == "completed"
    assert core["sourceTargetPath"] == "packages/core"


def test_package_set_ai_draft_normalizes_selected_member_role_aliases(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    payload["selectedMembers"][0]["role"] = "core_runtime"
    payload["selectedMembers"][1]["role"] = "react binding"
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    members = {item["packageId"]: item for item in report["selectedMembers"]}
    assert report["status"] == "completed"
    assert members["demo.core"]["role"] == "primary_package"
    assert members["demo.cli"]["role"] == "published_package"
    assert "selected_member_role_unknown" not in {item["code"] for item in report["diagnostics"]}


def test_package_set_ai_draft_warns_and_falls_back_for_unknown_selected_member_role(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    payload["selectedMembers"][0]["role"] = "mystery surface"
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    core = next(item for item in report["selectedMembers"] if item["packageId"] == "demo.core")
    role_diagnostic = next(
        item for item in report["diagnostics"] if item["code"] == "selected_member_role_unknown"
    )
    assert report["status"] == "warning"
    assert core["role"] == "member_package"
    assert role_diagnostic["modelRole"] == "mystery surface"
    assert role_diagnostic["normalizedFallbackRole"] == "member_package"


def test_package_set_ai_draft_fails_invalid_relation_endpoint(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    payload["relations"][0]["targetPackageId"] = "demo.fixture"
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    assert report["status"] == "failed"
    assert "relation_target_not_selected" in {item["code"] for item in report["diagnostics"]}


def test_package_set_ai_draft_fails_unsupported_relation_type(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    payload["relations"][0]["type"] = "depends_on"
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    assert report["status"] == "failed"
    assert "relation_type_unsupported" in {item["code"] for item in report["diagnostics"]}
    assert {item["targetPackageId"] for item in report["relations"]} == {"demo.cli"}


def test_package_set_ai_draft_accepts_common_relation_endpoint_aliases(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    relation = payload["relations"][0]
    relation["source"] = relation.pop("sourcePackageId")
    relation["target"] = relation.pop("targetPackageId")
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    assert report["status"] == "completed"
    assert "relation_target_not_selected" not in {item["code"] for item in report["diagnostics"]}
    assert {item["targetPackageId"] for item in report["relations"]} == {
        "demo.cli",
        "demo.core",
    }


def test_package_set_ai_draft_keeps_unknown_exclusion_warning_for_package_sets(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    payload["excludedPackages"].append(
        {
            "packageId": "demo.docs",
            "category": "out_of_scope",
            "reason": "Documentation site.",
            "evidencePaths": ["workspace-inventory.json"],
            "confidence": "low",
        }
    )
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    assert report["status"] == "warning"
    assert report["validationGuard"]["status"] == "warning"
    assert report["validationGuard"]["diagnosticCount"] == 1
    assert report["validationGuard"]["warningCount"] == 1
    assert "excluded_package_unknown" in {item["code"] for item in report["diagnostics"]}
    assert "excluded_package_unknown" in {
        item["code"] for item in report["validationGuard"]["diagnostics"]
    }


def test_package_set_ai_draft_ignores_unknown_exclusion_for_single_package_inventory(
    tmp_path: Path,
) -> None:
    inventory = write_single_package_inventory(tmp_path)
    model_output = write_single_package_model_output(tmp_path)

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    assert report["status"] == "completed"
    assert report["packageSet"]["packageId"] == "demo.workspace"
    assert [item["packageId"] for item in report["selectedMembers"]] == ["demo.core"]
    assert report["excludedPackages"] == []
    assert report["validationGuard"]["status"] == "passed"
    assert report["validationGuard"]["diagnosticCount"] == 0
    assert "excluded_package_unknown" not in {item["code"] for item in report["diagnostics"]}


def test_package_set_ai_draft_accepts_clean_zero_subject_single_package_policy(
    tmp_path: Path,
) -> None:
    inventory = write_single_package_inventory(tmp_path)
    model_output = write_single_package_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    payload["selectedMembers"] = []
    payload["relations"] = []
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    stop_policy = report["stopPolicySummary"]
    assert report["status"] == "completed"
    assert report["summary"]["selectedMemberCount"] == 0
    assert stop_policy["subjectCount"] == 0
    assert stop_policy["status"] == "author_ready_draft"
    assert stop_policy["decision"] == "stop_for_author_review"
    assert stop_policy["reason"] == "single_package_no_proposal_subjects_non_blocking"
    assert stop_policy["zeroSubjectPolicy"] == {
        "status": "accepted_non_blocking",
        "reason": "single_package_inventory_subject_stable",
        "inventoryPackageCount": 1,
        "inventoryPackageIds": ["demo.core"],
        "packageSetId": "demo.workspace",
    }


def test_package_set_ai_draft_accepts_source_backed_zero_subject_single_package_policy(
    tmp_path: Path,
) -> None:
    inventory = write_source_backed_empty_package_inventory(tmp_path)
    model_output = write_single_package_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    payload["packageSet"]["packageId"] = "demo.workspace"
    payload["selectedMembers"] = []
    payload["relations"] = []
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    stop_policy = report["stopPolicySummary"]
    assert report["status"] == "completed"
    assert report["inputs"][1]["packageCount"] == 1
    assert stop_policy["decision"] == "stop_for_author_review"
    assert stop_policy["reason"] == "single_package_no_proposal_subjects_non_blocking"
    assert stop_policy["zeroSubjectPolicy"] == {
        "status": "accepted_non_blocking",
        "reason": "single_package_inventory_subject_stable",
        "inventoryPackageCount": 1,
        "inventoryPackageIds": ["demo.workspace"],
        "packageSetId": "demo.workspace",
    }


def test_package_set_ai_draft_keeps_no_proposal_subjects_for_multi_package_zero_subjects(
    tmp_path: Path,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    payload["selectedMembers"] = []
    payload["relations"] = []
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    stop_policy = report["stopPolicySummary"]
    assert report["status"] == "completed"
    assert stop_policy["decision"] == "continue_generation"
    assert stop_policy["reason"] == "no_proposal_subjects"
    assert stop_policy["zeroSubjectPolicy"]["status"] == "requires_regeneration"
    assert stop_policy["zeroSubjectPolicy"]["reason"] == "package_set_requires_selected_members"
    assert stop_policy["zeroSubjectPolicy"]["inventoryPackageCount"] == 4


def test_package_set_ai_draft_requires_regeneration_for_warning_zero_subject_single_package(
    tmp_path: Path,
) -> None:
    inventory = write_single_package_inventory(tmp_path)
    model_output = write_single_package_model_output(tmp_path)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    payload["packageSet"]["evidencePaths"] = ["private/notes.md"]
    payload["selectedMembers"] = []
    payload["relations"] = []
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            model_output=model_output,
        )
    )

    stop_policy = report["stopPolicySummary"]
    assert report["status"] == "warning"
    assert stop_policy["decision"] == "continue_generation"
    assert stop_policy["reason"] == "no_proposal_subjects"
    assert stop_policy["zeroSubjectPolicy"] == {
        "status": "requires_regeneration",
        "reason": "single_package_proposal_has_diagnostics",
        "inventoryPackageCount": 1,
        "inventoryPackageIds": ["demo.core"],
        "packageSetId": "demo.workspace",
    }


def test_package_set_ai_draft_cli_writes_request_and_proposal(
    tmp_path: Path,
    capsys,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = write_model_output(tmp_path)
    request_output = tmp_path / "ai" / "request.json"
    proposal_output = tmp_path / "ai" / "proposal.json"

    exit_code = main(
        [
            "package-set-ai-draft-proposal",
            str(inventory),
            "--model-output",
            str(model_output),
            "--request-output",
            str(request_output),
            "--output",
            str(proposal_output),
        ]
    )

    printed = json.loads(capsys.readouterr().out)
    written = json.loads(proposal_output.read_text(encoding="utf-8"))
    requests = json.loads(request_output.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert printed == written
    assert written["status"] == "completed"
    assert requests["kind"] == "SpecHarvesterPackageSetAIDraftRequests"
    assert requests["requests"][0]["packageSet"]["id"] == "demo.workspace"


def test_package_set_ai_draft_repairs_malformed_live_json(
    tmp_path: Path,
    monkeypatch,
) -> None:
    inventory = write_inventory(tmp_path)
    model_output = json.loads(write_model_output(tmp_path).read_text(encoding="utf-8"))
    contents = ["not json", json.dumps(model_output)]
    calls = []

    class FakeResponse:
        def __init__(self, content: str, index: int) -> None:
            self.content = content
            self.index = index

        def __enter__(self) -> FakeResponse:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps(
                {
                    "model": "test-model",
                    "choices": [{"message": {"content": self.content}}],
                    "usage": {"total_tokens": self.index + 1},
                }
            ).encode("utf-8")

    def fake_urlopen(request, **_kwargs):
        payload = json.loads(request.data.decode("utf-8"))
        calls.append(payload)
        return FakeResponse(contents[len(calls) - 1], len(calls))

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            provider_base_url="http://127.0.0.1:1234",
            model="test-model",
            json_repair_max_attempts=1,
        )
    )

    serialized = json.dumps(report)
    assert len(calls) == 2
    assert report["status"] == "warning"
    assert report["providerReceipt"]["jsonRepairNeeded"] is True
    assert report["providerReceipt"]["jsonRepairAttemptCount"] == 1
    assert report["providerReceipt"]["jsonRepairStatus"] == "repaired"
    assert report["providerReceipt"]["usage"]["total_tokens"] == 5
    assert "ai_json_repair_needed" in {item["code"] for item in report["diagnostics"]}
    assert "not json" not in serialized
    assert report["privacy"]["rawModelResponsesPersisted"] is False


def test_package_set_ai_draft_fails_when_json_repair_is_exhausted(
    tmp_path: Path,
    monkeypatch,
) -> None:
    inventory = write_inventory(tmp_path)
    contents = ["not json", "still not json"]
    calls = []

    class FakeResponse:
        def __init__(self, content: str) -> None:
            self.content = content

        def __enter__(self) -> FakeResponse:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps(
                {
                    "model": "test-model",
                    "choices": [{"message": {"content": self.content}}],
                    "usage": {"total_tokens": 1},
                }
            ).encode("utf-8")

    def fake_urlopen(request, **_kwargs):
        payload = json.loads(request.data.decode("utf-8"))
        calls.append(payload)
        return FakeResponse(contents[len(calls) - 1])

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    report = build_package_set_ai_draft_proposal(
        PackageSetAIDraftProposalOptions(
            inventory=inventory,
            provider_base_url="http://127.0.0.1:1234",
            model="test-model",
            json_repair_max_attempts=1,
        )
    )

    serialized = json.dumps(report)
    codes = {item["code"] for item in report["diagnostics"]}
    assert len(calls) == 2
    assert report["status"] == "failed"
    assert report["providerReceipt"]["jsonRepairStatus"] == "exhausted"
    assert "responseDigest" not in report["providerReceipt"]
    assert "ai_json_repair_needed" in codes
    assert "ai_json_repair_exhausted" in codes
    assert "still not json" not in serialized
    assert report["privacy"]["rawModelResponsesPersisted"] is False


def write_inventory(tmp_path: Path) -> Path:
    inventory = {
        "apiVersion": "spec-harvester.workspace-inventory/v0",
        "kind": "SpecHarvesterWorkspaceInventory",
        "schemaVersion": 1,
        "source": {
            "repository": "https://github.com/example/demo",
            "exactRevision": "abc123",
            "revisionAuthority": "source_manifest_revision",
            "declaredRef": None,
        },
        "workspaceManifests": [
            {
                "path": "package.json",
                "ecosystem": "npm",
                "packageManager": "pnpm",
                "includePatterns": ["packages/*"],
                "excludePatterns": ["packages/*/__tests__"],
            }
        ],
        "packages": [
            package_record(".", "demo.workspace", "workspace", "@demo/workspace"),
            package_record("packages/core", "demo.core", "member_package", "@demo/core"),
            package_record("packages/cli", "demo.cli", "member_package", "@demo/cli"),
            package_record(
                "packages/core/__tests__/fixture",
                "demo.fixture",
                "member_package",
                "@demo/fixture",
            ),
        ],
        "summary": {
            "workspaceManifestCount": 1,
            "packageManifestCount": 4,
            "packageCount": 4,
            "diagnosticCount": 0,
        },
        "diagnostics": [],
        "authority": "producer_observed_review_evidence",
    }
    path = tmp_path / "workspace-inventory.json"
    path.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_single_package_inventory(tmp_path: Path) -> Path:
    inventory = {
        "apiVersion": "spec-harvester.workspace-inventory/v0",
        "kind": "SpecHarvesterWorkspaceInventory",
        "schemaVersion": 1,
        "source": {
            "repository": "https://github.com/example/demo",
            "exactRevision": "abc123",
            "revisionAuthority": "source_manifest_revision",
            "declaredRef": None,
        },
        "workspaceManifests": [],
        "packages": [
            package_record(".", "demo.core", "member_package", "demo"),
        ],
        "summary": {
            "workspaceManifestCount": 0,
            "packageManifestCount": 1,
            "packageCount": 1,
            "diagnosticCount": 0,
        },
        "diagnostics": [],
        "authority": "producer_observed_review_evidence",
    }
    path = tmp_path / "single-workspace-inventory.json"
    path.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_source_backed_empty_package_inventory(tmp_path: Path) -> Path:
    inventory = {
        "apiVersion": "spec-harvester.workspace-inventory/v0",
        "kind": "SpecHarvesterWorkspaceInventory",
        "schemaVersion": 1,
        "source": {
            "repository": "https://github.com/example/demo",
            "exactRevision": "abc123",
            "revisionAuthority": "source_manifest_revision",
            "declaredRef": None,
            "packageId": "demo.workspace",
            "target": {
                "kind": "repository",
                "path": ".",
                "label": "demo",
            },
        },
        "workspaceManifests": [],
        "packages": [],
        "summary": {
            "workspaceManifestCount": 0,
            "packageManifestCount": 0,
            "packageCount": 0,
            "diagnosticCount": 0,
        },
        "diagnostics": [],
        "authority": "producer_observed_review_evidence",
    }
    path = tmp_path / "source-backed-empty-workspace-inventory.json"
    path.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def package_record(
    source_target_path: str,
    package_id: str,
    role: str,
    name: str,
) -> dict[str, object]:
    manifest_path = (
        "package.json" if source_target_path == "." else f"{source_target_path}/package.json"
    )
    return {
        "ecosystem": "npm",
        "evidenceReferences": [
            {
                "kind": "package_manifest",
                "path": manifest_path,
                "size": 100,
            }
        ],
        "manifestPath": manifest_path,
        "name": name,
        "packageManager": "npm",
        "proposedSpecpmPackageId": package_id,
        "role": role,
        "sourceTargetPath": source_target_path,
        "version": "1.0.0",
    }


def write_checkout(tmp_path: Path) -> Path:
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    (checkout / "README.md").write_text("# Demo\n\nDemo package set.\n", encoding="utf-8")
    (checkout / "package.json").write_text('{"name":"@demo/workspace"}\n', encoding="utf-8")
    return checkout


def write_model_output(tmp_path: Path) -> Path:
    payload = {
        "packageSet": {
            "packageId": "demo.workspace",
            "summary": "Demo workspace containing core runtime and CLI packages.",
            "evidencePaths": ["workspace-inventory.json"],
            "confidence": "high",
        },
        "selectedMembers": [
            {
                "packageId": "demo.core",
                "role": "primary_package",
                "sourceTargetPath": "packages/core",
                "reason": "Primary runtime package.",
                "evidencePaths": ["workspace-inventory.json", "packages/core/package.json"],
                "confidence": "high",
            },
            {
                "packageId": "demo.cli",
                "role": "cli_package",
                "sourceTargetPath": "packages/cli",
                "reason": "CLI package for the workspace.",
                "evidencePaths": ["workspace-inventory.json", "packages/cli/package.json"],
                "confidence": "medium",
            },
        ],
        "excludedPackages": [
            {
                "packageId": "demo.fixture",
                "category": "fixture",
                "reason": "Test fixture package, not a primary public member.",
                "evidencePaths": [
                    "workspace-inventory.json",
                    "packages/core/__tests__/fixture/package.json",
                ],
                "confidence": "high",
            }
        ],
        "relations": [
            {
                "id": "demo.workspace.contains.demo.core",
                "type": "contains",
                "sourcePackageId": "demo.workspace",
                "targetPackageId": "demo.core",
                "evidencePaths": ["workspace-inventory.json"],
                "confidence": "high",
            },
            {
                "id": "demo.workspace.contains.demo.cli",
                "type": "contains",
                "sourcePackageId": "demo.workspace",
                "targetPackageId": "demo.cli",
                "evidencePaths": ["workspace-inventory.json"],
                "confidence": "medium",
            },
        ],
        "evidenceGaps": [],
        "overallConfidence": "high",
    }
    path = tmp_path / "model-output.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_single_package_model_output(tmp_path: Path) -> Path:
    payload = {
        "packageSet": {
            "summary": "Demo single-package repository.",
            "evidencePaths": ["workspace-inventory.json"],
            "confidence": "high",
        },
        "selectedMembers": [
            {
                "packageId": "demo.core",
                "role": "primary_package",
                "sourceTargetPath": ".",
                "reason": "Stable deterministic single-package candidate.",
                "evidencePaths": ["workspace-inventory.json", "package.json"],
                "confidence": "high",
            }
        ],
        "excludedPackages": [
            {
                "packageId": "demo.docs",
                "category": "out_of_scope",
                "reason": "Model-side documentation exclusion not present in inventory.",
                "evidencePaths": ["workspace-inventory.json"],
                "confidence": "low",
            }
        ],
        "relations": [],
        "evidenceGaps": [],
        "overallConfidence": "high",
    }
    path = tmp_path / "single-model-output.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
