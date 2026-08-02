from __future__ import annotations

import hashlib
import json
import re
from typing import Any

ANCHOR_API_VERSION = "spec-harvester.outcome-purpose-anchors/v0"
ANCHOR_KIND = "SpecHarvesterOutcomePurposeAnchors"
SOURCE_AUTHORITY_POLICY = "p55-t10g4-outcome-anchor-source-authority/v1"

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
    "boundary",
    "cli",
    "codebase",
    "command",
    "component",
    "dependency",
    "discover",
    "discovery",
    "ecosystem",
    "framework",
    "generate",
    "generated",
    "generating",
    "implementation",
    "import",
    "interface",
    "library",
    "line",
    "manifest",
    "member",
    "metadata",
    "module",
    "modules",
    "package",
    "plugin",
    "preview",
    "previews",
    "project",
    "repository",
    "runtime",
    "sdk",
    "source",
    "stack",
    "tool",
    "toolkit",
}

SOURCE_AUTHORITY_RANKS = {
    "descriptive_manifest": 3,
    "package_local_documentation": 3,
    "repository_documentation": 2,
    "generated_candidate_preview": 0,
    "generated_preview_mechanics": 0,
    "member_package_boundary_mechanics": 0,
    "import_mechanics": 0,
    "discovery_mechanics": 0,
    "module_mechanics": 0,
    "unclassified_documentation": 0,
    "legacy_unclassified": 0,
}
MECHANICS_SOURCE_AUTHORITIES = frozenset(
    authority for authority, rank in SOURCE_AUTHORITY_RANKS.items() if rank == 0
)
PHRASE_MECHANICS = (
    ("generated_preview_mechanics", re.compile(r"\bgenerated\s+preview\b", re.IGNORECASE)),
    (
        "member_package_boundary_mechanics",
        re.compile(r"\bmember(?:\s+package)?\s+boundary\b", re.IGNORECASE),
    ),
    ("import_mechanics", re.compile(r"\bimports?\b", re.IGNORECASE)),
    ("discovery_mechanics", re.compile(r"\bdiscover(?:y|ed|ing)?\b", re.IGNORECASE)),
    ("module_mechanics", re.compile(r"\bmodules?\b", re.IGNORECASE)),
)


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
    candidates: list[tuple[str, str, str, str]] = []
    description = profile.get("package", {}).get("description")
    if isinstance(description, str) and description.strip():
        candidates.append(
            (
                "semantic-product-profile.json",
                str(profile_evidence["sha256"]),
                description.strip(),
                _description_source_authority(profile),
            )
        )
    document_roles = {
        (item.get("evidencePath"), item.get("sha256")): item.get("role")
        for item in profile.get("documents", [])
        if isinstance(item, dict)
    }
    for document in profile.get("documents", []):
        if not isinstance(document, dict):
            continue
        item = evidence_by_path.get(document.get("evidencePath"))
        if not isinstance(item, dict) or item.get("sha256") != document.get("sha256"):
            continue
        source_authority = _document_source_authority(
            document_roles.get((document.get("evidencePath"), document.get("sha256")))
        )
        for match in SENTENCE_PATTERN.finditer(str(item["content"])):
            phrase = " ".join(match.group().split())
            if 20 <= len(phrase) <= 360:
                candidates.append(
                    (str(item["sourcePath"]), str(item["sha256"]), phrase, source_authority)
                )
            if len(candidates) >= 24:
                break

    anchors: list[dict[str, Any]] = []
    seen_phrases: set[str] = set()
    for source_path, sha256, phrase, source_authority in candidates:
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
                "sourceAuthority": _phrase_source_authority(phrase, source_authority),
                "untrusted": True,
            }
        )
        if len(anchors) == 8:
            break

    record = {
        "apiVersion": ANCHOR_API_VERSION,
        "kind": ANCHOR_KIND,
        "schemaVersion": 2,
        "authority": "deterministic_untrusted_outcome_guidance",
        "sourceAuthorityPolicy": SOURCE_AUTHORITY_POLICY,
        "candidateId": candidate_id,
        "sourceBundleSha256": source_bundle_sha256,
        "profileSha256": profile_sha256,
        "anchors": anchors,
        "sourceAuthorityState": _source_authority_state(anchors),
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
        or record.get("schemaVersion") not in {1, 2}
        or record.get("authority") != "deterministic_untrusted_outcome_guidance"
        or not isinstance(record.get("candidateId"), str)
        or not _sha256(record.get("sourceBundleSha256"))
        or not _sha256(record.get("profileSha256"))
        or record.get("anchorsSha256") != _digest_without(record, "anchorsSha256")
    ):
        raise ValueError("outcome purpose anchor record is invalid")
    anchors = record.get("anchors")
    mechanics = record.get("mechanicsTerms")
    schema_version = record["schemaVersion"]
    if (
        not isinstance(anchors, list)
        or len(anchors) > 8
        or not isinstance(mechanics, list)
        or mechanics != sorted(set(mechanics))
        or not all(isinstance(term, str) and term for term in mechanics)
    ):
        raise ValueError("outcome purpose anchor content is invalid")
    if schema_version == 2 and record.get("sourceAuthorityPolicy") != SOURCE_AUTHORITY_POLICY:
        raise ValueError("outcome purpose anchor authority policy is invalid")
    if schema_version == 2 and record.get("sourceAuthorityState") != _source_authority_state(
        anchors
    ):
        raise ValueError("outcome purpose anchor authority state is invalid")
    bindings = {
        (item.get("sourcePath"), item.get("sha256")): item.get("content")
        for item in evidence or []
        if isinstance(item, dict) and isinstance(item.get("content"), str)
    }
    bound_profile = profile or _profile_from_evidence(record, evidence)
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
            or (schema_version == 2 and anchor.get("sourceAuthority") not in SOURCE_AUTHORITY_RANKS)
        ):
            raise ValueError("outcome purpose anchor content is invalid")
        if evidence is not None:
            content = bindings.get((anchor["sourcePath"], anchor["sha256"]))
            if content is None:
                raise ValueError("outcome purpose anchor evidence binding is stale")
            if (
                " ".join(anchor["phrase"].split()).casefold()
                not in " ".join(content.split()).casefold()
            ):
                raise ValueError("outcome purpose anchor phrase is not present in bound evidence")
            expected_terms = sorted(
                token
                for token in set(_tokens(anchor["phrase"]))
                if len(token) >= 3 and token not in STOP_TERMS and token not in mechanics
            )[:16]
            if anchor["outcomeTerms"] != expected_terms:
                raise ValueError("outcome purpose anchor terms do not match bound phrase")
        if schema_version == 2 and bound_profile is not None:
            if anchor["sourceAuthority"] != _expected_source_authority(bound_profile, anchor):
                raise ValueError("outcome purpose anchor source authority is stale")
    if bound_profile is not None and record["profileSha256"] != bound_profile.get("profileSha256"):
        raise ValueError("outcome purpose anchor profile binding is stale")


def assess_purpose_specificity(record: dict[str, Any], purpose_text: str) -> str:
    """Return specific, weak_source_only, missing_anchor, or mechanics_only."""
    validate_outcome_purpose_anchors(record)
    purpose_terms = {term for term in _tokens(purpose_text) if term not in STOP_TERMS}
    mechanics = set(record["mechanicsTerms"])
    meaningful = purpose_terms - mechanics
    if purpose_terms and not meaningful:
        return "mechanics_only"
    if not record["anchors"]:
        return "no_outcome_source"
    strong_anchored = {
        term
        for anchor in record["anchors"]
        if _source_authority_rank(anchor, record["schemaVersion"]) > 0
        for term in anchor["outcomeTerms"]
    }
    if meaningful & strong_anchored:
        return "specific"
    if record["schemaVersion"] == 1:
        return "legacy_unclassified"
    weak_anchored = {
        term
        for anchor in record["anchors"]
        if _source_authority_rank(anchor, record["schemaVersion"]) == 0
        for term in anchor["outcomeTerms"]
    }
    return "weak_source_only" if meaningful & weak_anchored else "missing_anchor"


def has_strong_outcome_anchors(record: dict[str, Any]) -> bool:
    """Return whether a validated anchor record has at least one strong source."""
    validate_outcome_purpose_anchors(record)
    return any(
        _source_authority_rank(anchor, record["schemaVersion"]) > 0 for anchor in record["anchors"]
    )


def _description_source_authority(profile: dict[str, Any]) -> str:
    package = profile.get("package", {})
    provenance = package.get("descriptionProvenance") if isinstance(package, dict) else None
    if (
        isinstance(package, dict)
        and isinstance(provenance, dict)
        and provenance.get("sourcePath") == package.get("manifestPath")
        and provenance.get("sha256") == package.get("manifestSha256")
        and provenance.get("field") == "description"
        and provenance.get("extractor") == "pinned_manifest_metadata/v1"
        and provenance.get("normalizedValueSha256")
        == hashlib.sha256(str(package.get("description") or "").strip().encode()).hexdigest()
    ):
        return "descriptive_manifest"
    return "generated_candidate_preview"


def _document_source_authority(role: Any) -> str:
    if role == "package_local":
        return "package_local_documentation"
    if role == "repository_root":
        return "repository_documentation"
    return "unclassified_documentation"


def _phrase_source_authority(phrase: str, source_authority: str) -> str:
    for mechanics_authority, pattern in PHRASE_MECHANICS:
        if pattern.search(phrase):
            return mechanics_authority
    return source_authority


def _source_authority_rank(anchor: dict[str, Any], schema_version: int) -> int:
    authority = anchor.get("sourceAuthority") if schema_version == 2 else "legacy_unclassified"
    return SOURCE_AUTHORITY_RANKS.get(authority, 0)


def _source_authority_state(anchors: list[dict[str, Any]]) -> str:
    if any(SOURCE_AUTHORITY_RANKS.get(anchor.get("sourceAuthority"), 0) > 0 for anchor in anchors):
        return "strong_anchor_available"
    if anchors:
        return "weak_only"
    return "no_outcome_source"


def _profile_from_evidence(
    record: dict[str, Any], evidence: list[dict[str, Any]] | None
) -> dict[str, Any] | None:
    for item in evidence or []:
        if not isinstance(item, dict) or item.get("sourcePath") != "semantic-product-profile.json":
            continue
        try:
            profile = json.loads(item.get("content", ""))
        except (TypeError, json.JSONDecodeError):
            return None
        if isinstance(profile, dict) and profile.get("profileSha256") == record["profileSha256"]:
            return profile
    return None


def _expected_source_authority(profile: dict[str, Any], anchor: dict[str, Any]) -> str:
    if anchor["sourcePath"] == "semantic-product-profile.json":
        source_authority = _description_source_authority(profile)
    else:
        source_authority = _document_source_authority(
            next(
                (
                    document.get("role")
                    for document in profile.get("documents", [])
                    if isinstance(document, dict)
                    and document.get("evidencePath") == anchor["sourcePath"]
                    and document.get("sha256") == anchor["sha256"]
                ),
                None,
            )
        )
    return _phrase_source_authority(anchor["phrase"], source_authority)


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
