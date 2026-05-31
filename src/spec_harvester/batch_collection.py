from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.analyzer_orchestration import (
    PUBLIC_INTERFACE_INDEX_FILENAME,
    interface_index_batch_record,
    run_project_profile_analyzers,
)
from spec_harvester.batch_validation import (
    build_batch_validation_report,
    write_batch_validation_report,
)
from spec_harvester.collector import (
    DEFAULT_MAX_FILE_BYTES,
    HarvestOptions,
    collect_local_repository,
)
from spec_harvester.interface_index import render_public_interface_index_json
from spec_harvester.source_manifest import read_repository_source_manifests

SAFE_REPOSITORY_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


@dataclass(frozen=True)
class BatchCollectOptions:
    inputs: Path
    out: Path
    selected_ids: tuple[str, ...] = ()
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES
    report: Path | None = None
    strict_public: bool = True
    emit_interface_indexes: bool = False
    analyzer_cache_dir: Path | None = None


def collect_batch_snapshots(options: BatchCollectOptions) -> dict[str, Any]:
    inputs_root = options.inputs.resolve()
    out_root = options.out
    repositories = read_repository_source_manifests(options.inputs)
    selected_ids = tuple(options.selected_ids)
    selected_set = set(selected_ids)
    if len(selected_set) != len(selected_ids):
        raise ValueError("Duplicate selected repository id")

    known_ids = {repository["id"] for repository in repositories}
    unknown_ids = sorted(selected_set - known_ids)
    if unknown_ids:
        raise ValueError(f"Unknown selected repository id: {', '.join(unknown_ids)}")

    plans: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for repository in repositories:
        repository_id = repository["id"]
        if selected_set and repository_id not in selected_set:
            skipped.append({"id": repository_id, "reason": "not_selected"})
            continue

        output_dir = candidate_directory(out_root, repository_id)
        checkout = resolve_checkout(inputs_root, repository)
        if options.strict_public:
            reject_staged_changes(checkout, repository_id)
        plans.append(
            {
                "repository": repository,
                "checkout": checkout,
                "outputDir": output_dir,
                "outputPath": output_dir / "harvest.json",
            }
        )

    prepared: list[dict[str, Any]] = []
    for plan in plans:
        repository = plan["repository"]
        snapshot = collect_local_repository(
            HarvestOptions(
                source=plan["checkout"],
                repository=repository["repository"],
                revision=repository["revision"] or repository["ref"],
                target=Path(repository["target"]) if repository["target"] is not None else None,
                max_file_bytes=options.max_file_bytes,
            )
        )
        interface_index_result = None
        if options.emit_interface_indexes:
            interface_index_result = run_project_profile_analyzers(
                source=analysis_source_root(plan["checkout"], snapshot),
                snapshot=snapshot,
                package_id=repository["packageId"],
                cache_dir=repository_analyzer_cache_dir(
                    options.analyzer_cache_dir,
                    repository["id"],
                ),
            )
        prepared.append(
            {
                **plan,
                "snapshot": snapshot,
                "interfaceIndexResult": interface_index_result,
            }
        )

    collected: list[dict[str, Any]] = []
    for plan in prepared:
        repository = plan["repository"]
        repository_id = repository["id"]
        checkout = plan["checkout"]
        snapshot = plan["snapshot"]
        output_path = plan["outputPath"]
        plan["outputDir"].mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(snapshot, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        interface_index_record = None
        interface_index_result = plan["interfaceIndexResult"]
        if interface_index_result is not None:
            interface_index_output = None
            interface_index = interface_index_result.get("index")
            if isinstance(interface_index, dict):
                interface_index_output = plan["outputDir"] / PUBLIC_INTERFACE_INDEX_FILENAME
                interface_index_output.write_text(
                    render_public_interface_index_json(interface_index),
                    encoding="utf-8",
                )
            interface_index_record = interface_index_batch_record(
                interface_index_result,
                output_path=interface_index_output,
            )
        collected_record = {
            "id": repository_id,
            "repository": repository["repository"],
            "revision": repository["revision"],
            "ref": repository["ref"],
            "checkout": str(checkout),
            "target": repository["target"],
            "packageId": repository["packageId"],
            "labels": repository["labels"],
            "sourceManifest": repository["sourceManifest"],
            "output": str(output_path),
            "fileCount": snapshot["summary"]["fileCount"],
            "skippedFileCount": snapshot["summary"]["skippedFileCount"],
        }
        if interface_index_record is not None:
            collected_record["interfaceIndex"] = interface_index_record
        collected.append(collected_record)

    result = {
        "status": "ok",
        "input": str(options.inputs),
        "outputRoot": str(options.out),
        "selectedIds": list(selected_ids),
        "collectedCount": len(collected),
        "skippedCount": len(skipped),
        "collected": collected,
        "skipped": skipped,
    }
    if options.report is not None:
        report = build_batch_validation_report(
            batch_result=result,
            snapshots_by_id={plan["repository"]["id"]: plan["snapshot"] for plan in prepared},
            strict_public=options.strict_public,
        )
        write_batch_validation_report(options.report, report)
        result["status"] = report["status"]
        result["validationReport"] = str(options.report)
    return result


def analysis_source_root(checkout: Path, snapshot: dict[str, Any]) -> Path:
    source = snapshot.get("source")
    if not isinstance(source, dict):
        return checkout
    target = source.get("target")
    if not isinstance(target, dict):
        return checkout
    target_path = target.get("path")
    target_kind = target.get("kind")
    if not isinstance(target_path, str) or target_path == "." or target_kind == "repository":
        return checkout
    candidate = (checkout / target_path).resolve()
    if target_kind == "file":
        return candidate.parent
    return candidate


def candidate_directory(out_root: Path, repository_id: str) -> Path:
    if not SAFE_REPOSITORY_ID.match(repository_id):
        raise ValueError(
            f"Repository id {repository_id!r} is unsafe repository id for candidate directory"
        )
    return out_root / repository_id


def repository_analyzer_cache_dir(cache_root: Path | None, repository_id: str) -> Path | None:
    if cache_root is None:
        return None
    if not SAFE_REPOSITORY_ID.match(repository_id):
        raise ValueError(
            f"Repository id {repository_id!r} is unsafe repository id for analyzer cache directory"
        )
    return cache_root / repository_id


def resolve_checkout(inputs_root: Path, repository: dict[str, Any]) -> Path:
    checkout_value = repository.get("checkout")
    if not isinstance(checkout_value, str) or not checkout_value.strip():
        raise ValueError(f"Repository id {repository['id']!r} requires checkout")

    checkout_path = Path(checkout_value)
    if not checkout_path.is_absolute():
        checkout_path = inputs_root / checkout_path
    checkout = checkout_path.resolve()
    if not checkout.exists() or not checkout.is_dir():
        raise ValueError(f"Repository id {repository['id']!r} checkout does not exist: {checkout}")
    return checkout


def reject_staged_changes(checkout: Path, repository_id: str) -> None:
    staged_paths = git_staged_paths(checkout)
    if not staged_paths:
        return
    preview = ", ".join(staged_paths[:5])
    suffix = "" if len(staged_paths) <= 5 else f", and {len(staged_paths) - 5} more"
    raise ValueError(
        f"Repository id {repository_id!r} has staged changes in strict public mode: "
        f"{preview}{suffix}"
    )


def git_staged_paths(checkout: Path) -> list[str]:
    if not is_git_worktree(checkout):
        return []
    worktree_root = git_worktree_root(checkout)
    if worktree_root is None:
        return []
    relative_checkout = checkout.resolve().relative_to(worktree_root)
    pathspec = relative_checkout.as_posix() if relative_checkout.parts else "."
    result = subprocess.run(  # noqa: S603
        ["git", "-C", str(worktree_root), "diff", "--cached", "--name-only", "--", pathspec],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def is_git_worktree(checkout: Path) -> bool:
    result = subprocess.run(  # noqa: S603
        ["git", "-C", str(checkout), "rev-parse", "--is-inside-work-tree"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def git_worktree_root(checkout: Path) -> Path | None:
    result = subprocess.run(  # noqa: S603
        ["git", "-C", str(checkout), "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    if not value:
        return None
    return Path(value).resolve()
