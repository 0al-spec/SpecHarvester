from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.codegraph_source_graph import (
    CodeGraphSourceGraphOptions,
    SourceGraphIndexPayload,
    file_sha256,
    object_list,
)

COMPATIBILITY_REPORT_KIND = "SpecHarvesterCodeGraphCompatibilityReport"
COMPATIBILITY_FIXTURE_KIND = "SpecHarvesterCodeGraphCompatibilityFixture"
COMPATIBILITY_SCHEMA_VERSION = 1
REQUIRED_JSON_COMMANDS = (
    "status",
    "query",
    "files",
    "callers",
    "callees",
    "impact",
    "affected",
)
EXPECTED_PACKAGE_METADATA = {
    "name": "@colbymchenry/codegraph",
    "version": "0.9.7",
    "integrity": (
        "sha512-sBZnnKGkUdmM3BOkvfFq6wdK2OC/sA7nLMh28voan82xFzRp8irEVCakywfOXfDE4bkVMod"
        "Wvucz85f3+YMO6w=="
    ),
    "shasum": "72131a74720bebf719e13ebcbf37f0554cc6cac0",
    "license": "MIT",
}
EXPECTED_PLATFORM_PACKAGE_METADATA = {
    "name": "@colbymchenry/codegraph-darwin-arm64",
    "version": "0.9.7",
    "integrity": (
        "sha512-bQSQSBAeC2HRC4A0wH/T1sOxvLgtNlc7pIjz6vV03ccg0T7zhD0WfyO+HTQRdD1RzAdAILh"
        "IB1TJpCQsREoHrg=="
    ),
    "shasum": "303af1dd3152a6024615ea4ae8c09007239273af",
}


@dataclass(frozen=True)
class CodeGraphCompatibilityOptions:
    fixture: Path
    executable: Path | None = None
    timeout_seconds: int = 5


@dataclass(frozen=True)
class CodeGraphCompatibilityReport:
    options: CodeGraphCompatibilityOptions

    def payload(self) -> dict[str, Any]:
        fixture = CodeGraphCompatibilityFixture(self.options.fixture)
        checks = [
            fixture.identity_check(),
            fixture.package_metadata_check(),
            fixture.binary_contract_check(),
            fixture.required_commands_check(),
            fixture.normalized_mapping_check(),
            self.executable_check(fixture),
        ]
        return {
            "schemaVersion": COMPATIBILITY_SCHEMA_VERSION,
            "kind": COMPATIBILITY_REPORT_KIND,
            "status": report_status(checks),
            "fixture": {
                "path": str(self.options.fixture),
                "sha256": file_sha256(self.options.fixture),
            },
            "package": fixture.package_record(),
            "requiredJsonCommands": fixture.required_command_names(),
            "checks": checks,
            "trustBoundary": [
                (
                    "Compatibility guard reads local fixtures and optional local "
                    "executable metadata only."
                ),
                "No CodeGraph install, npm, npx, network access, or repository indexing occurs.",
                (
                    "Live executable checks are skipped unless an executable path is "
                    "explicitly provided."
                ),
            ],
        }

    def executable_check(self, fixture: CodeGraphCompatibilityFixture) -> dict[str, Any]:
        executable = self.options.executable
        if executable is None:
            return {
                "id": "executable_available",
                "status": "skipped",
                "message": "No CodeGraph executable path provided.",
            }
        if not executable.exists() or not executable.is_file():
            return {
                "id": "executable_available",
                "status": "failed",
                "message": f"CodeGraph executable does not exist: {executable}",
            }
        version_result = CodeGraphExecutableVersionProbe(
            executable=executable,
            fixture=fixture,
            timeout_seconds=self.options.timeout_seconds,
        ).check()
        return version_result


@dataclass(frozen=True)
class CodeGraphCompatibilityFixture:
    path: Path

    def payload(self) -> dict[str, Any]:
        if not self.path.exists() or not self.path.is_file():
            raise ValueError(f"CodeGraph compatibility fixture does not exist: {self.path}")
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise ValueError(f"Unable to read CodeGraph compatibility fixture: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid CodeGraph compatibility fixture JSON: {exc.msg}") from exc
        if not isinstance(payload, dict):
            raise ValueError("CodeGraph compatibility fixture must be a JSON object")
        return payload

    def identity_check(self) -> dict[str, Any]:
        payload = self.payload()
        if (
            payload.get("schemaVersion") == COMPATIBILITY_SCHEMA_VERSION
            and payload.get("kind") == COMPATIBILITY_FIXTURE_KIND
        ):
            return passed_check("fixture_identity", "Fixture identity is supported.")
        return failed_check("fixture_identity", "Fixture identity is unsupported.")

    def package_metadata_check(self) -> dict[str, Any]:
        package = self.package_record()
        missing = [
            key
            for key in EXPECTED_PACKAGE_METADATA
            if not isinstance(package.get(key), str) or not package.get(key)
        ]
        if missing:
            return failed_check(
                "pinned_package_metadata",
                f"Package metadata missing required fields: {', '.join(missing)}",
            )
        mismatches = metadata_mismatches(package, EXPECTED_PACKAGE_METADATA, "package")
        platform_package = package.get("platformPackage")
        if not isinstance(platform_package, dict):
            mismatches.append("platformPackage must be an object")
        else:
            mismatches.extend(
                metadata_mismatches(
                    platform_package,
                    EXPECTED_PLATFORM_PACKAGE_METADATA,
                    "platformPackage",
                )
            )
        if mismatches:
            return failed_check(
                "pinned_package_metadata",
                (
                    "Package metadata does not match pinned CodeGraph release: "
                    f"{', '.join(mismatches)}"
                ),
            )
        return passed_check(
            "pinned_package_metadata",
            f"Fixture pins {package['name']}@{package['version']}.",
        )

    def binary_contract_check(self) -> dict[str, Any]:
        binary = self.binary_record()
        version_command = binary.get("versionCommand")
        if not isinstance(version_command, list) or not all(
            isinstance(item, str) and item for item in version_command
        ):
            return failed_check(
                "binary_availability_contract",
                "Binary contract must declare a string versionCommand array.",
            )
        if binary.get("availability") != "optional_preprovisioned":
            return failed_check(
                "binary_availability_contract",
                "Binary availability must be optional_preprovisioned.",
            )
        environment = binary.get("environment")
        if not isinstance(environment, dict) or environment.get("CODEGRAPH_NO_DOWNLOAD") != "1":
            return failed_check(
                "binary_availability_contract",
                "Binary contract must set CODEGRAPH_NO_DOWNLOAD=1.",
            )
        return passed_check(
            "binary_availability_contract",
            "Binary contract is optional and download-disabled.",
        )

    def required_commands_check(self) -> dict[str, Any]:
        command_records = self.required_command_records()
        missing = [command for command in REQUIRED_JSON_COMMANDS if command not in command_records]
        if missing:
            return failed_check(
                "required_json_cli_commands",
                f"Missing JSON CLI commands: {', '.join(missing)}",
            )
        invalid = [
            command
            for command in REQUIRED_JSON_COMMANDS
            if not command_records[command].declares_json_args(command)
        ]
        if invalid:
            return failed_check(
                "required_json_cli_commands",
                f"Commands must declare their command name and --json args: {', '.join(invalid)}",
            )
        return passed_check(
            "required_json_cli_commands",
            "Fixture declares all required JSON CLI commands.",
        )

    def normalized_mapping_check(self) -> dict[str, Any]:
        sample = self.sample_evidence()
        try:
            payload = SourceGraphIndexPayload(
                CodeGraphSourceGraphOptions(
                    input=self.path,
                    input_format="json",
                    source_target_kind="folder",
                    source_target_path="fixture",
                    analyzer_version=str(self.package_record().get("version") or ""),
                ),
                {
                    "files": object_list(sample.get("files")),
                    "nodes": object_list(sample.get("nodes")),
                    "edges": object_list(sample.get("edges")),
                    "diagnostics": object_list(sample.get("diagnostics")),
                },
            ).payload()
        except ValueError as exc:
            return failed_check("normalized_schema_mapping", str(exc))
        if (
            payload.get("schemaVersion") == "spec-harvester-codegraph-v1"
            and payload.get("kind") == "source_graph_index"
            and payload.get("trust", {}).get("trustLevel") == "untrusted_optional_tool"
        ):
            return {
                **passed_check(
                    "normalized_schema_mapping",
                    "Sample evidence maps into source_graph_index.",
                ),
                "summary": payload.get("summary", {}),
            }
        return failed_check(
            "normalized_schema_mapping",
            "Sample evidence did not produce expected source_graph_index identity.",
        )

    def package_record(self) -> dict[str, Any]:
        package = self.payload().get("package")
        return package if isinstance(package, dict) else {}

    def binary_record(self) -> dict[str, Any]:
        binary = self.payload().get("binary")
        return binary if isinstance(binary, dict) else {}

    def sample_evidence(self) -> dict[str, Any]:
        sample = self.payload().get("sampleEvidence")
        return sample if isinstance(sample, dict) else {}

    def required_command_names(self) -> list[str]:
        return sorted(self.required_command_records())

    def required_command_records(self) -> dict[str, CodeGraphJsonCommandFixture]:
        commands = self.payload().get("requiredJsonCommands")
        records: dict[str, CodeGraphJsonCommandFixture] = {}
        for item in object_list(commands):
            name = item.get("name")
            if isinstance(name, str) and name:
                records[name] = CodeGraphJsonCommandFixture(item)
        return records


@dataclass(frozen=True)
class CodeGraphJsonCommandFixture:
    payload: dict[str, Any]

    def declares_json_args(self, command: str) -> bool:
        args = self.payload.get("args")
        if not isinstance(args, list) or not all(isinstance(item, str) for item in args):
            return False
        return args[:1] == [command] and "--json" in args


@dataclass(frozen=True)
class CodeGraphExecutableVersionProbe:
    executable: Path
    fixture: CodeGraphCompatibilityFixture
    timeout_seconds: int

    def check(self) -> dict[str, Any]:
        command = [str(self.executable), *self.version_command()]
        try:
            completed = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                env=self.environment(),
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return failed_check("executable_version", f"Version probe failed: {exc}")
        output = "\n".join([completed.stdout.strip(), completed.stderr.strip()]).strip()
        expected = str(self.fixture.package_record().get("version") or "")
        if completed.returncode == 0 and expected and expected in output:
            return {
                **passed_check("executable_version", "Executable reports pinned version."),
                "executable": str(self.executable),
                "sha256": file_sha256(self.executable),
                "versionOutput": output,
            }
        return {
            **failed_check(
                "executable_version",
                "Executable version output did not match pinned fixture version.",
            ),
            "executable": str(self.executable),
            "returnCode": completed.returncode,
            "versionOutput": output,
        }

    def version_command(self) -> list[str]:
        command = self.fixture.binary_record().get("versionCommand")
        if not isinstance(command, list):
            return ["--version"]
        return [str(item) for item in command if isinstance(item, str) and item]

    def environment(self) -> dict[str, str]:
        environment = dict(os.environ)
        fixture_environment = self.fixture.binary_record().get("environment")
        if isinstance(fixture_environment, dict):
            for key, value in fixture_environment.items():
                if isinstance(key, str) and isinstance(value, str):
                    environment[key] = value
        environment["CODEGRAPH_NO_DOWNLOAD"] = "1"
        return environment


def build_codegraph_compatibility_report(
    options: CodeGraphCompatibilityOptions,
) -> dict[str, Any]:
    return CodeGraphCompatibilityReport(options).payload()


def write_codegraph_compatibility_report(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def metadata_mismatches(
    actual: dict[str, Any],
    expected: dict[str, str],
    label: str,
) -> list[str]:
    return [
        f"{label}.{key}"
        for key, expected_value in expected.items()
        if actual.get(key) != expected_value
    ]


def report_status(checks: list[dict[str, Any]]) -> str:
    if any(check.get("status") == "failed" for check in checks):
        return "failed"
    return "passed"


def passed_check(identifier: str, message: str) -> dict[str, str]:
    return {"id": identifier, "status": "passed", "message": message}


def failed_check(identifier: str, message: str) -> dict[str, str]:
    return {"id": identifier, "status": "failed", "message": message}
