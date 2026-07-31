#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

from spec_harvester.controlled_calibration import git_dirty_status, git_head
from spec_harvester.semantic_author_input_pack import (
    SemanticAuthorInputPackOptions,
    build_semantic_author_input_pack,
)
from spec_harvester.semantic_author_pass import (
    CodexSparkSemanticAuthorProvider,
    LMStudioSemanticAuthorProvider,
    SemanticAuthorPassError,
    SemanticAuthorPassOptions,
    run_semantic_author_pass,
)
from spec_harvester.semantic_proposal_quality import (
    evaluate_semantic_proposal_quality,
    load_semantic_author_quality_policy,
)
from spec_harvester.source_manifest import read_repository_source_manifests


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def observed_catalog(manifest: dict[str, Any]) -> dict[str, Any]:
    provides = manifest.get("index", {}).get("provides", {})
    intent_ids = sorted(item for item in provides.get("intents", []) if isinstance(item, str))
    content = {
        "sourcePath": "generated/observed-intents.json",
        "intents": [
            {"intentId": intent_id, "sha256": hashlib.sha256(intent_id.encode()).hexdigest()}
            for intent_id in intent_ids
        ],
    }
    return {**content, "sha256": digest(content)}


def prepare_workspace(candidate: Path, source: Path, root: Path) -> Path:
    workspace = root / "workspace"
    workspace.mkdir()
    shutil.copy2(candidate / "specpm.yaml", workspace / "specpm.yaml")
    shutil.copytree(candidate / "specs", workspace / "specs")
    shutil.copy2(candidate / "harvest.json", workspace / "harvest.json")
    readme = next(
        (
            path
            for name in ("README.md", "README.markdown", "README")
            if (path := source / name).is_file()
        ),
        None,
    )
    if readme is None:
        raise ValueError(f"README evidence is unavailable: {source.name}")
    shutil.copy2(readme, workspace / "README.md")
    return workspace


def validate_source_checkout(source: Path, expected_revision: str) -> None:
    if not source.is_dir() or source.is_symlink():
        raise ValueError(f"Retained source checkout is unavailable: {source.name}")
    head = git_head(source)
    dirty = git_dirty_status(source)
    if head != expected_revision:
        raise ValueError(f"Retained source revision mismatch: {source.name}")
    if dirty is None:
        raise ValueError(f"Retained source status is unavailable: {source.name}")
    if dirty:
        raise ValueError(f"Retained source checkout is dirty: {source.name}")


def source_revisions(inputs: Path, target_ids: set[str]) -> dict[str, str]:
    records = read_repository_source_manifests(inputs)
    revisions = {
        record["id"]: record["revision"]
        for record in records
        if record["id"] in target_ids and isinstance(record.get("revision"), str)
    }
    if set(revisions) != target_ids:
        raise ValueError("Targeted calibration sources are absent from the pinned manifest")
    return revisions


def contains_rubric_term(text: str, term: str) -> bool:
    text_tokens = re.findall(r"[a-z0-9]+", text.casefold())
    term_tokens = re.findall(r"[a-z0-9]+", term.casefold())
    if not term_tokens:
        return False
    width = len(term_tokens)
    return any(
        text_tokens[index : index + width] == term_tokens for index in range(len(text_tokens))
    )


def rubric_metrics(
    target: dict[str, Any], semantic_pass: dict[str, Any], quality: dict[str, Any]
) -> dict[str, Any]:
    proposal = semantic_pass["proposal"]
    claims = proposal["claims"]
    purpose = " ".join(claim["text"].lower() for claim in claims if claim["kind"] == "purpose")
    capability = " ".join(
        claim["text"].lower() for claim in claims if claim["kind"] == "capability"
    )
    purpose_groups = target["purposeConceptGroups"]
    purpose_matches = [
        any(contains_rubric_term(purpose, term) for term in group) for group in purpose_groups
    ]
    purpose_accurate = all(purpose_matches)
    capability_specific = any(
        contains_rubric_term(capability, term) for term in target["specificTerms"]
    )
    intent_decisions = proposal["intentDecisions"]
    reuse_count = sum(item["state"] == "proposed_reuse" for item in intent_decisions)
    experimental = [item for item in intent_decisions if item["state"] == "proposed_experimental"]
    experimental_quality = (
        all(
            item["intentId"].startswith("intent.experimental.")
            and item["userNeedClaimId"]
            and item["nearbyIntentIds"]
            and item["nonGoalClaimIds"]
            for item in experimental
        )
        if experimental
        else None
    )
    critical_edits = int(not purpose_accurate) + int(not capability_specific)
    return {
        "purposeAccurate": purpose_accurate,
        "purposeConceptGroupMatches": purpose_matches,
        "evidenceSupportRate": quality["metrics"]["evidenceSupportRate"],
        "schemaValid": quality["metrics"]["schemaValid"],
        "capabilitySpecific": capability_specific,
        "observedIntentReuseCount": reuse_count,
        "experimentalIntentCount": len(experimental),
        "experimentalIntentQuality": experimental_quality,
        "reviewerEditBurdenRate": round(critical_edits / 2, 4),
    }


def provider_summary(records: list[dict[str, Any]], policy: dict[str, Any]) -> dict[str, Any]:
    completed = [record for record in records if record["status"] == "completed"]
    total = len(records)

    def rate(name: str) -> float:
        return round(sum(bool(item["metrics"][name]) for item in completed) / total, 4)

    def average(name: str) -> float:
        return round(sum(float(item["metrics"][name]) for item in completed) / total, 4)

    failed_count = total - len(completed)

    metrics = {
        "purposeAccuracyRate": rate("purposeAccurate"),
        "evidenceSupportedClaimRate": average("evidenceSupportRate"),
        "schemaValidProposalRate": rate("schemaValid"),
        "reviewerEditBurdenRate": round(
            (
                sum(float(item["metrics"]["reviewerEditBurdenRate"]) for item in completed)
                + failed_count
            )
            / total,
            4,
        ),
        "capabilitySpecificityRate": rate("capabilitySpecific"),
        "observedIntentReuseRate": round(
            sum(item["metrics"]["observedIntentReuseCount"] > 0 for item in completed) / total,
            4,
        ),
        "experimentalIntentProposalRate": round(
            sum(item["metrics"]["experimentalIntentCount"] > 0 for item in completed) / total,
            4,
        ),
    }
    gates = {}
    for name, rule in policy["metrics"].items():
        value = metrics[name]
        threshold = rule["threshold"]
        passed = {
            "greater_than_or_equal": value >= threshold,
            "less_than_or_equal": value <= threshold,
            "equal": value == threshold,
        }[rule["operator"]]
        gates[name] = {"value": value, **rule, "passed": passed}
    return {
        "targetCount": total,
        "completedCount": len(completed),
        "failedCount": failed_count,
        "metrics": metrics,
        "frozenGates": gates,
        "passed": len(completed) == total and all(item["passed"] for item in gates.values()),
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    rubric = json.loads(args.rubric.read_text())
    policy = load_semantic_author_quality_policy()
    if rubric["policySha256"] != policy["policySha256"]:
        raise ValueError("Target rubric policy binding is stale")
    target_ids = {target["repositoryId"] for target in rubric["targets"]}
    revisions = source_revisions(args.source_manifest_dir, target_ids)
    providers = {
        "codex_spark": CodexSparkSemanticAuthorProvider(
            command=args.codex_command, model=args.codex_model
        ),
        "lm_studio": LMStudioSemanticAuthorProvider(
            base_url=args.lm_studio_base_url, model=args.lm_studio_model
        ),
    }
    records: dict[str, list[dict[str, Any]]] = {name: [] for name in providers}
    for target in rubric["targets"]:
        candidate = args.candidate_root / target["repositoryId"] / target["candidateDirectory"]
        source = args.source_root / target["repositoryId"]
        validate_source_checkout(source, revisions[target["repositoryId"]])
        with tempfile.TemporaryDirectory(prefix="p55-t9-") as temporary:
            workspace = prepare_workspace(candidate, source, Path(temporary))
            manifest = yaml.safe_load((workspace / "specpm.yaml").read_text())
            pack = build_semantic_author_input_pack(
                workspace,
                observed_catalog(manifest),
                options=SemanticAuthorInputPackOptions(document_paths=("README.md",)),
            )
            for provider_name, provider in providers.items():
                try:
                    semantic_pass = run_semantic_author_pass(
                        pack,
                        provider,
                        options=SemanticAuthorPassOptions(
                            timeout_seconds=args.timeout_seconds,
                            max_output_bytes=256 * 1024,
                            json_repair_max_attempts=1,
                        ),
                    )
                    quality = evaluate_semantic_proposal_quality(pack, semantic_pass)
                    metrics = rubric_metrics(target, semantic_pass, quality)
                    records[provider_name].append(
                        {
                            "repositoryId": target["repositoryId"],
                            "candidateId": pack["candidateId"],
                            "status": "completed",
                            "qualityStatus": quality["status"],
                            "proposalSha256": semantic_pass["proposal"]["proposalSha256"],
                            "providerReceipt": semantic_pass["providerReceipt"],
                            "claims": semantic_pass["proposal"]["claims"],
                            "intentDecisions": semantic_pass["proposal"]["intentDecisions"],
                            "diagnosticCodes": [item["code"] for item in quality["diagnostics"]],
                            "metrics": metrics,
                        }
                    )
                except (SemanticAuthorPassError, ValueError) as exc:
                    records[provider_name].append(
                        {
                            "repositoryId": target["repositoryId"],
                            "candidateId": pack["candidateId"],
                            "status": "failed",
                            "failureCode": str(exc),
                        }
                    )
    summaries = {
        provider: provider_summary(provider_records, policy)
        for provider, provider_records in records.items()
    }
    report = {
        "apiVersion": "spec-harvester.targeted-semantic-quality-calibration/v0",
        "kind": "SpecHarvesterTargetedSemanticQualityCalibration",
        "authority": "targeted_calibration_evidence_only",
        "sourceManifestSha256": hashlib.sha256(
            (args.source_manifest_dir / "repositories.yml").read_bytes()
        ).hexdigest(),
        "sourceRevisions": dict(sorted(revisions.items())),
        "rubricSha256": digest(rubric),
        "policySha256": policy["policySha256"],
        "providers": {
            provider: {"summary": summaries[provider], "records": provider_records}
            for provider, provider_records in records.items()
        },
        "decision": {
            "p55T10Unblocked": all(summary["passed"] for summary in summaries.values()),
            "thresholdsRedefined": False,
        },
        "privacy": {
            "rawPromptsPersisted": False,
            "rawResponsesPersisted": False,
            "chainOfThoughtPersisted": False,
            "credentialsPersisted": False,
            "machineLocalPathsPersisted": False,
        },
        "materializationCount": 0,
        "registryMutationCount": 0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rubric", type=Path, required=True)
    parser.add_argument("--candidate-root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source-manifest-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--codex-command", default="codex")
    parser.add_argument("--codex-model", default="gpt-5.3-codex-spark")
    parser.add_argument("--lm-studio-base-url", default="http://127.0.0.1:1234")
    parser.add_argument("--lm-studio-model", default="openai/gpt-oss-20b")
    parser.add_argument("--timeout-seconds", type=float, default=180)
    args = parser.parse_args()
    try:
        report = run(args)
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}))
        return 2
    print(json.dumps(report["decision"], sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
