from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.batch_collection import BatchCollectOptions, collect_batch_snapshots
from spec_harvester.bundle_set_preflight import BundleSetPreflightOptions, run_bundle_set_preflight
from spec_harvester.package_set_drafter import PackageSetDraftOptions, draft_package_set
from spec_harvester.static_spec_renderer import write_static_package_set_site

XYFLOW_PACKAGE_SET_SMOKE_API_VERSION = "spec-harvester.xyflow-package-set-smoke/v0"
XYFLOW_PACKAGE_SET_SMOKE_KIND = "SpecHarvesterXyflowPackageSetSmokeReport"
XYFLOW_PACKAGE_SET_SMOKE_SCHEMA_VERSION = 1
XYFLOW_REPOSITORY = "https://github.com/xyflow/xyflow"
XYFLOW_REVISION = "abc123"
EXPECTED_PACKAGE_IDS = (
    "xyflow.workspace",
    "xyflow.system",
    "xyflow.react",
    "xyflow.svelte",
)
EXPECTED_RELATIONS = (
    ("xyflow.workspace", "contains", "xyflow.react"),
    ("xyflow.workspace", "contains", "xyflow.svelte"),
    ("xyflow.workspace", "contains", "xyflow.system"),
)


@dataclass(frozen=True)
class XyflowPackageSetSmokeOptions:
    output: Path


def run_xyflow_package_set_smoke(options: XyflowPackageSetSmokeOptions) -> dict[str, Any]:
    output = options.output
    ensure_empty_output(output)
    fixture_root = output / "fixture" / "xyflow"
    inputs = output / "inputs"
    candidates_root = output / "candidates"
    package_set_root = output / "package-set"
    viewer_root = output / "viewer"
    report_path = output / "xyflow-package-set-smoke.json"

    inputs.mkdir(parents=True)
    write_xyflow_fixture_checkout(fixture_root)
    write_xyflow_source_manifest(inputs / "repositories.yml", fixture_root, inputs)
    collection = collect_batch_snapshots(
        BatchCollectOptions(
            inputs=inputs,
            out=candidates_root,
            emit_workspace_inventory=True,
        )
    )
    inventory_path = candidates_root / "xyflow" / "workspace-inventory.json"
    draft = draft_package_set(
        PackageSetDraftOptions(
            inventory=inventory_path,
            out=package_set_root,
        )
    )
    preflight = run_bundle_set_preflight(BundleSetPreflightOptions(bundle_set=package_set_root))
    (package_set_root / "bundle-set-preflight.json").write_text(
        json.dumps(preflight, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    viewer = write_static_package_set_site(package_set_root, viewer_root)
    package_set = read_json(package_set_root / "package-set-draft.json")
    relation_payload = read_json(package_set_root / "package-relation-proposals.json")
    rendered = read_json(viewer_root / "package-set.json")

    report = smoke_report(
        output=output,
        collection=collection,
        draft=draft,
        preflight=preflight,
        viewer=viewer,
        package_set=package_set,
        relation_payload=relation_payload,
        rendered=rendered,
        artifacts={
            "sourceManifest": inputs / "repositories.yml",
            "workspaceInventory": inventory_path,
            "packageSetDraft": package_set_root / "package-set-draft.json",
            "relationProposals": package_set_root / "package-relation-proposals.json",
            "bundleSetPreflight": package_set_root / "bundle-set-preflight.json",
            "viewerPayload": viewer_root / "package-set.json",
            "viewerIndex": viewer_root / "index.html",
        },
    )
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def smoke_report(
    *,
    output: Path,
    collection: dict[str, Any],
    draft: dict[str, Any],
    preflight: dict[str, Any],
    viewer: dict[str, Any],
    package_set: dict[str, Any],
    relation_payload: dict[str, Any],
    rendered: dict[str, Any],
    artifacts: dict[str, Path],
) -> dict[str, Any]:
    package_ids = sorted(
        item["packageId"]
        for item in package_set.get("candidates", [])
        if isinstance(item, dict) and isinstance(item.get("packageId"), str)
    )
    relations = relation_summary(relation_payload)
    expected_relation_records = [
        {"source": source, "type": relation_type, "target": target}
        for source, relation_type, target in EXPECTED_RELATIONS
    ]
    status = (
        "passed"
        if smoke_passed(collection, draft, preflight, viewer, package_ids, relations)
        else "failed"
    )
    return {
        "apiVersion": XYFLOW_PACKAGE_SET_SMOKE_API_VERSION,
        "kind": XYFLOW_PACKAGE_SET_SMOKE_KIND,
        "schemaVersion": XYFLOW_PACKAGE_SET_SMOKE_SCHEMA_VERSION,
        "status": status,
        "output": str(output),
        "source": {
            "repository": XYFLOW_REPOSITORY,
            "revision": XYFLOW_REVISION,
            "fixture": "synthetic_local_checkout",
        },
        "artifacts": {key: str(path) for key, path in artifacts.items()},
        "packageSet": {
            "id": rendered.get("packageSet", {}).get("id"),
            "candidateCount": len(package_ids),
            "packageIds": package_ids,
            "skippedPackageIds": sorted(
                item["packageId"]
                for item in package_set.get("skipped", [])
                if isinstance(item, dict) and isinstance(item.get("packageId"), str)
            ),
        },
        "relations": relations,
        "expectedRelations": expected_relation_records,
        "preflight": {
            "status": preflight.get("status"),
            "summary": preflight.get("summary"),
        },
        "viewer": {
            "status": viewer.get("status"),
            "packageSetId": viewer.get("packageSetId"),
            "written": viewer.get("written", []),
            "payloadKind": rendered.get("kind"),
        },
        "executionBoundary": {
            "network": "none",
            "packageScripts": "not_run",
            "packageManagers": "not_run",
            "builds": "not_run",
            "tests": "not_run",
            "prompts": "not_run",
        },
    }


def smoke_passed(
    collection: dict[str, Any],
    draft: dict[str, Any],
    preflight: dict[str, Any],
    viewer: dict[str, Any],
    package_ids: list[str],
    relations: list[dict[str, str]],
) -> bool:
    relation_tuples = {(item["source"], item["type"], item["target"]) for item in relations}
    return (
        collection.get("status") == "ok"
        and draft.get("status") == "ok"
        and preflight.get("status") == "passed"
        and viewer.get("status") == "ok"
        and set(package_ids) == set(EXPECTED_PACKAGE_IDS)
        and relation_tuples == set(EXPECTED_RELATIONS)
    )


def relation_summary(payload: dict[str, Any]) -> list[dict[str, str]]:
    records = payload.get("relations")
    if not isinstance(records, list):
        return []
    result = []
    for relation in records:
        if not isinstance(relation, dict):
            continue
        source = relation_endpoint_package_id(relation.get("source"))
        target = relation_endpoint_package_id(relation.get("target"))
        relation_type = relation.get("type")
        review_status = relation.get("reviewStatus")
        if not all(isinstance(value, str) for value in (source, target, relation_type)):
            continue
        result.append(
            {
                "source": source,
                "type": relation_type,
                "target": target,
                "reviewStatus": review_status if isinstance(review_status, str) else "",
            }
        )
    return sorted(result, key=lambda item: (item["source"], item["type"], item["target"]))


def relation_endpoint_package_id(endpoint: Any) -> str | None:
    if not isinstance(endpoint, dict):
        return None
    package_id = endpoint.get("packageId")
    return package_id if isinstance(package_id, str) else None


def ensure_empty_output(output: Path) -> None:
    if output.exists() and not output.is_dir():
        raise ValueError(f"Smoke output path is not a directory: {output}")
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"Smoke output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)


def write_xyflow_source_manifest(path: Path, checkout: Path, inputs_root: Path) -> None:
    path.write_text(
        f"""
repositories:
  - id: xyflow
    repository: {XYFLOW_REPOSITORY}
    revision: {XYFLOW_REVISION}
    checkout: {relative_to(checkout, inputs_root)}
    packageId: xyflow.workspace
""",
        encoding="utf-8",
    )


def write_xyflow_fixture_checkout(path: Path) -> None:
    path.mkdir(parents=True)
    (path / "README.md").write_text(
        "# Xyflow\n\nMonorepo for React Flow and Svelte Flow packages.\n",
        encoding="utf-8",
    )
    (path / "package.json").write_text(
        json.dumps(
            {
                "name": "@xyflow/monorepo",
                "version": "0.0.0",
                "private": True,
                "packageManager": "pnpm@9.2.0",
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    (path / "pnpm-lock.yaml").write_text("lockfileVersion: '9.0'\n", encoding="utf-8")
    (path / "pnpm-workspace.yaml").write_text(
        """
packages:
  - packages/*
  - examples/*
  - tooling/*
  - tests/*
  - "!**/test-fixtures/**"
""",
        encoding="utf-8",
    )
    packages = {
        "packages/system": {
            "name": "@xyflow/system",
            "version": "1.0.0",
            "description": "Core graph and viewport utilities for xyflow packages.",
        },
        "packages/react": {
            "name": "@xyflow/react",
            "version": "12.0.0",
            "description": "React package for node-based editors and flow diagrams.",
        },
        "packages/svelte": {
            "name": "@xyflow/svelte",
            "version": "1.0.0",
            "description": "Svelte package for node-based editors and flow diagrams.",
        },
        "examples/react": {"name": "react-examples", "version": "0.0.0"},
        "examples/svelte": {"name": "svelte-examples", "version": "0.0.0"},
        "tooling/cli": {"name": "@xyflow/cli", "version": "0.1.0"},
        "tests/e2e": {"name": "@xyflow/e2e", "version": "0.0.0"},
    }
    for relative, payload in packages.items():
        package_dir = path / relative
        package_dir.mkdir(parents=True)
        (package_dir / "package.json").write_text(
            json.dumps(payload, sort_keys=True),
            encoding="utf-8",
        )


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return payload


def relative_to(path: Path, root: Path) -> str:
    return Path(os.path.relpath(path, root)).as_posix()
