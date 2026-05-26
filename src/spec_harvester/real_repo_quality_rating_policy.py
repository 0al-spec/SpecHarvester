"""Rating policies for real-repository quality reports."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# QualityRating literals
RATING_STRONG = "strong"
RATING_PARTIAL = "partial"
RATING_WEAK = "weak"
RATING_UNSCORED = "unscored"


def step_outcome(steps: list[dict[str, Any]], step_name: str) -> str | None:
    """Return the status of *step_name* from the steps list, or None."""
    for step in steps:
        if step.get("step") == step_name:
            return str(step.get("status", ""))
    return None


@dataclass(frozen=True)
class RatingOutcome:
    rating: str
    notes: str

    def as_tuple(self) -> tuple[str, str]:
        return self.rating, self.notes


@dataclass(frozen=True)
class DraftRatingResolution:
    candidate: dict[str, Any] | None
    blocked: RatingOutcome | None = None


@dataclass(frozen=True)
class DraftRatingPreflight:
    steps: list[dict[str, Any]]
    draft_data: dict[str, Any] | None
    dry_run: bool

    def resolve(self) -> DraftRatingResolution:
        if self.dry_run:
            return self._blocked(RATING_UNSCORED, "dry_run mode; draft not executed")

        draft_status = step_outcome(self.steps, "draft")
        if draft_status is None or draft_status != "ok":
            return self._blocked(RATING_WEAK, "draft step did not complete successfully")

        if self.draft_data is None:
            return self._blocked(
                RATING_WEAK,
                "draft summary artifact not found after successful draft step",
            )

        candidate = self._candidate_payload()
        if candidate is None:
            return self._blocked(RATING_WEAK, "draft summary candidate field is not an object")

        return DraftRatingResolution(candidate=candidate)

    def _blocked(self, rating: str, notes: str) -> DraftRatingResolution:
        return DraftRatingResolution(candidate=None, blocked=RatingOutcome(rating, notes))

    def _candidate_payload(self) -> dict[str, Any] | None:
        assert self.draft_data is not None
        candidate = self.draft_data.get("candidate", self.draft_data)
        return candidate if isinstance(candidate, dict) else None


@dataclass(frozen=True)
class IntentRatingPolicy:
    preflight: DraftRatingPreflight

    @classmethod
    def from_inputs(
        cls,
        steps: list[dict[str, Any]],
        draft_data: dict[str, Any] | None,
        dry_run: bool,
    ) -> IntentRatingPolicy:
        return cls(DraftRatingPreflight(steps, draft_data, dry_run))

    def evaluate(self) -> tuple[str, str]:
        resolution = self.preflight.resolve()
        if resolution.blocked is not None:
            return resolution.blocked.as_tuple()

        candidate = _resolved_candidate(resolution)
        intent = candidate.get("intent") or ""
        if not isinstance(intent, str) or not intent.strip():
            return RATING_WEAK, "draft summary has no intent field"

        evidence_sources = candidate.get("evidenceSources") or []
        if not isinstance(evidence_sources, list):
            evidence_sources = []

        if evidence_sources:
            return RATING_STRONG, f"intent present with {len(evidence_sources)} evidence source(s)"
        return RATING_PARTIAL, "intent present but no evidenceSources references found"


@dataclass(frozen=True)
class CapabilityRatingPolicy:
    preflight: DraftRatingPreflight

    @classmethod
    def from_inputs(
        cls,
        steps: list[dict[str, Any]],
        draft_data: dict[str, Any] | None,
        dry_run: bool,
    ) -> CapabilityRatingPolicy:
        return cls(DraftRatingPreflight(steps, draft_data, dry_run))

    def evaluate(self) -> tuple[str, str]:
        resolution = self.preflight.resolve()
        if resolution.blocked is not None:
            return resolution.blocked.as_tuple()

        candidate = _resolved_candidate(resolution)
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


def _resolved_candidate(resolution: DraftRatingResolution) -> dict[str, Any]:
    assert resolution.candidate is not None
    return resolution.candidate
