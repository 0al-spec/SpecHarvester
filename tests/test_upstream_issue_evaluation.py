from dataclasses import dataclass

from spec_harvester.upstream_issue_evaluation import (
    NON_GITHUB_UPSTREAM_REPOSITORY,
    UPSTREAM_NAMESPACE_MISMATCH,
    UpstreamArtifactEvidence,
    UpstreamIssuePolicy,
    namespace_matches_upstream,
    parse_upstream_owner,
    parse_upstream_repository_reference,
    upstream_issue_subjects,
)


@dataclass(frozen=True)
class DummyArtifact:
    artifact_id: str
    uri: str


@dataclass(frozen=True)
class DummyRecord:
    path: str
    package_id: str
    package_version: str
    namespace: str
    upstream_artifacts: tuple[DummyArtifact, ...]


def test_upstream_issue_subjects_map_report_records() -> None:
    subjects = upstream_issue_subjects(
        [
            DummyRecord(
                path="specpm.yaml",
                package_id="demo.core",
                package_version="1.0.0",
                namespace="demo",
                upstream_artifacts=(
                    DummyArtifact("upstream_repository", "https://github.com/demo/demo"),
                ),
            )
        ]
    )

    assert subjects[0].path == "specpm.yaml"
    assert subjects[0].artifacts == (
        UpstreamArtifactEvidence("upstream_repository", "https://github.com/demo/demo"),
    )


def test_upstream_issue_policy_reports_non_github_with_configured_severity() -> None:
    subject = upstream_issue_subjects(
        [
            DummyRecord(
                path="specpm.yaml",
                package_id="demo.core",
                package_version="1.0.0",
                namespace="demo",
                upstream_artifacts=(
                    DummyArtifact("upstream_repository", "https://gitlab.com/demo/demo"),
                ),
            )
        ]
    )[0]
    policy = UpstreamIssuePolicy(
        missing_message="missing",
        report_non_github=True,
        severity_by_code=((NON_GITHUB_UPSTREAM_REPOSITORY, "low"),),
    )

    assert policy.evaluate([subject]) == [
        {
            "path": "specpm.yaml",
            "packageId": "demo.core",
            "packageVersion": "1.0.0",
            "code": NON_GITHUB_UPSTREAM_REPOSITORY,
            "message": "Upstream URI is not a GitHub source: https://gitlab.com/demo/demo",
            "severity": "low",
        }
    ]


def test_upstream_repository_reference_parsing_and_namespace_matching() -> None:
    upstream = parse_upstream_repository_reference("git@github.com:SoundBlaster/xyflow.git")

    assert upstream is not None
    assert upstream.owner == "SoundBlaster"
    assert upstream.name == "xyflow"
    assert parse_upstream_owner("https://github.com/SoundBlaster/xyflow.git") == "SoundBlaster"
    assert namespace_matches_upstream("xy-flow", upstream)


def test_upstream_issue_policy_reports_namespace_mismatch() -> None:
    subject = upstream_issue_subjects(
        [
            DummyRecord(
                path="specpm.yaml",
                package_id="demo.core",
                package_version="1.0.0",
                namespace="other",
                upstream_artifacts=(
                    DummyArtifact("upstream_repository", "https://github.com/demo/demo"),
                ),
            )
        ]
    )[0]

    assert (
        UpstreamIssuePolicy(missing_message="missing").evaluate([subject])[0]["code"]
        == UPSTREAM_NAMESPACE_MISMATCH
    )
