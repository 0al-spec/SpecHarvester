from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_real_repository_validation.py"

SPEC = importlib.util.spec_from_file_location("run_real_repository_validation", SCRIPT)
assert SPEC is not None
runner = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = runner
SPEC.loader.exec_module(runner)


def _manifest_record(
    identifier: str, *, repository: str = "https://github.com/example/demo"
) -> dict:
    return {
        "id": identifier,
        "repository": repository,
        "revision": "cafebabe",
        "ref": None,
        "checkout": f"/tmp/{identifier}",
        "packageId": f"{identifier}.core",
        "labels": [],
        "sourceManifest": {"path": "repositories.yml", "entryIndex": 0},
    }


def _run_command_success(
    *, command: list[str], cwd: Path, env: dict[str, str] | None, dry_run: bool
) -> runner.CommandResult:
    del cwd, env, dry_run
    return runner.CommandResult(command=command, returncode=0, stdout="", stderr="")


def test_select_repositories_rejects_unknown() -> None:
    with pytest.raises(runner.RealRepositoryValidationError, match="Unknown repository id"):
        runner._select_repositories([_manifest_record("a")], ("a", "missing"))


def test_build_specnode_command_all_placeholders_supported() -> None:
    candidate = Path("/tmp/candidate")
    command = runner._build_specnode_command(
        template="echo {candidate} {bundle} {preview_plan} {result}",
        candidate_dir=candidate,
        bundle_path=candidate / "bundle.json",
        preview_plan_path=candidate / "preview.json",
    )
    assert command == [
        "echo",
        "/tmp/candidate",
        "/tmp/candidate/bundle.json",
        "/tmp/candidate/preview.json",
        "/tmp/candidate/specnode-refinement-result.json",
    ]


def test_build_specnode_command_missing_template_data_fails() -> None:
    with pytest.raises(runner.RealRepositoryValidationError, match="missing required placeholder"):
        runner._build_specnode_command(
            template="echo {candidate} {missing}",
            candidate_dir=Path("/tmp/candidate"),
            bundle_path=None,
            preview_plan_path=None,
        )


def test_parse_args_uses_defaults_and_flags(tmp_path: Path) -> None:
    args = runner.parse_args(["--out", str(tmp_path), "--strict-exit", "--dry-run"])
    assert args.out == tmp_path
    assert args.strict_exit is True
    assert args.dry_run is True
    assert args.no_specnode_artifacts is False


def test_build_draft_summary_extracts_generated_artifacts(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    specs = candidate / "specs"
    specs.mkdir(parents=True)
    (candidate / "harvest.json").write_text(
        '{"kind":"SpecHarvesterEvidenceSnapshot","source":{"repository":"https://github.com/example/demo","revision":"abc"}}',
        encoding="utf-8",
    )
    (candidate / "specpm.yaml").write_text(
        "\n".join(
            [
                "apiVersion: specpm.dev/v0.1",
                "kind: SpecPackage",
                "metadata:",
                "  id: demo.core",
                "  name: Demo",
                "  version: 0.1.0",
                "  summary: Demo package",
                "  license: MIT",
                "specs:",
                "  - path: specs/demo.spec.yaml",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (specs / "demo.spec.yaml").write_text(
        "\n".join(
            [
                "apiVersion: specpm.dev/v0.1",
                "kind: BoundarySpec",
                "intent:",
                "  summary: Demo boundary intent",
                "provides:",
                "  capabilities:",
                "    - id: demo.core.parse",
                "      role: primary",
                "      summary: Parse demo input",
                "evidence:",
                "  - id: harvest_snapshot",
                "    supports:",
                "      - intent.summary",
                "      - provides.capabilities.demo.core.parse",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = runner._build_draft_summary(candidate)

    assert summary["kind"] == "SpecHarvesterDraftSummary"
    assert summary["sourceArtifacts"] == ["specpm.yaml", "specs/demo.spec.yaml"]
    assert summary["candidate"]["intent"] == "Demo boundary intent"
    assert summary["candidate"]["capabilities"] == [
        {
            "id": "demo.core.parse",
            "evidenceSources": ["specpm.yaml", "specs/demo.spec.yaml"],
        }
    ]


def test_run_validation_dry_run_supports_select_and_no_candidate_checking(tmp_path: Path) -> None:
    manifest_records = [_manifest_record("alpha"), _manifest_record("beta")]
    args = runner.parse_args(
        [
            "--inputs",
            str(tmp_path / "inputs"),
            "--out",
            str(tmp_path / "out"),
            "--select",
            "beta",
            "--dry-run",
            "--skip-specpm-validation",
            "--skip-governance-reports",
            "--skip-smoke-triage",
            "--no-specnode-artifacts",
        ]
    )
    commands: list[list[str]] = []

    def fake_run_command(
        *, command: list[str], cwd: Path, env: dict[str, str] | None, dry_run: bool
    ) -> runner.CommandResult:
        del cwd, env, dry_run
        commands.append(command)
        return runner.CommandResult(command=command, returncode=0, stdout="", stderr="")

    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(runner, "read_repository_source_manifests", lambda path: manifest_records)
    monkeypatch.setattr(runner, "run_command", fake_run_command)
    try:
        report = runner.run_validation(args)
    finally:
        monkeypatch.undo()

    assert report["status"] == "ok"
    assert report["runReport"] == str(tmp_path / "out" / "run-report.json")
    assert report["selected"] == ["beta"]
    assert report["packageCount"] == 1
    assert len(report["packages"]) == 1
    collect_batch_command = next(
        step["command"] for step in report["steps"] if step["step"] == "collect-batch"
    )
    assert "--select" in collect_batch_command
    assert collect_batch_command[-1] == "beta"
    assert len(commands) >= 2


def test_main_writes_default_run_report(tmp_path: Path) -> None:
    manifest_records = [_manifest_record("alpha")]

    def fake_run_command(
        *, command: list[str], cwd: Path, env: dict[str, str] | None, dry_run: bool
    ) -> runner.CommandResult:
        del cwd, env, dry_run
        return runner.CommandResult(command=command, returncode=0, stdout="", stderr="")

    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(runner, "read_repository_source_manifests", lambda path: manifest_records)
    monkeypatch.setattr(runner, "run_command", fake_run_command)
    try:
        result = runner.main(
            [
                "--inputs",
                str(tmp_path / "inputs"),
                "--out",
                str(tmp_path / "out"),
                "--dry-run",
                "--skip-specpm-validation",
                "--skip-governance-reports",
                "--skip-smoke-triage",
                "--no-specnode-artifacts",
            ]
        )
    finally:
        monkeypatch.undo()

    report_path = tmp_path / "out" / "run-report.json"
    assert result == 0
    assert report_path.exists()


def test_main_writes_error_run_report(tmp_path: Path) -> None:
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(runner, "read_repository_source_manifests", lambda path: [])
    try:
        result = runner.main(
            [
                "--inputs",
                str(tmp_path / "inputs"),
                "--out",
                str(tmp_path / "out"),
                "--dry-run",
            ]
        )
    finally:
        monkeypatch.undo()

    report_path = tmp_path / "out" / "run-report.json"
    assert result == 2
    assert report_path.exists()
    assert '"status": "error"' in report_path.read_text(encoding="utf-8")


def test_run_validation_optional_steps_are_degraded_without_strict_exit(tmp_path: Path) -> None:
    args = runner.parse_args(
        [
            "--inputs",
            str(tmp_path / "inputs"),
            "--out",
            str(tmp_path / "out"),
            "--dry-run",
            "--skip-specpm-validation",
            "--skip-governance-reports",
            "--skip-smoke-triage",
            "--specnode-command",
            "echo --specnode-step",
            "--select",
            "alpha",
        ]
    )

    def fake_run_command(
        *, command: list[str], cwd: Path, env: dict[str, str] | None, dry_run: bool
    ) -> runner.CommandResult:
        del cwd, env, dry_run
        if command[:2] == ["echo", "--specnode-step"]:
            return runner.CommandResult(command=command, returncode=3, stdout="", stderr="")
        return runner.CommandResult(command=command, returncode=0, stdout="", stderr="")

    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(
        runner, "read_repository_source_manifests", lambda path: [_manifest_record("alpha")]
    )
    monkeypatch.setattr(runner, "run_command", fake_run_command)
    try:
        report = runner.run_validation(args)
    finally:
        monkeypatch.undo()

    assert report["status"] == "degraded"
    package = report["packages"][0]
    assert package["status"] == "degraded"
    assert package["nonFatalFailures"][0]["step"] == "specnode"
    assert report["nonFatalFailures"][0]["step"] == "specnode"


def test_run_validation_optional_steps_fail_fast_when_strict_exit(tmp_path: Path) -> None:
    args = runner.parse_args(
        [
            "--inputs",
            str(tmp_path / "inputs"),
            "--out",
            str(tmp_path / "out"),
            "--dry-run",
            "--strict-exit",
            "--skip-specpm-validation",
            "--skip-governance-reports",
            "--skip-smoke-triage",
            "--specnode-command",
            "echo --specnode-step",
            "--select",
            "alpha",
        ]
    )

    def fake_run_command(
        *, command: list[str], cwd: Path, env: dict[str, str] | None, dry_run: bool
    ) -> runner.CommandResult:
        del cwd, env, dry_run
        if command[:2] == ["echo", "--specnode-step"]:
            return runner.CommandResult(command=command, returncode=3, stdout="", stderr="")
        return runner.CommandResult(command=command, returncode=0, stdout="", stderr="")

    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(
        runner, "read_repository_source_manifests", lambda path: [_manifest_record("alpha")]
    )
    monkeypatch.setattr(runner, "run_command", fake_run_command)
    try:
        with pytest.raises(
            runner.RealRepositoryValidationError,
            match="external specnode command failed",
        ):
            runner.run_validation(args)
    finally:
        monkeypatch.undo()
