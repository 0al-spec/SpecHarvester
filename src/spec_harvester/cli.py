from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

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
    draft.set_defaults(func=run_draft)
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


def run_draft(args: argparse.Namespace) -> int:
    result = draft_spec_package(
        DraftOptions(
            snapshot=args.snapshot,
            out=args.out,
            package_id=args.package_id,
            name=args.name,
            version=args.version,
            author=args.author,
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
