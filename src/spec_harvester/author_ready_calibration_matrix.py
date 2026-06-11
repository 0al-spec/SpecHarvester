"""Author-ready draft calibration matrix for real-repository runs.

The matrix interprets an existing real-repository quality report as a product
calibration surface: how many author edits remain after SpecHarvester produced
a valid starter package.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

AUTHOR_READY_CALIBRATION_API_VERSION = "spec-harvester.author-ready-calibration-matrix/v0"
AUTHOR_READY_CALIBRATION_KIND = "SpecHarvesterAuthorReadyCalibrationMatrix"
AUTHOR_READY_CALIBRATION_SCHEMA_VERSION = 1

STATUS_AUTHOR_READY = "author_ready_draft"
STATUS_NEEDS_REGENERATION = "needs_regeneration"
STATUS_BLOCKED = "blocked"

PRIORITY_LOW = "low"
PRIORITY_MEDIUM = "medium"
PRIORITY_HIGH = "high"
PRIORITY_BLOCKING = "blocking"

TRUST_BOUNDARY_NOTES = [
    "Author-ready calibration reads existing local JSON artifacts only.",
    "It does not execute harvested repository code or package scripts.",
    "It does not install dependencies, run package managers, or contact registries.",
    "It is product calibration evidence, not SpecPM registry acceptance.",
    "Estimated author edits are review guidance, not upstream endorsement.",
]


def build_author_ready_calibration_matrix(
    quality_report: dict[str, Any],
    *,
    author_notes: dict[str, Any] | None = None,
    quality_report_path: str | Path | None = None,
) -> dict[str, Any]:
    notes = normalize_author_notes(author_notes)
    packages = [
        build_calibration_record(package, notes)
        for package in object_list(quality_report.get("packages"))
    ]
    return {
        "apiVersion": AUTHOR_READY_CALIBRATION_API_VERSION,
        "kind": AUTHOR_READY_CALIBRATION_KIND,
        "schemaVersion": AUTHOR_READY_CALIBRATION_SCHEMA_VERSION,
        "qualityReport": str(quality_report_path)
        if quality_report_path is not None
        else quality_report.get("runReport"),
        "sourceQualityReportKind": string_value(quality_report.get("kind")),
        "packageCount": len(packages),
        "summary": calibration_summary(packages),
        "packages": packages,
        "repeatedGeneratorFollowUps": repeated_generator_follow_ups(packages),
        "trustBoundary": TRUST_BOUNDARY_NOTES,
    }


def build_calibration_record(
    package: dict[str, Any],
    author_notes: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    package_id = string_value(package.get("id"))
    spec_package_id = string_value(package.get("packageId")) or package_id
    note = author_notes.get(package_id) or author_notes.get(spec_package_id) or {}
    categories = edit_categories(package, note)
    estimated_edits = estimated_author_edits(package, note, categories)
    status = author_ready_status(package, note)
    generator_reasons = generator_follow_up_reasons(package, note)
    return {
        "id": package_id,
        "packageId": spec_package_id,
        "qualityVerdict": string_value(package.get("overallVerdict")),
        "authorReadyStatus": status,
        "reviewPriority": review_priority(status, estimated_edits, generator_reasons),
        "estimatedAuthorEdits": estimated_edits,
        "editCategories": categories,
        "intentAccuracy": string_value(package.get("intentAccuracy")),
        "capabilityEvidenceQuality": string_value(package.get("capabilityEvidenceQuality")),
        "analyzerCoverage": string_value(package.get("analyzerCoverage")),
        "specpmStatus": string_value(package.get("specpmStatus")),
        "retryOutcome": string_value(package.get("retryOutcome")),
        "humanReviewNotes": human_review_notes(package, note),
        "generatorFollowUpRecommended": bool(generator_reasons),
        "generatorFollowUpReasons": generator_reasons,
    }


def estimated_author_edits(
    package: dict[str, Any],
    note: dict[str, Any],
    categories: list[str],
) -> int:
    explicit = note.get("estimatedAuthorEdits")
    if isinstance(explicit, int) and explicit >= 0:
        return explicit

    score = 0
    for rating_key in ("intentAccuracy", "capabilityEvidenceQuality", "analyzerCoverage"):
        score += rating_edit_cost(string_value(package.get(rating_key)))

    specpm_status = string_value(package.get("specpmStatus"))
    if specpm_status == "failed":
        score += 2
    elif specpm_status in {"skipped", "not_run"}:
        score += 1

    if string_value(package.get("overallVerdict")) == "review" and score == 0:
        score = 1

    if not categories and score == 0:
        return 0
    return max(score, len(categories))


def edit_categories(package: dict[str, Any], note: dict[str, Any]) -> list[str]:
    explicit = string_list(note.get("editCategories"))
    if explicit:
        return explicit

    categories: set[str] = set()
    if string_value(package.get("intentAccuracy")) in {"partial", "weak", "unscored"}:
        categories.add("intent_summary")
    if string_value(package.get("capabilityEvidenceQuality")) in {"partial", "weak", "unscored"}:
        categories.add("capability_evidence")
    if string_value(package.get("analyzerCoverage")) in {"partial", "weak", "unscored"}:
        categories.add("evidence_depth")
    if string_value(package.get("specpmStatus")) in {"failed", "skipped", "not_run"}:
        categories.add("validation")
    if string_value(package.get("overallVerdict")) == "review":
        categories.add("author_curation")
    return sorted(categories)


def author_ready_status(package: dict[str, Any], note: dict[str, Any]) -> str:
    explicit = string_value(note.get("authorReadyStatus"))
    if explicit in {STATUS_AUTHOR_READY, STATUS_NEEDS_REGENERATION, STATUS_BLOCKED}:
        return explicit

    if string_value(package.get("overallVerdict")) == "fail":
        return STATUS_BLOCKED
    if string_value(package.get("specpmStatus")) == "failed":
        return STATUS_BLOCKED
    if string_value(package.get("overallVerdict")) == "review":
        return STATUS_NEEDS_REGENERATION
    return STATUS_AUTHOR_READY


def generator_follow_up_reasons(package: dict[str, Any], note: dict[str, Any]) -> list[str]:
    explicit = string_list(note.get("generatorFollowUpReasons"))
    if explicit:
        return explicit

    reasons: set[str] = set()
    if string_value(package.get("intentAccuracy")) == "weak":
        reasons.add("weak_intent_generation")
    if string_value(package.get("capabilityEvidenceQuality")) == "weak":
        reasons.add("weak_capability_evidence")
    if string_value(package.get("analyzerCoverage")) == "weak":
        reasons.add("missing_analyzer_coverage")
    if string_value(package.get("specpmStatus")) == "failed":
        reasons.add("specpm_validation_failure")
    if string_value(package.get("retryOutcome")) == "degraded":
        reasons.add("degraded_refinement_retry")
    return sorted(reasons)


def calibration_summary(packages: list[dict[str, Any]]) -> dict[str, Any]:
    status_counts = Counter(package["authorReadyStatus"] for package in packages)
    priority_counts = Counter(package["reviewPriority"] for package in packages)
    edit_category_counts: Counter[str] = Counter()
    total_edits = 0
    for package in packages:
        total_edits += int(package["estimatedAuthorEdits"])
        edit_category_counts.update(package["editCategories"])
    return {
        "packageCount": len(packages),
        "authorReadyDraftCount": status_counts[STATUS_AUTHOR_READY],
        "needsRegenerationCount": status_counts[STATUS_NEEDS_REGENERATION],
        "blockedCount": status_counts[STATUS_BLOCKED],
        "totalEstimatedAuthorEdits": total_edits,
        "averageEstimatedAuthorEdits": round(total_edits / len(packages), 2) if packages else 0,
        "generatorFollowUpCount": sum(
            1 for package in packages if package["generatorFollowUpRecommended"]
        ),
        "editCategoryCounts": dict(sorted(edit_category_counts.items())),
        "reviewPriorityCounts": dict(sorted(priority_counts.items())),
        "calibrationVerdict": calibration_verdict(packages),
    }


def calibration_verdict(packages: list[dict[str, Any]]) -> str:
    if any(package["authorReadyStatus"] == STATUS_BLOCKED for package in packages):
        return "blocked_inputs_present"
    if any(package["generatorFollowUpRecommended"] for package in packages):
        return "generator_follow_up_recommended"
    if any(package["authorReadyStatus"] == STATUS_NEEDS_REGENERATION for package in packages):
        return "mixed_author_ready"
    return "author_curation_ready"


def repeated_generator_follow_ups(packages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: Counter[str] = Counter()
    package_ids: dict[str, list[str]] = {}
    for package in packages:
        for reason in package["generatorFollowUpReasons"]:
            counts[reason] += 1
            package_ids.setdefault(reason, []).append(package["id"])
    return [
        {
            "reason": reason,
            "count": count,
            "packageIds": sorted(package_ids[reason]),
            "followUpRecommended": count >= 2,
        }
        for reason, count in sorted(counts.items())
    ]


def rating_edit_cost(rating: str) -> int:
    return {
        "strong": 0,
        "partial": 1,
        "weak": 2,
        "unscored": 1,
    }.get(rating, 1)


def review_priority(
    status: str,
    estimated_edits: int,
    generator_reasons: list[str],
) -> str:
    if status == STATUS_BLOCKED:
        return PRIORITY_BLOCKING
    if generator_reasons or status == STATUS_NEEDS_REGENERATION or estimated_edits >= 4:
        return PRIORITY_HIGH
    if estimated_edits > 0:
        return PRIORITY_MEDIUM
    return PRIORITY_LOW


def human_review_notes(package: dict[str, Any], note: dict[str, Any]) -> str:
    explicit = string_value(note.get("notes"))
    if explicit:
        return explicit
    return string_value(package.get("humanReviewNotes"))


def normalize_author_notes(raw: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not isinstance(raw, dict):
        return {}
    packages = raw.get("packages", raw)
    if not isinstance(packages, dict):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for key, value in packages.items():
        if isinstance(value, dict):
            result[str(key)] = value
        elif isinstance(value, str):
            result[str(key)] = {"notes": value}
    return result


def write_author_ready_calibration_matrix(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return sorted(item for item in value if isinstance(item, str) and item)


def object_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]
