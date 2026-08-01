from __future__ import annotations

import hashlib
import json
import re
from typing import Any

ANCHOR_API_VERSION = "spec-harvester.outcome-purpose-anchors/v0"
ANCHOR_KIND = "SpecHarvesterOutcomePurposeAnchors"

WORD_PATTERN = re.compile(r"[a-z0-9]+")
SENTENCE_PATTERN = re.compile(r"[^.!?\n]+[.!?]?")

STOP_TERMS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "with",
}
MECHANICS_TERMS = {
    "api",
    "application",
    "binary",
    "cli",
    "codebase",
    "command",
    "component",
    "dependency",
    "ecosystem",
    "framework",
    "implementation",
    "import",
    "interface",
    "library",
    "line",
    "manifest",
    "metadata",
    "module",
    "package",
    "plugin",
    "project",
    "repository",
    "runtime",
    "sdk",
    "source",
    "stack",
    "tool",
    "toolkit",
}


def build_outcome_purpose_anchors(
    profile: dict[str, Any],
    evidence: list[dict[str, Any]],
    *,
    candidate_id: str,
    source_bundle_sha256: str,
) -> dict[str, Any]:
    """Build bounded outcome hints from already allowlisted, digest-bound evidence."""
    profile_sha256 = profile.get("profileSha256")
    if not _sha256(profile_sha256):
        raise ValueError("outcome purpose anchor profile binding is invalid")
    evidence_by_path = {
        item.get("sourcePath"): item
        for item in evidence
        if isinstance(item, dict)
        and isinstance(item.get("sourcePath"), str)
        and isinstance(item.get("content"), str)
        and _sha256(item.get("sha256"))
    }
    profile_evidence = evidence_by_path.get("semantic-product-profile.json")
    if not isinstance(profile_evidence, dict):
        raise ValueError("outcome purpose anchor profile evidence is unavailable")

    identity_terms = _identity_terms(profile)
    mechanics_terms = sorted(MECHANICS_TERMS | identity_terms | _technology_terms(profile))
    candidates: list[tuple[str, str, str]] = []
    description = profile.get("package", {}).get("description")
    if isinstance(description, str) and description.strip():
        candidates.append(
            (
                "semantic-product-profile.json",
                str(profile_evidence["sha256"]),
                description.strip(),
            )
        )
    for document in profile.get("documents", []):
        if not isinstance(document, dict):
            continue
        item = evidence_by_path.get(document.get("evidencePath"))
        if not isinstance(item, dict) or item.get("sha256") != document.get("sha256"):
            continue
        for match in SENTENCE_PATTERN.finditer(str(item["content"])):
            phrase = " ".join(match.group().split())
            if 20 <= len(phrase) <= 360:
                candidates.append((str(item["sourcePath"]), str(item["sha256"]), phrase))
            if len(candidates) >= 24:
                break

    anchors: list[dict[str, Any]] = []
    seen_phrases: set[str] = set()
    for source_path, sha256, phrase in candidates:
        normalized = phrase.casefold()
        if normalized in seen_phrases:
            continue
        seen_phrases.add(normalized)
        outcome_terms = sorted(
            token
            for token in set(_tokens(phrase))
            if len(token) >= 3 and token not in STOP_TERMS and token not in mechanics_terms
        )[:16]
        if not outcome_terms:
            continue
        anchors.append(
            {
                "sourcePath": source_path,
                "sha256": sha256,
                "phrase": phrase,
                "outcomeTerms": outcome_terms,
                "untrusted": True,
            }
        )
        if len(anchors) == 8:
            break

    record = {
        "apiVersion": ANCHOR_API_VERSION,
        "kind": ANCHOR_KIND,
        "schemaVersion": 1,
        "authority": "deterministic_untrusted_outcome_guidance",
        "candidateId": candidate_id,
        "sourceBundleSha256": source_bundle_sha256,
        "profileSha256": profile_sha256,
        "anchors": anchors,
        "mechanicsTerms": mechanics_terms,
        "executionBoundary": {
            "providerInvoked": False,
            "repositoryCodeExecuted": False,
            "materializationPerformed": False,
        },
    }
    record["anchorsSha256"] = _digest_without(record, "anchorsSha256")
    validate_outcome_purpose_anchors(record, profile=profile, evidence=evidence)
    return record


def validate_outcome_purpose_anchors(
    record: dict[str, Any],
    *,
    profile: dict[str, Any] | None = None,
    evidence: list[dict[str, Any]] | None = None,
) -> None:
    if (
        not isinstance(record, dict)
        or record.get("apiVersion") != ANCHOR_API_VERSION
        or record.get("kind") != ANCHOR_KIND
        or record.get("schemaVersion") != 1
        or record.get("authority") != "deterministic_untrusted_outcome_guidance"
        or not isinstance(record.get("candidateId"), str)
        or not _sha256(record.get("sourceBundleSha256"))
        or not _sha256(record.get("profileSha256"))
        or record.get("anchorsSha256") != _digest_without(record, "anchorsSha256")
    ):
        raise ValueError("outcome purpose anchor record is invalid")
    anchors = record.get("anchors")
    mechanics = record.get("mechanicsTerms")
    if (
        not isinstance(anchors, list)
        or len(anchors) > 8
        or not isinstance(mechanics, list)
        or mechanics != sorted(set(mechanics))
        or not all(isinstance(term, str) and term for term in mechanics)
    ):
        raise ValueError("outcome purpose anchor content is invalid")
    bindings = {
        (item.get("sourcePath"), item.get("sha256"))
        for item in evidence or []
        if isinstance(item, dict)
    }
    for anchor in anchors:
        if (
            not isinstance(anchor, dict)
            or not isinstance(anchor.get("sourcePath"), str)
            or not _sha256(anchor.get("sha256"))
            or not isinstance(anchor.get("phrase"), str)
            or not anchor["phrase"]
            or anchor.get("untrusted") is not True
            or not isinstance(anchor.get("outcomeTerms"), list)
            or not anchor["outcomeTerms"]
            or anchor["outcomeTerms"] != sorted(set(anchor["outcomeTerms"]))
            or any(term in mechanics for term in anchor["outcomeTerms"])
        ):
            raise ValueError("outcome purpose anchor content is invalid")
        if evidence is not None and (anchor["sourcePath"], anchor["sha256"]) not in bindings:
            raise ValueError("outcome purpose anchor evidence binding is stale")
    if profile is not None and record["profileSha256"] != profile.get("profileSha256"):
        raise ValueError("outcome purpose anchor profile binding is stale")


def assess_purpose_specificity(record: dict[str, Any], purpose_text: str) -> str:
    """Return specific, missing_anchor, or mechanics_only for one purpose claim set."""
    validate_outcome_purpose_anchors(record)
    purpose_terms = {term for term in _tokens(purpose_text) if term not in STOP_TERMS}
    mechanics = set(record["mechanicsTerms"])
    meaningful = purpose_terms - mechanics
    if purpose_terms and not meaningful:
        return "mechanics_only"
    anchored = {term for anchor in record["anchors"] for term in anchor["outcomeTerms"]}
    return "specific" if meaningful & anchored else "missing_anchor"


def _identity_terms(profile: dict[str, Any]) -> set[str]:
    values = [
        profile.get("repository", {}).get("owner"),
        profile.get("repository", {}).get("name"),
        profile.get("package", {}).get("name"),
        profile.get("package", {}).get("targetLabel"),
        profile.get("package", {}).get("candidateId"),
    ]
    return {token for value in values if isinstance(value, str) for token in _tokens(value)}


def _technology_terms(profile: dict[str, Any]) -> set[str]:
    return {
        token
        for group in ("languages", "ecosystems", "analyzerSignals")
        for item in profile.get("technology", {}).get(group, [])
        for value in ([item.get("id")] if isinstance(item, dict) else [item])
        if isinstance(value, str)
        for token in _tokens(value)
    }


def _tokens(value: str) -> list[str]:
    return WORD_PATTERN.findall(value.casefold())


def _sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _digest_without(value: dict[str, Any], key: str) -> str:
    return hashlib.sha256(
        json.dumps(
            {name: item for name, item in value.items() if name != key},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
