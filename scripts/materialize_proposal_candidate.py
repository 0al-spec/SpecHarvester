from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

import yaml

from spec_harvester.producer_receipt import (
    CandidateOutputFile,
    ProducerReceipt,
    ProducerReceiptRequest,
)
from spec_harvester.producer_reports import (
    DIAGNOSTICS_REPORT_FILENAME,
    VALIDATION_REPORT_FILENAME,
    ProducerDiagnosticsReport,
    ProducerReportRequest,
    ProducerValidationReport,
)
from spec_harvester.promoter import read_manifest_identity, reject_symlinks


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Materialize missing producer artifacts for a reviewed candidate fixture."
    )
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--package-id", required=True)
    parser.add_argument("--package-version", required=True)
    args = parser.parse_args()

    result = materialize_reviewed_candidate(
        source=args.source,
        out=args.out,
        package_id=args.package_id,
        package_version=args.package_version,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def materialize_reviewed_candidate(
    *,
    source: Path,
    out: Path,
    package_id: str,
    package_version: str,
) -> dict[str, Any]:
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(source, out, ignore=shutil.ignore_patterns(".git", ".DS_Store"))
    reject_symlinks(out)

    manifest_path = out / "specpm.yaml"
    identity = read_manifest_identity(manifest_path)
    if identity["id"] != package_id:
        raise SystemExit("candidate id mismatch after materialization")
    if identity["version"] != package_version:
        raise SystemExit("candidate version mismatch after materialization")

    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise SystemExit("candidate specpm.yaml must be a YAML object")
    spec_paths = safe_manifest_spec_paths(out, manifest)
    if not spec_paths:
        raise SystemExit("candidate specpm.yaml has no safe specs[].path")

    package_api_version = str(manifest.get("apiVersion") or "specpm.dev/v0.1")
    output_files = [
        CandidateOutputFile(root=out, path="specpm.yaml", role="manifest"),
        *[
            CandidateOutputFile(root=out, path=spec_path, role="boundary_spec")
            for spec_path in spec_paths
        ],
    ]
    public_interface_index_path = optional_public_interface_index(out)
    if public_interface_index_path is not None:
        output_files.append(
            CandidateOutputFile(root=out, path="public-interface-index.json", role="evidence")
        )

    report_request = ProducerReportRequest(
        candidate_root=out,
        package_id=identity["id"],
        package_version=identity["version"],
        package_api_version=package_api_version,
        spec_paths=tuple(spec_paths),
        output_files=tuple(output_files),
        has_external_inputs=False,
    )
    validation_report_path = ProducerValidationReport(report_request).write()
    diagnostics_report = ProducerDiagnosticsReport(report_request)
    diagnostics_payload = diagnostics_report.payload()
    diagnostics_report_path = diagnostics_report.write()
    output_files.extend(
        [
            CandidateOutputFile(
                root=out,
                path=VALIDATION_REPORT_FILENAME,
                role="validation_report",
            ),
            CandidateOutputFile(
                root=out,
                path=DIAGNOSTICS_REPORT_FILENAME,
                role="diagnostics",
            ),
        ]
    )
    receipt_path = ProducerReceipt(
        ProducerReceiptRequest(
            candidate_root=out,
            package_id=identity["id"],
            package_version=identity["version"],
            package_api_version=package_api_version,
            spec_paths=tuple(spec_paths),
            snapshot_path=out / "harvest.json",
            public_interface_index_path=public_interface_index_path,
            configuration={
                "materialization": "preserve_reviewed_candidate_files",
                "packageId": identity["id"],
                "version": identity["version"],
            },
            output_files=tuple(output_files),
            validation_report_path=validation_report_path,
            diagnostics_report_path=diagnostics_report_path,
            diagnostics_entries=tuple(diagnostics_payload["entries"]),
        )
    ).write()

    return {
        "status": "ok",
        "candidate": str(out),
        "producerReceipt": str(receipt_path),
        "validationReport": str(validation_report_path),
        "diagnosticsReport": str(diagnostics_report_path),
        "specs": spec_paths,
    }


def optional_public_interface_index(root: Path) -> Path | None:
    path = root / "public-interface-index.json"
    return path if path.is_file() else None


def safe_manifest_spec_paths(root: Path, manifest: dict[str, Any]) -> list[str]:
    specs = manifest.get("specs")
    if not isinstance(specs, list):
        raise SystemExit("candidate specpm.yaml must include specs[]")
    spec_paths: list[str] = []
    for entry in specs:
        if not isinstance(entry, dict):
            continue
        value = entry.get("path")
        if not isinstance(value, str) or not value:
            continue
        relative = Path(value)
        if relative.is_absolute() or ".." in relative.parts:
            raise SystemExit(f"candidate spec path escapes bundle: {value}")
        target = (root / relative).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError as exc:
            raise SystemExit(f"candidate spec path escapes bundle: {value}") from exc
        if not target.is_file():
            raise SystemExit(f"candidate spec file is missing: {value}")
        spec_paths.append(relative.as_posix())
    return spec_paths


if __name__ == "__main__":
    raise SystemExit(main())
