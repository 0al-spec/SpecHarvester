"""Structured quality report for real-repository refinement validation runs.

Derives semantic quality dimensions from a P15-T2 execution report and
per-candidate artifact directories.  Human-review notes may be supplied as
an optional per-package mapping.

Safety rules:
  - Reads only existing local JSON artifacts; never executes repository code,
    installs packages, or contacts external services.
  - Does not embed raw repository source, prompts, provider transcripts,
    chain-of-thought, or secrets.
  - Produced reports are advisory and must not be committed to the repository.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from spec_harvester.interface_index import validate_public_interface_index

QUALITY_REPORT_KIND = "SpecHarvesterRealRepositoryQualityReport"
QUALITY_REPORT_SCHEMA_VERSION = 1
DRAFT_SUMMARY_FILENAME = "draft-summary.json"
LEGACY_DRAFT_FILENAME = "draft.json"
PUBLIC_INTERFACE_INDEX_FILENAME = "public-interface-index.json"
PUBLIC_INTERFACE_INDEX_ANALYZER_TYPE = "publicInterfaceIndex"

# QualityRating literals
RATING_STRONG = "strong"
RATING_PARTIAL = "partial"
RATING_WEAK = "weak"
RATING_UNSCORED = "unscored"

# SpecPMStatus literals
SPECPM_PASSED = "passed"
SPECPM_FAILED = "failed"
SPECPM_SKIPPED = "skipped"
SPECPM_NOT_RUN = "not_run"

# RetryOutcome literals
RETRY_NOT_ATTEMPTED = "not_attempted"
RETRY_IMPROVED = "improved"
RETRY_UNCHANGED = "unchanged"
RETRY_DEGRADED = "degraded"

# OverallVerdict literals
VERDICT_PASS = "pass"
VERDICT_REVIEW = "review"
VERDICT_FAIL = "fail"
VERDICT_UNSCORED = "unscored"

TRUST_BOUNDARY_NOTES = [
    "Quality report generation reads existing local JSON artifacts only.",
    (
        "No repository code execution, package installation, network access, "
        "or analyzer execution is performed."
    ),
    (
        "The report is advisory and does not mutate candidates, accepted packages, "
        "or detailed reports."
    ),
    "Generated quality report files must not be committed to the repository.",
]


def build_quality_report(
    run_report: dict[str, Any],
    *,
    candidates_root: Path | None = None,
    run_report_path: str | Path | None = None,
    human_notes: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Build a quality report dict from an execution run report.

    Args:
        run_report: The JSON execution report produced by the P15-T2 runner.
        candidates_root: Optional override for the candidate output root
            directory.  Defaults to ``run_report["out"]`` when not provided.
        run_report_path: Optional source path for the execution report.
        human_notes: Optional mapping of package id → free-text human-review
            notes to embed in each package record.

    Returns:
        A quality report dict conforming to the schema defined in the P15-T3
        PRD.
    """
    notes = human_notes or {}
    root = Path(candidates_root) if candidates_root is not None else _run_report_root(run_report)
    dry_run = bool(run_report.get("dryRun", False))

    packages = []
    package_records = run_report.get("packages", [])
    if not isinstance(package_records, list):
        package_records = []
    for pkg_record in package_records:
        if not isinstance(pkg_record, dict):
            continue
        pkg_id = str(pkg_record.get("id", ""))
        candidate_dir = _package_candidate_dir(
            pkg_record,
            candidates_root=root,
            package_id=pkg_id,
            prefer_report_path=candidates_root is None,
        )
        record = build_package_quality_record(
            pkg_record,
            candidate_dir=candidate_dir,
            dry_run=dry_run,
            human_review_notes=notes.get(pkg_id, ""),
        )
        packages.append(record)

    summary = _build_summary(packages)

    return {
        "schemaVersion": QUALITY_REPORT_SCHEMA_VERSION,
        "kind": QUALITY_REPORT_KIND,
        "runReport": str(run_report_path)
        if run_report_path is not None
        else run_report.get("runReport"),
        "inputs": run_report.get("inputs"),
        "candidatesRoot": str(root) if root is not None else None,
        "dryRun": dry_run,
        "packageCount": len(packages),
        "summary": summary,
        "packages": packages,
        "trustBoundary": TRUST_BOUNDARY_NOTES,
    }


def build_package_quality_record(
    package_record: dict[str, Any],
    *,
    candidate_dir: Path | None,
    dry_run: bool = False,
    human_review_notes: str = "",
) -> dict[str, Any]:
    """Derive a quality record for one package from its execution record.

    Reads ``draft-summary.json`` (or legacy ``draft.json``), ``harvest.json``,
    and the optional SpecNode result file from *candidate_dir* (when not dry_run
    and not None) to populate the quality dimensions.
    """
    pkg_id = str(package_record.get("id", ""))
    steps = _coerce_step_records(package_record.get("steps", []))

    draft_data = _read_draft_summary(candidate_dir) if not dry_run else None
    harvest_data = _read_candidate_json(candidate_dir, "harvest.json") if not dry_run else None
    specnode_result = (
        _read_candidate_json(candidate_dir, "specnode-refinement-result.json")
        if not dry_run
        else None
    )

    intent_rating, intent_notes = _derive_intent_rating(steps, draft_data, dry_run)
    cap_rating, cap_notes = _derive_capability_rating(steps, draft_data, dry_run)
    specpm_status, specpm_notes = _derive_specpm_status(steps)
    retry_outcome, retry_notes = _derive_retry_outcome(steps, specnode_result)
    token_usage = _extract_token_usage(specnode_result)
    analyzer_coverage, analyzer_notes, analyzers_used = _derive_analyzer_coverage(
        harvest_data, dry_run, candidate_dir=candidate_dir
    )
    overall = _derive_overall_verdict(
        intent_rating=intent_rating,
        cap_rating=cap_rating,
        specpm_status=specpm_status,
        dry_run=dry_run,
    )

    return {
        "id": pkg_id,
        "packageId": package_record.get("packageId"),
        "intentAccuracy": intent_rating,
        "intentNotes": intent_notes,
        "capabilityEvidenceQuality": cap_rating,
        "capabilityNotes": cap_notes,
        "specpmStatus": specpm_status,
        "specpmNotes": specpm_notes,
        "retryOutcome": retry_outcome,
        "retryNotes": retry_notes,
        "tokenUsage": token_usage,
        "analyzerCoverage": analyzer_coverage,
        "analyzerCoverageNotes": analyzer_notes,
        "analyzersUsed": analyzers_used,
        "humanReviewNotes": human_review_notes,
        "overallVerdict": overall,
    }


def write_quality_report(path: Path, report: dict[str, Any]) -> None:
    """Write a quality report dict to *path* as formatted JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _run_report_root(run_report: dict[str, Any]) -> Path | None:
    out = run_report.get("out")
    return Path(out) if out else None


def _package_candidate_dir(
    package_record: dict[str, Any],
    *,
    candidates_root: Path | None,
    package_id: str,
    prefer_report_path: bool,
) -> Path | None:
    if prefer_report_path:
        candidate_dir = package_record.get("candidateDir")
        if isinstance(candidate_dir, str) and candidate_dir:
            return Path(candidate_dir)
    if candidates_root is None:
        return None
    return candidates_root / package_id


def _read_candidate_json(candidate_dir: Path | None, filename: str) -> dict[str, Any] | None:
    if candidate_dir is None:
        return None
    path = candidate_dir / filename
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def _read_draft_summary(candidate_dir: Path | None) -> dict[str, Any] | None:
    for filename in (DRAFT_SUMMARY_FILENAME, LEGACY_DRAFT_FILENAME):
        data = _read_candidate_json(candidate_dir, filename)
        if data is not None:
            return data
    return None


def _coerce_step_records(raw_steps: Any) -> list[dict[str, Any]]:
    if not isinstance(raw_steps, list):
        return []
    return [step for step in raw_steps if isinstance(step, dict)]


def _candidate_payload(draft_data: dict[str, Any]) -> dict[str, Any] | None:
    candidate = draft_data.get("candidate", draft_data)
    return candidate if isinstance(candidate, dict) else None


def _step_outcome(steps: list[dict[str, Any]], step_name: str) -> str | None:
    """Return the status of *step_name* from the steps list, or None."""
    for step in steps:
        if step.get("step") == step_name:
            return str(step.get("status", ""))
    return None


def _derive_intent_rating(
    steps: list[dict[str, Any]],
    draft_data: dict[str, Any] | None,
    dry_run: bool,
) -> tuple[str, str]:
    if dry_run:
        return RATING_UNSCORED, "dry_run mode; draft not executed"

    draft_status = _step_outcome(steps, "draft")
    if draft_status is None or draft_status != "ok":
        return RATING_WEAK, "draft step did not complete successfully"

    if draft_data is None:
        return RATING_WEAK, "draft summary artifact not found after successful draft step"

    candidate = _candidate_payload(draft_data)
    if candidate is None:
        return RATING_WEAK, "draft summary candidate field is not an object"
    intent = candidate.get("intent") or ""
    if not isinstance(intent, str) or not intent.strip():
        return RATING_WEAK, "draft summary has no intent field"

    evidence_sources = candidate.get("evidenceSources") or []
    if not isinstance(evidence_sources, list):
        evidence_sources = []

    if evidence_sources:
        return RATING_STRONG, f"intent present with {len(evidence_sources)} evidence source(s)"
    return RATING_PARTIAL, "intent present but no evidenceSources references found"


def _derive_capability_rating(
    steps: list[dict[str, Any]],
    draft_data: dict[str, Any] | None,
    dry_run: bool,
) -> tuple[str, str]:
    if dry_run:
        return RATING_UNSCORED, "dry_run mode; draft not executed"

    draft_status = _step_outcome(steps, "draft")
    if draft_status is None or draft_status != "ok":
        return RATING_WEAK, "draft step did not complete successfully"

    if draft_data is None:
        return RATING_WEAK, "draft summary artifact not found after successful draft step"

    candidate = _candidate_payload(draft_data)
    if candidate is None:
        return RATING_WEAK, "draft summary candidate field is not an object"
    capabilities = candidate.get("capabilities") or []
    if not isinstance(capabilities, list) or not capabilities:
        return RATING_WEAK, "draft summary has no capabilities"

    total = len(capabilities)
    with_evidence = sum(
        1 for cap in capabilities if isinstance(cap, dict) and cap.get("evidenceSources")
    )

    if with_evidence == total:
        return RATING_STRONG, f"all {total} capability/ies have evidence sources"
    if with_evidence > 0:
        return (
            RATING_PARTIAL,
            f"{with_evidence}/{total} capabilities have evidence sources",
        )
    return RATING_WEAK, f"{total} capability/ies found but none have evidence sources"


def _derive_specpm_status(steps: list[dict[str, Any]]) -> tuple[str, str]:
    outcome = _step_outcome(steps, "specpm")
    if outcome is None:
        return SPECPM_NOT_RUN, "specpm step was not present in the run report"
    if outcome == "skipped":
        return SPECPM_SKIPPED, "specpm validation was skipped"
    if outcome == "ok":
        return SPECPM_PASSED, "specpm validation passed"
    return SPECPM_FAILED, f"specpm step status: {outcome}"


def _derive_retry_outcome(
    steps: list[dict[str, Any]],
    specnode_result: dict[str, Any] | None,
) -> tuple[str, str]:
    specnode_step = _step_outcome(steps, "specnode")
    if specnode_step is None:
        return RETRY_NOT_ATTEMPTED, "no specnode step in run report"

    if specnode_step != "ok":
        return RETRY_DEGRADED, f"specnode step failed (status: {specnode_step})"

    if specnode_result is None:
        return RETRY_UNCHANGED, "specnode step succeeded but result file not found"

    retry_count = specnode_result.get("retryCount") or 0
    if not isinstance(retry_count, int):
        retry_count = 0

    if retry_count == 0:
        return RETRY_UNCHANGED, "specnode step succeeded with no retries"

    improved = specnode_result.get("improved")
    if improved is True:
        return RETRY_IMPROVED, f"specnode step improved after {retry_count} retry/ies"
    return RETRY_UNCHANGED, f"specnode ran {retry_count} retry/ies but no improvement recorded"


def _extract_token_usage(specnode_result: dict[str, Any] | None) -> dict[str, int | None]:
    if specnode_result is None:
        return {"prompt": None, "completion": None}

    usage = specnode_result.get("tokenUsage") or specnode_result.get("usage") or {}
    if not isinstance(usage, dict):
        usage = {}

    def _first_present(d: dict, *keys: str) -> int | float | None:
        for k in keys:
            v = d.get(k)
            if v is not None:
                return v
        return None

    prompt = _first_present(usage, "prompt", "promptTokens", "input_tokens")
    completion = _first_present(usage, "completion", "completionTokens", "output_tokens")
    return {
        "prompt": int(prompt) if isinstance(prompt, (int, float)) else None,
        "completion": int(completion) if isinstance(completion, (int, float)) else None,
    }


def _derive_analyzer_coverage(
    harvest_data: dict[str, Any] | None,
    dry_run: bool,
    *,
    candidate_dir: Path | None = None,
) -> tuple[str, str, list[str]]:
    if dry_run or harvest_data is None:
        return RATING_UNSCORED, "harvest.json not available", []

    files = harvest_data.get("files") or []
    if not isinstance(files, list):
        files = []

    analyzer_types: set[str] = set()
    for f in files:
        if not isinstance(f, dict):
            continue
        # Check well-known analyzer output keys explicitly, then fall back to
        # any dict-valued field that isn't a standard file metadata key.
        _KNOWN_NON_ANALYZER_KEYS = frozenset(
            ("path", "digest", "size", "language", "encoding", "skipped", "error")
        )
        for key, val in f.items():
            if key in _KNOWN_NON_ANALYZER_KEYS:
                continue
            if isinstance(val, dict) and val:
                analyzer_types.add(key)

    summary = harvest_data.get("summary") or {}
    if isinstance(summary, dict):
        for key in ("analyzersUsed", "analyzerTypes"):
            val = summary.get(key)
            if isinstance(val, list):
                analyzer_types.update(str(v) for v in val)

    public_index_notes = _add_public_interface_index_analyzer(candidate_dir, analyzer_types)

    analyzers = sorted(analyzer_types)
    count = len(analyzers)

    if count >= 2:
        notes = f"{count} analyzer type(s) found: {', '.join(analyzers)}"
        if public_index_notes:
            notes = f"{notes}; {public_index_notes}"
        return RATING_STRONG, notes, analyzers
    if count == 1:
        notes = f"1 analyzer type found: {analyzers[0]}"
        if public_index_notes:
            notes = f"{notes}; {public_index_notes}"
        return RATING_PARTIAL, notes, analyzers
    return RATING_WEAK, "harvest.json present but no analyzer output detected", []


def _add_public_interface_index_analyzer(
    candidate_dir: Path | None,
    analyzer_types: set[str],
) -> str:
    if candidate_dir is None:
        return ""

    index_path = candidate_dir / PUBLIC_INTERFACE_INDEX_FILENAME
    if not index_path.exists():
        return ""

    try:
        index_data = json.loads(index_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return ""
    if not isinstance(index_data, dict):
        return ""

    try:
        validate_public_interface_index(index_data)
    except ValueError:
        return ""

    analyzer_types.add(PUBLIC_INTERFACE_INDEX_ANALYZER_TYPE)
    analyzers = index_data.get("analyzers")
    if isinstance(analyzers, list):
        for analyzer in analyzers:
            if not isinstance(analyzer, dict):
                continue
            analyzer_id = analyzer.get("id")
            if isinstance(analyzer_id, str) and analyzer_id.strip():
                analyzer_types.add(analyzer_id.strip())
    return f"{PUBLIC_INTERFACE_INDEX_FILENAME} counted"


def _derive_overall_verdict(
    *,
    intent_rating: str,
    cap_rating: str,
    specpm_status: str,
    dry_run: bool,
) -> str:
    if dry_run:
        return VERDICT_UNSCORED

    if (
        intent_rating == RATING_UNSCORED
        and cap_rating == RATING_UNSCORED
        and specpm_status == SPECPM_NOT_RUN
    ):
        return VERDICT_UNSCORED

    if specpm_status == SPECPM_FAILED or intent_rating == RATING_WEAK:
        return VERDICT_FAIL

    if (
        specpm_status in (SPECPM_PASSED, SPECPM_NOT_RUN, SPECPM_SKIPPED)
        and intent_rating in (RATING_STRONG, RATING_PARTIAL)
        and cap_rating in (RATING_STRONG, RATING_PARTIAL)
    ):
        return VERDICT_PASS

    return VERDICT_REVIEW


def _build_summary(packages: list[dict[str, Any]]) -> dict[str, Any]:
    pass_count = sum(1 for p in packages if p.get("overallVerdict") == VERDICT_PASS)
    review_count = sum(1 for p in packages if p.get("overallVerdict") == VERDICT_REVIEW)
    fail_count = sum(1 for p in packages if p.get("overallVerdict") == VERDICT_FAIL)
    unscored_count = sum(1 for p in packages if p.get("overallVerdict") == VERDICT_UNSCORED)
    return {
        "passCount": pass_count,
        "reviewCount": review_count,
        "failCount": fail_count,
        "unscoredCount": unscored_count,
    }
