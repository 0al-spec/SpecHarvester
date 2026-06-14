from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatchcase
from typing import Any

PYTHON_WEB_FRAMEWORK_PROFILE_ID = "python.web_framework.v0"


@dataclass(frozen=True)
class RepositoryParsingDecision:
    profile_id: str
    path: str
    role: str
    matched_rule_id: str
    reason_codes: tuple[str, ...]
    public_interface_eligible: bool
    semantic_usage_eligible: bool
    subrole: str | None = None

    def to_record(self) -> dict[str, Any]:
        record: dict[str, Any] = {
            "apiVersion": "spec-harvester.repository-parsing-plugin/v0",
            "kind": "SpecHarvesterRepositoryParsingPluginDecision",
            "authority": "producer_path_classification_only",
            "profileId": self.profile_id,
            "path": self.path,
            "role": self.role,
            "matchedRuleId": self.matched_rule_id,
            "reasonCodes": list(self.reason_codes),
            "publicInterfaceEligible": self.public_interface_eligible,
            "semanticUsageEligible": self.semantic_usage_eligible,
        }
        if self.subrole is not None:
            record["subrole"] = self.subrole
        return record


@dataclass(frozen=True)
class RepositoryParsingRule:
    id: str
    match: dict[str, Any]
    role: str
    reason_codes: tuple[str, ...]
    public_interface_eligible: bool
    semantic_usage_eligible: bool
    subrole: str | None = None

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> RepositoryParsingRule:
        return cls(
            id=str(record["id"]),
            match=dict(record.get("match") or {}),
            role=str(record["role"]),
            reason_codes=tuple(str(item) for item in record.get("reasonCodes", [])),
            public_interface_eligible=bool(record.get("publicInterfaceEligible")),
            semantic_usage_eligible=bool(record.get("semanticUsageEligible")),
            subrole=optional_string(record.get("subrole")),
        )

    def matches(self, path: str) -> bool:
        prefixes = tuple(str(item) for item in self.match.get("pathPrefixes", []))
        if prefixes and not any(path.startswith(prefix) for prefix in prefixes):
            return False

        extensions = tuple(str(item) for item in self.match.get("fileExtensions", []))
        if extensions and not path.endswith(extensions):
            return False

        filename_patterns = tuple(str(item) for item in self.match.get("filenamePatterns", []))
        if filename_patterns and not any(
            fnmatchcase(path_name(path), item) for item in filename_patterns
        ):
            return False

        segments = tuple(str(item) for item in self.match.get("pathSegments", []))
        if segments and not any(segment in path.split("/") for segment in segments):
            return False

        return True


@dataclass(frozen=True)
class RepositoryParsingProfile:
    id: str
    rules: tuple[RepositoryParsingRule, ...]
    fallback: RepositoryParsingRule

    def classify(self, path: str) -> RepositoryParsingDecision:
        normalized_path = normalize_path(path)
        matched_rules = [rule for rule in self.rules if rule.matches(normalized_path)]
        if matched_rules:
            rule = sorted(matched_rules, key=rule_precedence_key)[0]
            return decision_from_rule(self.id, normalized_path, rule)
        return decision_from_rule(self.id, normalized_path, self.fallback)


def repository_parsing_profile(profile_id: str | None) -> RepositoryParsingProfile | None:
    if profile_id is None or not profile_id.strip():
        return None
    if profile_id != PYTHON_WEB_FRAMEWORK_PROFILE_ID:
        raise ValueError(f"Unsupported repository parsing profile: {profile_id}")
    return python_web_framework_profile()


def python_web_framework_profile() -> RepositoryParsingProfile:
    return RepositoryParsingProfile(
        id=PYTHON_WEB_FRAMEWORK_PROFILE_ID,
        rules=tuple(
            RepositoryParsingRule.from_record(record) for record in PYTHON_WEB_FRAMEWORK_RULES
        ),
        fallback=RepositoryParsingRule.from_record(PYTHON_WEB_FRAMEWORK_FALLBACK),
    )


def decision_from_rule(
    profile_id: str,
    path: str,
    rule: RepositoryParsingRule,
) -> RepositoryParsingDecision:
    return RepositoryParsingDecision(
        profile_id=profile_id,
        path=path,
        role=rule.role,
        matched_rule_id=rule.id,
        reason_codes=rule.reason_codes,
        public_interface_eligible=rule.public_interface_eligible,
        semantic_usage_eligible=rule.semantic_usage_eligible,
        subrole=rule.subrole,
    )


def rule_precedence_key(rule: RepositoryParsingRule) -> tuple[int, str]:
    if not rule.public_interface_eligible and (
        rule.match.get("pathSegments") or rule.match.get("filenamePatterns")
    ):
        return (0, rule.id)
    return (1, rule.id)


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("/")


def path_name(path: str) -> str:
    return path.rsplit("/", 1)[-1]


def optional_string(value: Any) -> str | None:
    return value if isinstance(value, str) and value.strip() else None


PYTHON_WEB_FRAMEWORK_RULES: tuple[dict[str, Any], ...] = (
    {
        "id": "python_package_root_public_interface",
        "match": {"pathPrefixes": ["fastapi/"], "fileExtensions": [".py"]},
        "role": "public_interface",
        "reasonCodes": ["python_package_root", "consumer_facing_api_surface"],
        "publicInterfaceEligible": True,
        "semanticUsageEligible": False,
    },
    {
        "id": "docs_src_semantic_usage",
        "match": {"pathPrefixes": ["docs_src/"], "fileExtensions": [".py", ".md", ".rst"]},
        "role": "semantic_usage",
        "subrole": "example",
        "reasonCodes": ["documentation_example", "not_package_root"],
        "publicInterfaceEligible": False,
        "semanticUsageEligible": True,
    },
    {
        "id": "docs_semantic_usage",
        "match": {"pathPrefixes": ["docs/"]},
        "role": "documentation",
        "reasonCodes": ["documentation", "semantic_context"],
        "publicInterfaceEligible": False,
        "semanticUsageEligible": True,
    },
    {
        "id": "examples_semantic_usage",
        "match": {"pathPrefixes": ["examples/", "example/"]},
        "role": "example",
        "reasonCodes": ["example_code", "semantic_context"],
        "publicInterfaceEligible": False,
        "semanticUsageEligible": True,
    },
    {
        "id": "tests_not_public_interface",
        "match": {
            "pathPrefixes": ["tests/", "test/"],
            "filenamePatterns": ["test_*.py", "*_test.py"],
        },
        "role": "test",
        "reasonCodes": ["test_fixture", "not_public_api"],
        "publicInterfaceEligible": False,
        "semanticUsageEligible": False,
    },
    {
        "id": "generated_artifacts_not_public_interface",
        "match": {
            "pathPrefixes": ["build/", "dist/", "site/"],
            "filenamePatterns": ["*.generated.py", "*_pb2.py"],
        },
        "role": "generated",
        "reasonCodes": ["generated_artifact", "provenance_required"],
        "publicInterfaceEligible": False,
        "semanticUsageEligible": False,
    },
    {
        "id": "repository_tooling_not_public_interface",
        "match": {"pathPrefixes": [".github/", "scripts/", "tools/"]},
        "role": "tooling",
        "reasonCodes": ["repository_tooling", "not_public_api"],
        "publicInterfaceEligible": False,
        "semanticUsageEligible": False,
    },
    {
        "id": "private_python_modules_internal",
        "match": {"pathSegments": ["__pycache__", "_internal", "_private"]},
        "role": "internal",
        "reasonCodes": ["internal_implementation", "not_public_api"],
        "publicInterfaceEligible": False,
        "semanticUsageEligible": False,
    },
)

PYTHON_WEB_FRAMEWORK_FALLBACK: dict[str, Any] = {
    "id": "conservative_default_fallback",
    "match": {},
    "role": "semantic_usage",
    "reasonCodes": [
        "unmatched_python_web_framework_path",
        "conservative_non_public_interface_default",
    ],
    "publicInterfaceEligible": False,
    "semanticUsageEligible": True,
}
