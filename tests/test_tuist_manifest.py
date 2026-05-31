from __future__ import annotations

import json
import textwrap

from spec_harvester.tuist_manifest import parse_tuist_manifest


def test_parse_tuist_project_manifest_extracts_project_and_targets() -> None:
    payload = parse_tuist_manifest(
        textwrap.dedent(
            """
            import ProjectDescription

            let project = Project(
                name: "Player",
                targets: [
                    .target(
                        name: "PlayerKit",
                        destinations: [.iPhone, .iPad],
                        product: .framework,
                        bundleId: "dev.spec.player",
                        sources: ["Sources/**", "Generated/**/*.swift"],
                        resources: .resources(["Resources/**"])
                    ),
                    .target(
                        name: "PlayerApp",
                        platform: .iOS,
                        product: .app,
                        sources: .glob("App/Sources/**")
                    )
                ]
            )
            """
        ),
        filename="Project.swift",
    )

    assert payload == {
        "ecosystem": "tuist",
        "language": "swift",
        "manifest": "project",
        "name": "Player",
        "targets": [
            {
                "name": "PlayerApp",
                "product": "app",
                "platforms": ["iOS"],
                "sources": ["App/Sources/**"],
            },
            {
                "name": "PlayerKit",
                "product": "framework",
                "platforms": ["iPad", "iPhone"],
                "sources": ["Generated/**/*.swift", "Sources/**"],
                "resources": ["Resources/**"],
            },
        ],
        "products": [
            {"name": "PlayerApp", "type": "app"},
            {"name": "PlayerKit", "type": "framework"},
        ],
        "sourceGlobs": ["App/Sources/**", "Generated/**/*.swift", "Sources/**"],
        "resourceGlobs": ["Resources/**"],
    }


def test_parse_tuist_workspace_manifest_extracts_projects() -> None:
    payload = parse_tuist_manifest(
        """
        import ProjectDescription

        let workspace = Workspace(
            name: "Mobile",
            projects: ["Apps/*", "Modules/Player"]
        )
        """,
        filename="Workspace.swift",
    )

    assert payload == {
        "ecosystem": "tuist",
        "language": "swift",
        "manifest": "workspace",
        "name": "Mobile",
        "projects": ["Apps/*", "Modules/Player"],
    }


def test_parse_tuist_manifest_ignores_comments_and_tolerates_partial_shapes() -> None:
    payload = parse_tuist_manifest(
        """
        // Project(name: "Commented")
        let project = Project(
            name: "Real",
            targets: [
                // .target(name: "CommentedTarget", product: .framework)
                .target(
                    name: "RealTarget",
                    deploymentTargets: .iOS("17.0"),
                    sources: SourceFilesList(globs: ["Sources/**"])
                )
            ]
        )
        """,
        filename="Project.swift",
    )

    assert payload is not None
    assert payload["name"] == "Real"
    assert payload["targets"] == [
        {
            "name": "RealTarget",
            "platforms": ["iOS"],
            "sources": ["Sources/**"],
        }
    ]
    assert "Commented" not in json.dumps(payload)


def test_parse_tuist_config_without_static_metadata_returns_none() -> None:
    assert parse_tuist_manifest("let config = Config()", filename="Tuist.swift") is None
