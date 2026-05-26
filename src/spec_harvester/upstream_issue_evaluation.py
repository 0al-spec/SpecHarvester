from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

UPSTREAM_REPOSITORY_ARTIFACT_ID = "upstream_repository"
MISSING_UPSTREAM_REPOSITORY = "missing_upstream_repository"
DUPLICATE_UPSTREAM_REPOSITORY_ENTRIES = "duplicate_upstream_repository_entries"
INVALID_UPSTREAM_REPOSITORY_URI = "invalid_upstream_repository_uri"
UPSTREAM_NAMESPACE_MISMATCH = "upstream_namespace_mismatch"
NON_GITHUB_UPSTREAM_REPOSITORY = "non_github_upstream_repository"


@dataclass(frozen=True)
class UpstreamArtifactEvidence:
    artifact_id: str
    uri: str


@dataclass(frozen=True)
class UpstreamRepositoryReference:
    owner: str
    name: str


@dataclass(frozen=True)
class UpstreamIssueSubject:
    path: str
    package_id: str
    package_version: str
    namespace: str
    artifacts: tuple[UpstreamArtifactEvidence, ...]


@dataclass(frozen=True)
class UpstreamIssuePolicy:
    missing_message: str
    severity_by_code: tuple[tuple[str, str], ...] = ()
    report_non_github: bool = False

    def evaluate(self, subjects: Iterable[UpstreamIssueSubject]) -> list[dict[str, str]]:
        issues: list[dict[str, str]] = []
        for subject in subjects:
            issues.extend(self.evaluate_subject(subject))
        return sorted(issues, key=lambda item: (item["path"], item["code"]))

    def evaluate_subject(self, subject: UpstreamIssueSubject) -> list[dict[str, str]]:
        issues: list[dict[str, str]] = []
        upstream_entries = [
            entry
            for entry in subject.artifacts
            if entry.artifact_id == UPSTREAM_REPOSITORY_ARTIFACT_ID
        ]
        if not upstream_entries:
            return [self.issue(subject, MISSING_UPSTREAM_REPOSITORY, self.missing_message)]

        if len(upstream_entries) > 1:
            issues.append(
                self.issue(
                    subject,
                    DUPLICATE_UPSTREAM_REPOSITORY_ENTRIES,
                    "Multiple upstream_repository artifacts found.",
                )
            )

        for entry in upstream_entries:
            issues.extend(self.evaluate_entry(subject, entry))
        return issues

    def evaluate_entry(
        self,
        subject: UpstreamIssueSubject,
        entry: UpstreamArtifactEvidence,
    ) -> list[dict[str, str]]:
        if not entry.uri:
            return [
                self.issue(
                    subject,
                    INVALID_UPSTREAM_REPOSITORY_URI,
                    "upstream_repository artifact missing URI.",
                )
            ]

        upstream = parse_upstream_repository_reference(entry.uri)
        if upstream is None:
            return [self.invalid_upstream_uri_issue(subject, entry.uri)]

        issues: list[dict[str, str]] = []
        if not namespace_matches_upstream(subject.namespace, upstream):
            issues.append(
                self.issue(
                    subject,
                    UPSTREAM_NAMESPACE_MISMATCH,
                    (
                        f"Package namespace `{subject.namespace}` does not match inferred "
                        f"upstream owner `{upstream.owner}` or repository `{upstream.name}`."
                    ),
                )
            )

        if self.report_non_github and "github.com" not in entry.uri.lower():
            issues.append(
                self.issue(
                    subject,
                    NON_GITHUB_UPSTREAM_REPOSITORY,
                    f"Upstream URI is not a GitHub source: {entry.uri}",
                )
            )
        return issues

    def invalid_upstream_uri_issue(
        self,
        subject: UpstreamIssueSubject,
        uri: str,
    ) -> dict[str, str]:
        if self.report_non_github and "github.com" not in uri.lower():
            return self.issue(
                subject,
                NON_GITHUB_UPSTREAM_REPOSITORY,
                f"Upstream URI is not a GitHub source: {uri}",
            )
        return self.issue(
            subject,
            INVALID_UPSTREAM_REPOSITORY_URI,
            f"Could not parse upstream owner from URI: {uri}",
        )

    def issue(self, subject: UpstreamIssueSubject, code: str, message: str) -> dict[str, str]:
        issue = {
            "path": subject.path,
            "packageId": subject.package_id,
            "packageVersion": subject.package_version,
            "code": code,
            "message": message,
        }
        severity = self.severity_for(code)
        if severity is not None:
            issue["severity"] = severity
        return issue

    def severity_for(self, code: str) -> str | None:
        for issue_code, severity in self.severity_by_code:
            if issue_code == code:
                return severity
        return None


def upstream_issue_subject(
    *,
    path: str,
    package_id: str,
    package_version: str,
    namespace: str,
    artifacts: Iterable[Any],
) -> UpstreamIssueSubject:
    return UpstreamIssueSubject(
        path=path,
        package_id=package_id,
        package_version=package_version,
        namespace=namespace,
        artifacts=tuple(
            UpstreamArtifactEvidence(
                artifact_id=str(getattr(artifact, "artifact_id", "")),
                uri=str(getattr(artifact, "uri", "")),
            )
            for artifact in artifacts
        ),
    )


def upstream_issue_subjects(records: Iterable[Any]) -> tuple[UpstreamIssueSubject, ...]:
    return tuple(
        upstream_issue_subject(
            path=str(getattr(record, "path", "")),
            package_id=str(getattr(record, "package_id", "")),
            package_version=str(getattr(record, "package_version", "")),
            namespace=str(getattr(record, "namespace", "")),
            artifacts=getattr(record, "upstream_artifacts", ()),
        )
        for record in records
    )


def namespace_matches_upstream(namespace: str, upstream: UpstreamRepositoryReference) -> bool:
    normalized_namespace = normalized_identifier_key(namespace)
    if not normalized_namespace:
        return False
    return normalized_namespace in {
        normalized_identifier_key(upstream.owner),
        normalized_identifier_key(upstream.name),
    }


def normalized_identifier_key(value: str) -> str:
    return "".join(character.casefold() for character in value.strip() if character.isalnum())


def parse_upstream_owner(uri: str) -> str | None:
    upstream = parse_upstream_repository_reference(uri)
    if upstream is None:
        return None
    return upstream.owner


def parse_upstream_repository_reference(uri: str) -> UpstreamRepositoryReference | None:
    text = uri.strip().strip("'\"")
    if text.startswith("git@github.com:"):
        body = text.removeprefix("git@github.com:")
        parts = body.strip("/").split("/")
    elif text.startswith("https://github.com/") or text.startswith("http://github.com/"):
        parsed = urlparse(text)
        parts = parsed.path.strip("/").split("/")
    else:
        return None

    if len(parts) < 2 or not parts[0] or not parts[1]:
        return None
    repository_name = strip_git_suffix(parts[1])
    if not repository_name:
        return None
    return UpstreamRepositoryReference(owner=parts[0], name=repository_name)


def strip_git_suffix(name: str) -> str:
    if name.endswith(".git"):
        return name.removesuffix(".git")
    return name
