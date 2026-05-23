#!/usr/bin/env python3
"""Local-only real repository validation runner for SpecHarvester artifacts."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from spec_harvester.source_manifest import read_repository_source_manifests  # noqa: E402
from spec_harvester.specnode_refinement import (  # noqa: E402
    build_refine_preview_plan,
    build_specnode_artifact_bundle,
)

DEFAULT_INPUTS = ROOT / ".smoke" / "inputs"
DEFAULT_OUT = ROOT / ".smoke" / "output" / "real-repository-validation"
DEFAULT_PYTHON_COMMAND = sys.executable
DEFAULT_PYTHONPATH = str(SRC_ROOT)
DEFAULT_SPECPM_COMMAND = "python -m specpm.cli validate {candidate} --json"
DEFAULT_RUN_REPORT_NAME = "run-report.json"
DEFAULT_DRAFT_SUMMARY_NAME = "draft-summary.json"
DEFAULT_SPECNODE_BUNDLE_NAME = "specnode-artifact-bundle.json"
DEFAULT_SPECNODE_PREVIEW_NAME = "specnode-refine-preview-plan.json"
DEFAULT_SPECNODE_RESULT_NAME = "specnode-refinement-result.json"


class RealRepositoryValidationError(RuntimeError):
    """Raised when the local validation runner fails in a fatal way."""


@dataclass(frozen=True)
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Orchestrate local-only real repository validation."
    )
    parser.add_argument(
        "--inputs",
        type=Path,
        default=DEFAULT_INPUTS,
        help=f"Manifest directory to validate. Default: {DEFAULT_INPUTS}.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Output root for validation artifacts. Default: {DEFAULT_OUT}.",
    )
    parser.add_argument(
        "--select",
        action="append",
        default=[],
        help="Repository id(s) to validate. Repeats for multiple ids.",
    )
    parser.add_argument(
        "--python-command",
        default=DEFAULT_PYTHON_COMMAND,
        help=f"Python executable used for SpecHarvester CLI steps. "
        f"Default: {DEFAULT_PYTHON_COMMAND}.",
    )
    parser.add_argument(
        "--pythonpath",
        default=DEFAULT_PYTHONPATH,
        help=f"PYTHONPATH for SpecHarvester CLI steps. Default: {DEFAULT_PYTHONPATH}.",
    )
    parser.add_argument(
        "--relaxed-private",
        action="store_true",
        help="Use relaxed-private mode during collect-batch.",
    )
    parser.add_argument(
        "--emit-interface-indexes",
        action="store_true",
        help="Generate public interface index artifacts before drafting.",
    )
    parser.add_argument(
        "--analyzer-cache-dir",
        type=Path,
        help="Optional analyzer cache directory for interface-index generation.",
    )
    parser.add_argument(
        "--specpm-command",
        default=DEFAULT_SPECPM_COMMAND,
        help=(
            "Command template for SpecPM validation. Supports {candidate}. "
            f"Default: {DEFAULT_SPECPM_COMMAND}."
        ),
    )
    parser.add_argument(
        "--specpm-pythonpath",
        help="PYTHONPATH for SpecPM validation command.",
    )
    parser.add_argument(
        "--skip-specpm-validation",
        action="store_true",
        help="Skip per-package SpecPM validation.",
    )
    parser.add_argument(
        "--specnode-command",
        help=(
            "Optional SpecNode-compatible command template. "
            "Supports {candidate}, {bundle}, {preview_plan}, {result}."
        ),
    )
    parser.add_argument(
        "--no-specnode-artifacts",
        action="store_true",
        help="Do not write specnode artifact bundle and preview plan files.",
    )
    parser.add_argument(
        "--skip-governance-reports",
        action="store_true",
        help="Skip generation of governance report outputs.",
    )
    parser.add_argument(
        "--skip-smoke-triage",
        action="store_true",
        help="Skip local smoke triage summary generation.",
    )
    parser.add_argument(
        "--strict-exit",
        action="store_true",
        help="Treat optional SpecNode/governance/smoke failures as fatal.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned commands without executing them.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help=f"Run report JSON output path. Default: <out>/{DEFAULT_RUN_REPORT_NAME}.",
    )
    return parser.parse_args(argv)


def run_command(
    *,
    command: list[str],
    cwd: Path,
    env: dict[str, str] | None = None,
    dry_run: bool,
) -> CommandResult:
    if dry_run:
        return CommandResult(command=command, returncode=0, stdout="", stderr="")

    completed = subprocess.run(
        command,
        cwd=str(cwd),
        env=env,
        text=True,
        capture_output=True,
    )
    return CommandResult(
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout.strip(),
        stderr=completed.stderr.strip(),
    )


def _shell_split(value: str) -> list[str]:
    return shlex.split(value)


def _python_env(pythonpath: str | None) -> dict[str, str] | None:
    if not pythonpath:
        return None
    env = os.environ.copy()
    env["PYTHONPATH"] = pythonpath
    return env


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _run_report_path(args: argparse.Namespace) -> Path:
    return args.output if args.output is not None else args.out / DEFAULT_RUN_REPORT_NAME


def _select_repositories(
    records: list[dict[str, Any]],
    selected: tuple[str, ...],
) -> list[dict[str, Any]]:
    if not selected:
        return list(records)

    available = {record["id"]: record for record in records}
    unknown = sorted(set(selected) - set(available))
    if unknown:
        raise RealRepositoryValidationError(f"Unknown repository id(s): {', '.join(unknown)}")

    ordered: list[dict[str, Any]] = []
    included: set[str] = set()
    for repository_id in selected:
        if repository_id in included:
            continue
        ordered.append(available[repository_id])
        included.add(repository_id)

    return ordered


def _build_source_manifest_command(python_command: str, inputs: Path) -> list[str]:
    return [
        python_command,
        "-m",
        "spec_harvester",
        "source-manifests",
        str(inputs),
    ]


def _build_collect_batch_command(
    python_command: str,
    inputs: Path,
    out: Path,
    *,
    emit_interface_indexes: bool,
    analyzer_cache_dir: Path | None,
    relaxed_private: bool,
    selected_ids: tuple[str, ...],
) -> list[str]:
    command = [
        python_command,
        "-m",
        "spec_harvester",
        "collect-batch",
        str(inputs),
        "--out",
        str(out),
        "--report",
        str(out / "batch-validation.json"),
    ]
    if emit_interface_indexes:
        command.extend(["--emit-interface-indexes"])
    if analyzer_cache_dir is not None:
        command.extend(["--analyzer-cache-dir", str(analyzer_cache_dir)])
    if relaxed_private:
        command.append("--relaxed-private")
    for repository_id in selected_ids:
        command.extend(["--select", repository_id])
    return command


def _build_draft_command(
    python_command: str,
    out_dir: Path,
    package_id: str | None,
) -> list[str]:
    command = [
        python_command,
        "-m",
        "spec_harvester",
        "draft",
        str(out_dir),
        "--out",
        str(out_dir),
    ]
    if package_id:
        command.extend(["--package-id", package_id])
    return command


def _build_specpm_command(template: str, candidate_dir: Path) -> list[str]:
    return _shell_split(template.format(candidate=str(candidate_dir)))


def _specnode_artifact_paths(candidate_dir: Path) -> tuple[Path, Path]:
    return (
        candidate_dir / DEFAULT_SPECNODE_BUNDLE_NAME,
        candidate_dir / DEFAULT_SPECNODE_PREVIEW_NAME,
    )


def _build_specnode_artifacts(candidate_dir: Path) -> tuple[Path, Path]:
    bundle_path, preview_plan_path = _specnode_artifact_paths(candidate_dir)
    bundle = build_specnode_artifact_bundle(candidate_dir)
    preview_plan = build_refine_preview_plan(bundle, candidate_dir)
    _write_json(bundle_path, bundle)
    _write_json(preview_plan_path, preview_plan)
    return bundle_path, preview_plan_path


def _draft_summary_path(candidate_dir: Path) -> Path:
    return candidate_dir / DEFAULT_DRAFT_SUMMARY_NAME


def _strip_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _parse_boundary_spec_summary_and_capabilities(spec_path: Path) -> tuple[str | None, list[str]]:
    summary: str | None = None
    capability_ids: list[str] = []
    in_intent = False
    in_provides = False
    in_capabilities = False
    for line in spec_path.read_text(encoding="utf-8").splitlines():
        if line == "intent:":
            in_intent = True
            continue
        if in_intent:
            if line.startswith("  summary:"):
                summary = _strip_yaml_scalar(line.split(":", 1)[1])
                in_intent = False
                continue
            if line and not line.startswith(" "):
                in_intent = False

        if line == "provides:":
            in_provides = True
            continue
        if in_provides and line == "  capabilities:":
            in_capabilities = True
            continue
        if in_capabilities:
            if line and not line.startswith("    "):
                in_capabilities = False
                in_provides = False
                continue
            if line.startswith("    - id:"):
                capability_id = _strip_yaml_scalar(line.split(":", 1)[1])
                if capability_id:
                    capability_ids.append(capability_id)

    return summary, capability_ids


def _build_draft_summary(candidate_dir: Path) -> dict[str, Any]:
    bundle = build_specnode_artifact_bundle(candidate_dir)
    preview_plan = build_refine_preview_plan(bundle, candidate_dir)
    compact_input = preview_plan.get("compactModelInput", {})
    if not isinstance(compact_input, dict):
        compact_input = {}
    metadata = compact_input.get("draftCandidateMetadata", {})
    if not isinstance(metadata, dict):
        metadata = {}

    spec_paths = [
        item
        for item in metadata.get("specPaths", [])
        if isinstance(item, str) and item.startswith("specs/")
    ]
    source_artifacts = ["specpm.yaml", *spec_paths]

    boundary_summary: str | None = None
    capability_ids: list[str] = []
    for spec_path in spec_paths:
        summary, parsed_capabilities = _parse_boundary_spec_summary_and_capabilities(
            candidate_dir / spec_path
        )
        boundary_summary = boundary_summary or summary
        capability_ids.extend(parsed_capabilities)

    if not capability_ids:
        capability_ids = [
            item for item in metadata.get("capabilityIds", []) if isinstance(item, str)
        ]

    unique_capability_ids = sorted(set(capability_ids))
    intent = boundary_summary or metadata.get("summary") or ""
    intent_ids = [item for item in metadata.get("intentIds", []) if isinstance(item, str)]
    capabilities = [
        {"id": capability_id, "evidenceSources": source_artifacts}
        for capability_id in unique_capability_ids
    ]

    return {
        "schemaVersion": 1,
        "kind": "SpecHarvesterDraftSummary",
        "sourceArtifacts": source_artifacts,
        "candidate": {
            "intent": intent,
            "intentIds": sorted(set(intent_ids)),
            "evidenceSources": source_artifacts,
            "capabilities": capabilities,
        },
    }


def _build_specnode_command(
    *,
    template: str,
    candidate_dir: Path,
    bundle_path: Path | None,
    preview_plan_path: Path | None,
) -> list[str]:
    template_values: dict[str, str] = {
        "candidate": str(candidate_dir),
        "result": str(candidate_dir / DEFAULT_SPECNODE_RESULT_NAME),
    }
    if bundle_path is not None:
        template_values["bundle"] = str(bundle_path)
    if preview_plan_path is not None:
        template_values["preview_plan"] = str(preview_plan_path)

    try:
        return _shell_split(template.format(**template_values))
    except KeyError as exc:
        missing = str(exc).strip("'")
        raise RealRepositoryValidationError(
            f"SpecNode command template missing required placeholder: {{{missing}}}"
        ) from exc


def _step_status(
    *,
    returncode: int,
    optional: bool,
    strict: bool,
) -> str:
    if returncode == 0:
        return "ok"
    if optional and not strict:
        return "degraded"
    return "failed"


def _merge_status(current: str, next_status: str) -> str:
    if current == "error" or next_status == "error":
        return "error"
    if current == "degraded" or next_status == "degraded":
        return "degraded"
    return next_status


def _run_step(
    *,
    payload: dict[str, Any],
    package_record: dict[str, Any] | None,
    step: str,
    command: list[str],
    strict: bool,
    optional: bool,
    error_message: str,
    env: dict[str, str] | None,
    cwd: Path,
    args: argparse.Namespace,
) -> None:
    result = run_command(
        command=command,
        cwd=cwd,
        env=env,
        dry_run=args.dry_run,
    )

    status = _step_status(
        returncode=result.returncode,
        optional=optional,
        strict=strict and optional,
    )

    step_record = {
        "step": step,
        "status": status,
        "returncode": result.returncode,
        "command": result.command,
        "strict": strict,
        "optional": optional,
    }

    payload["steps"].append(step_record)
    if package_record is not None:
        package_record.setdefault("steps", []).append(step_record)
    if result.stdout:
        payload.setdefault("commandOutput", []).append({"step": step, "stdout": result.stdout})
        if package_record is not None:
            package_record.setdefault("commandOutput", []).append(
                {"step": step, "stdout": result.stdout}
            )
    if result.stderr:
        payload.setdefault("commandOutput", []).append({"step": step, "stderr": result.stderr})
        if package_record is not None:
            package_record.setdefault("commandOutput", []).append(
                {"step": step, "stderr": result.stderr}
            )

    if result.returncode == 0:
        if payload["status"] == "ok":
            return
        payload["status"] = _merge_status(payload["status"], status)
        return

    if optional and not strict:
        failure = {
            "step": step,
            "status": "failed",
            "returncode": result.returncode,
            "message": error_message,
            "command": result.command,
            "package": package_record.get("id") if package_record is not None else None,
        }
        payload["nonFatalFailures"].append(failure)
        if package_record is not None:
            package_record.setdefault("nonFatalFailures", []).append(failure)
        payload["status"] = _merge_status(payload["status"], status)
        if package_record is not None:
            package_record["status"] = _merge_status(package_record["status"], status)
        return

    raise RealRepositoryValidationError(f"{error_message} (exit {result.returncode})")


def _run_package_step(
    *,
    args: argparse.Namespace,
    repository: dict[str, Any],
    payload: dict[str, Any],
) -> None:
    candidate_dir = args.out / repository["id"]
    package_record: dict[str, Any] = {
        "id": repository["id"],
        "packageId": repository.get("packageId"),
        "candidateDir": str(candidate_dir),
        "repository": repository["repository"],
        "revision": repository["revision"],
        "status": "ok",
        "steps": [],
    }

    if not args.dry_run:
        if not candidate_dir.exists():
            raise RealRepositoryValidationError(
                f"Collected candidate directory not found: {candidate_dir}"
            )
        if not (candidate_dir / "harvest.json").exists():
            raise RealRepositoryValidationError(
                f"Candidate directory missing harvest.json: {candidate_dir}"
            )

    _run_step(
        args=args,
        payload=payload,
        package_record=package_record,
        step="draft",
        command=_build_draft_command(
            args.python_command,
            candidate_dir,
            package_id=repository.get("packageId"),
        ),
        strict=True,
        optional=False,
        error_message=f"draft failed for {repository['id']}",
        env=_python_env(args.pythonpath),
        cwd=ROOT,
    )

    draft_summary_path = _draft_summary_path(candidate_dir)
    package_record["draftSummaryPath"] = str(draft_summary_path)
    package_record["manifestPath"] = str(candidate_dir / "specpm.yaml")
    if not args.dry_run:
        draft_summary = _build_draft_summary(candidate_dir)
        _write_json(draft_summary_path, draft_summary)
        source_artifacts = draft_summary.get("sourceArtifacts")
        if isinstance(source_artifacts, list):
            package_record["candidateArtifacts"] = [
                str(candidate_dir / artifact)
                for artifact in source_artifacts
                if isinstance(artifact, str)
            ]

    artifact_paths: tuple[Path, Path] | None = None
    if not args.no_specnode_artifacts:
        artifact_paths = _specnode_artifact_paths(candidate_dir)
        package_record["artifactBundlePath"] = str(artifact_paths[0])
        package_record["previewPlanPath"] = str(artifact_paths[1])
        if not args.dry_run:
            artifact_paths = _build_specnode_artifacts(candidate_dir)

    if args.specnode_command is not None:
        specnode_command = _build_specnode_command(
            template=args.specnode_command,
            candidate_dir=candidate_dir,
            bundle_path=artifact_paths[0] if artifact_paths is not None else None,
            preview_plan_path=artifact_paths[1] if artifact_paths is not None else None,
        )
        _run_step(
            payload=payload,
            package_record=package_record,
            step="specnode",
            command=specnode_command,
            strict=args.strict_exit,
            optional=True,
            error_message=f"external specnode command failed for {repository['id']}",
            env=_python_env(args.pythonpath),
            cwd=ROOT,
            args=args,
        )
        package_record["specnodeResultPath"] = str(candidate_dir / DEFAULT_SPECNODE_RESULT_NAME)

    if not args.skip_specpm_validation:
        _run_step(
            payload=payload,
            package_record=package_record,
            step="specpm",
            command=_build_specpm_command(args.specpm_command, candidate_dir),
            strict=True,
            optional=False,
            error_message=f"specpm validation failed for {repository['id']}",
            env=_python_env(args.specpm_pythonpath),
            cwd=ROOT,
            args=args,
        )

    payload["packages"].append(package_record)


def run_validation(args: argparse.Namespace) -> dict[str, Any]:
    args.out.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "status": "ok",
        "runReport": str(_run_report_path(args)),
        "out": str(args.out),
        "inputs": str(args.inputs),
        "selected": [],
        "packageCount": 0,
        "packages": [],
        "steps": [],
        "nonFatalFailures": [],
        "commandOutput": [],
        "strictMode": bool(args.strict_exit),
        "dryRun": bool(args.dry_run),
        "emitInterfaceIndexes": bool(args.emit_interface_indexes),
        "relaxedPrivate": bool(args.relaxed_private),
    }

    try:
        repository_records = read_repository_source_manifests(args.inputs)
    except ValueError as exc:
        raise RealRepositoryValidationError(str(exc)) from exc

    selected_records = _select_repositories(repository_records, tuple(args.select))
    if not selected_records:
        raise RealRepositoryValidationError("No repositories selected for validation")

    payload["selected"] = [repository["id"] for repository in selected_records]

    _run_step(
        args=args,
        payload=payload,
        package_record=None,
        step="source-manifests",
        command=_build_source_manifest_command(args.python_command, args.inputs),
        strict=True,
        optional=False,
        error_message="source-manifests failed",
        env=_python_env(args.pythonpath),
        cwd=ROOT,
    )

    _run_step(
        args=args,
        payload=payload,
        package_record=None,
        step="collect-batch",
        command=_build_collect_batch_command(
            args.python_command,
            args.inputs,
            args.out,
            emit_interface_indexes=args.emit_interface_indexes,
            analyzer_cache_dir=args.analyzer_cache_dir,
            relaxed_private=args.relaxed_private,
            selected_ids=tuple(repository["id"] for repository in selected_records),
        ),
        strict=True,
        optional=False,
        error_message="collect-batch failed",
        env=_python_env(args.pythonpath),
        cwd=ROOT,
    )

    for repository in selected_records:
        _run_package_step(args=args, repository=repository, payload=payload)
        payload["packageCount"] += 1

    if not args.skip_governance_reports:
        _run_step(
            args=args,
            payload=payload,
            package_record=None,
            step="governance-report",
            command=[
                args.python_command,
                "-m",
                "spec_harvester",
                "governance-report",
                "--candidates-root",
                str(args.out),
                "--output",
                str(args.out / "governance-claims.json"),
            ],
            strict=args.strict_exit,
            optional=True,
            error_message="governance-report failed",
            env=_python_env(args.pythonpath),
            cwd=ROOT,
        )

        _run_step(
            args=args,
            payload=payload,
            package_record=None,
            step="governance-upstream-report",
            command=[
                args.python_command,
                "-m",
                "spec_harvester",
                "governance-upstream-report",
                "--candidates-root",
                str(args.out),
                "--output",
                str(args.out / "namespace-upstream.json"),
            ],
            strict=args.strict_exit,
            optional=True,
            error_message="governance-upstream-report failed",
            env=_python_env(args.pythonpath),
            cwd=ROOT,
        )

        _run_step(
            args=args,
            payload=payload,
            package_record=None,
            step="governance-license-provenance-report",
            command=[
                args.python_command,
                "-m",
                "spec_harvester",
                "governance-license-provenance-report",
                "--candidates-root",
                str(args.out),
                "--output",
                str(args.out / "license-provenance.json"),
            ],
            strict=args.strict_exit,
            optional=True,
            error_message="governance-license-provenance-report failed",
            env=_python_env(args.pythonpath),
            cwd=ROOT,
        )

    if not args.skip_smoke_triage and not args.skip_governance_reports:
        _run_step(
            args=args,
            payload=payload,
            package_record=None,
            step="smoke-triage-summary",
            command=[
                args.python_command,
                "-m",
                "spec_harvester",
                "smoke-triage-summary",
                "--batch-validation",
                str(args.out / "batch-validation.json"),
                "--governance-claims",
                str(args.out / "governance-claims.json"),
                "--namespace-upstream",
                str(args.out / "namespace-upstream.json"),
                "--license-provenance",
                str(args.out / "license-provenance.json"),
                "--output",
                str(args.out / "smoke-triage.json"),
            ],
            strict=args.strict_exit,
            optional=True,
            error_message="smoke-triage-summary failed",
            env=_python_env(args.pythonpath),
            cwd=ROOT,
        )

    return payload


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = run_validation(args)
        _write_json(_run_report_path(args), report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except RealRepositoryValidationError as exc:
        report = {
            "status": "error",
            "message": str(exc),
            "runReport": str(_run_report_path(args)),
            "out": str(args.out),
            "inputs": str(args.inputs),
            "selected": args.select,
        }
        _write_json(_run_report_path(args), report)
        print(json.dumps(report, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
