from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.batch_validation import (
    build_batch_validation_report,
    write_batch_validation_report,
)
from spec_harvester.collector import (
    DEFAULT_MAX_FILE_BYTES,
    HarvestOptions,
    collect_local_repository,
)
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
                max_file_bytes=options.max_file_bytes,
            )
        )
        prepared.append({**plan, "snapshot": snapshot})

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
        collected.append(
            {
                "id": repository_id,
                "repository": repository["repository"],
                "revision": repository["revision"],
                "ref": repository["ref"],
                "checkout": str(checkout),
                "packageId": repository["packageId"],
                "labels": repository["labels"],
                "sourceManifest": repository["sourceManifest"],
                "output": str(output_path),
                "fileCount": snapshot["summary"]["fileCount"],
                "skippedFileCount": snapshot["summary"]["skippedFileCount"],
            }
        )

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


def candidate_directory(out_root: Path, repository_id: str) -> Path:
    if not SAFE_REPOSITORY_ID.match(repository_id):
        raise ValueError(
            f"Repository id {repository_id!r} is unsafe repository id for candidate directory"
        )
    return out_root / repository_id


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
