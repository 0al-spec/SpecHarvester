from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from spec_harvester.batch_collection import BatchCollectOptions, collect_batch_snapshots
from spec_harvester.collector import (
    DEFAULT_MAX_FILE_BYTES,
    HarvestOptions,
    collect_local_repository,
)
from spec_harvester.drafter import (
    DEFAULT_AUTHOR,
    DEFAULT_SPEC_VERSION,
    DraftOptions,
    draft_spec_package,
)
from spec_harvester.promoter import (
    PrepareAcceptedManifestEntryOptions,
    PromoteOptions,
    prepare_accepted_manifest_entry,
    promote_candidate,
)
from spec_harvester.source_manifest import read_repository_source_manifests


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="spec-harvester")
    subcommands = parser.add_subparsers(dest="command", required=True)

    collect_local = subcommands.add_parser(
        "collect-local",
        help="Collect a safe evidence snapshot from a local repository checkout.",
    )
    collect_local.add_argument("source", type=Path, help="Local repository checkout path.")
    collect_local.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output directory where harvest.json will be written.",
    )
    collect_local.add_argument("--repository", help="Public source repository URL.")
    collect_local.add_argument("--revision", help="Pinned source revision or commit SHA.")
    collect_local.add_argument(
        "--max-file-bytes",
        type=int,
        default=DEFAULT_MAX_FILE_BYTES,
        help=f"Maximum allowlisted file size to read. Default: {DEFAULT_MAX_FILE_BYTES}.",
    )
    collect_local.set_defaults(func=run_collect_local)

    collect_batch = subcommands.add_parser(
        "collect-batch",
        help="Collect harvest snapshots from repository source manifests.",
    )
    collect_batch.add_argument(
        "inputs",
        type=Path,
        help="Directory containing repository source manifests matching *.yml.",
    )
    collect_batch.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output root where deterministic candidate directories are written.",
    )
    collect_batch.add_argument(
        "--select",
        action="append",
        default=[],
        help="Repository id to collect. Can be passed multiple times.",
    )
    collect_batch.add_argument(
        "--max-file-bytes",
        type=int,
        default=DEFAULT_MAX_FILE_BYTES,
        help=f"Maximum allowlisted file size to read. Default: {DEFAULT_MAX_FILE_BYTES}.",
    )
    collect_batch.add_argument(
        "--report",
        type=Path,
        help="Optional path where a deterministic batch validation JSON report is written.",
    )
    collect_batch.set_defaults(func=run_collect_batch)

    draft = subcommands.add_parser(
        "draft",
        help="Draft a candidate SpecPackage from a harvest.json snapshot.",
    )
    draft.add_argument("snapshot", type=Path, help="Harvest snapshot file or directory.")
    draft.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output candidate package directory.",
    )
    draft.add_argument(
        "--package-id",
        help="SpecPackage id. Defaults to <repository-name>.core.",
    )
    draft.add_argument("--name", help="Human-readable package name.")
    draft.add_argument(
        "--version",
        default=DEFAULT_SPEC_VERSION,
        help=f"Generated SpecPackage version. Default: {DEFAULT_SPEC_VERSION}.",
    )
    draft.add_argument(
        "--author",
        default=DEFAULT_AUTHOR,
        help=f"Generated SpecPackage author. Default: {DEFAULT_AUTHOR}.",
    )
    draft.add_argument(
        "--interface-index",
        type=Path,
        help=(
            "Optional PublicInterfaceIndex JSON artifact used to enrich "
            "generated interfaces.inbound entries."
        ),
    )
    draft.set_defaults(func=run_draft)

    promote = subcommands.add_parser(
        "promote",
        help="Validate and copy a candidate package into an accepted source root.",
    )
    promote.add_argument("candidate", type=Path, help="Candidate SpecPackage directory.")
    promote.add_argument(
        "--accepted-root",
        type=Path,
        required=True,
        help="Directory where the promoted package copy will be written.",
    )
    promote.add_argument(
        "--manifest",
        type=Path,
        help="Optional accepted-packages.yml manifest to update with a local path entry.",
    )
    promote.add_argument(
        "--manifest-entry-path",
        help="Path to write into the manifest. Defaults to an inferred local path.",
    )
    promote.add_argument(
        "--package-subdir",
        help="Subdirectory under --accepted-root. Defaults to <package_id>/<version>.",
    )
    promote.add_argument(
        "--specpm-command",
        default="specpm",
        help="SpecPM validation command. Default: specpm.",
    )
    promote.add_argument(
        "--specpm-pythonpath",
        help="PYTHONPATH prefix for a local SpecPM checkout.",
    )
    promote.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip SpecPM validation. Intended only for tests or emergency manual workflows.",
    )
    promote.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing promoted package directory.",
    )
    promote.set_defaults(func=run_promote)

    prepare_manifest_entry = subcommands.add_parser(
        "prepare-accepted-entry",
        help="Prepare a PR-ready accepted-packages.yml entry for a reviewed candidate.",
    )
    prepare_manifest_entry.add_argument(
        "candidate", type=Path, help="Reviewed candidate SpecPackage directory."
    )
    prepare_manifest_entry.add_argument(
        "--manifest",
        required=True,
        type=Path,
        help="Accepted-packages manifest file to update.",
    )
    prepare_manifest_entry.add_argument(
        "--manifest-entry-path",
        help=(
            "Explicit manifest entry path to write. If set, --manifest-entry-prefix "
            "and --package-subdir are ignored."
        ),
    )
    prepare_manifest_entry.add_argument(
        "--manifest-entry-prefix",
        default="public-index/generated",
        help="Path prefix for inferred manifest entry. Default: public-index/generated.",
    )
    prepare_manifest_entry.add_argument(
        "--package-subdir",
        help=(
            "Package subdirectory used with --manifest-entry-prefix "
            "(defaults to <packageId>/<version>)."
        ),
    )
    prepare_manifest_entry.set_defaults(func=run_prepare_accepted_manifest_entry)

    source_manifests = subcommands.add_parser(
        "source-manifests",
        help="Read repository source manifests from an inputs directory and print JSON.",
    )
    source_manifests.add_argument(
        "inputs",
        type=Path,
        help="Directory containing repository source manifests matching *.yml.",
    )
    source_manifests.add_argument(
        "--include-disabled",
        action="store_true",
        help="Include entries with enabled: false in the JSON output.",
    )
    source_manifests.set_defaults(func=run_source_manifests)
    return parser


def run_collect_local(args: argparse.Namespace) -> int:
    snapshot = collect_local_repository(
        HarvestOptions(
            source=args.source,
            repository=args.repository,
            revision=args.revision,
            max_file_bytes=args.max_file_bytes,
        )
    )
    args.out.mkdir(parents=True, exist_ok=True)
    output_path = args.out / "harvest.json"
    output_path.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "ok",
                "output": str(output_path),
                "fileCount": snapshot["summary"]["fileCount"],
                "skippedFileCount": snapshot["summary"]["skippedFileCount"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def run_collect_batch(args: argparse.Namespace) -> int:
    result = collect_batch_snapshots(
        BatchCollectOptions(
            inputs=args.inputs,
            out=args.out,
            selected_ids=tuple(args.select),
            max_file_bytes=args.max_file_bytes,
            report=args.report,
        )
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_draft(args: argparse.Namespace) -> int:
    result = draft_spec_package(
        DraftOptions(
            snapshot=args.snapshot,
            out=args.out,
            package_id=args.package_id,
            name=args.name,
            version=args.version,
            author=args.author,
            interface_index=args.interface_index,
        )
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_promote(args: argparse.Namespace) -> int:
    result = promote_candidate(
        PromoteOptions(
            candidate=args.candidate,
            accepted_root=args.accepted_root,
            manifest=args.manifest,
            manifest_entry_path=args.manifest_entry_path,
            package_subdir=args.package_subdir,
            specpm_command=args.specpm_command,
            specpm_pythonpath=args.specpm_pythonpath,
            skip_validation=args.skip_validation,
            force=args.force,
        )
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_source_manifests(args: argparse.Namespace) -> int:
    repositories = read_repository_source_manifests(
        args.inputs,
        include_disabled=args.include_disabled,
    )
    print(
        json.dumps(
            {
                "status": "ok",
                "input": str(args.inputs),
                "repositoryCount": len(repositories),
                "repositories": repositories,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def run_prepare_accepted_manifest_entry(args: argparse.Namespace) -> int:
    result = prepare_accepted_manifest_entry(
        PrepareAcceptedManifestEntryOptions(
            candidate=args.candidate,
            manifest=args.manifest,
            manifest_entry_path=args.manifest_entry_path,
            manifest_entry_prefix=args.manifest_entry_prefix,
            package_subdir=args.package_subdir,
        )
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
