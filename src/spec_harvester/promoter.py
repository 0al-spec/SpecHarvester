from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PromoteOptions:
    candidate: Path
    accepted_root: Path
    manifest: Path | None = None
    manifest_entry_path: str | None = None
    package_subdir: str | None = None
    specpm_command: str = "specpm"
    specpm_pythonpath: str | None = None
    skip_validation: bool = False
    force: bool = False


def promote_candidate(options: PromoteOptions) -> dict[str, Any]:
    candidate = options.candidate.resolve()
    if not candidate.is_dir():
        raise ValueError(f"Candidate directory does not exist: {candidate}")
    manifest_path = candidate / "specpm.yaml"
    if not manifest_path.is_file():
        raise ValueError(f"Candidate is missing specpm.yaml: {candidate}")
    reject_symlinks(candidate)

    validation = None
    if not options.skip_validation:
        validation = validate_with_specpm(
            candidate,
            command=options.specpm_command,
            pythonpath=options.specpm_pythonpath,
        )
        if validation.get("status") == "invalid":
            raise ValueError("SpecPM validation failed; candidate was not promoted.")

    identity = read_manifest_identity(manifest_path)
    package_id = identity["id"]
    version = identity["version"]
    package_subdir = options.package_subdir or f"{package_id}/{version}"
    accepted_root = options.accepted_root.resolve()
    destination = resolve_inside(accepted_root, package_subdir)
    if destination is None:
        raise ValueError(f"Package subdir escapes accepted root: {package_subdir}")

    accepted_root.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if not options.force:
            raise ValueError(f"Destination already exists: {destination}")
    copy_candidate_atomically(candidate, destination, force=options.force)

    manifest_result = None
    if options.manifest is not None:
        entry_path = options.manifest_entry_path
        if entry_path is None:
            entry_path = infer_manifest_entry_path(options.manifest, destination)
        manifest_result = append_local_manifest_entry(options.manifest, entry_path)

    return {
        "status": "ok",
        "candidate": str(candidate),
        "destination": str(destination),
        "packageId": package_id,
        "version": version,
        "validationStatus": validation.get("status") if isinstance(validation, dict) else "skipped",
        "manifest": manifest_result,
    }


def validate_with_specpm(
    candidate: Path,
    *,
    command: str,
    pythonpath: str | None = None,
) -> dict[str, Any]:
    argv = shlex.split(command) + ["validate", str(candidate), "--json"]
    env = os.environ.copy()
    if pythonpath:
        existing = env.get("PYTHONPATH")
        env["PYTHONPATH"] = pythonpath if not existing else f"{pythonpath}{os.pathsep}{existing}"
    try:
        completed = subprocess.run(  # noqa: S603
            argv,
            check=False,
            capture_output=True,
            env=env,
            text=True,
        )
    except FileNotFoundError as exc:
        raise ValueError(f"SpecPM command was not found: {command}") from exc

    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "SpecPM validation did not return JSON. "
            f"exit={completed.returncode}, stderr={completed.stderr.strip()}"
        ) from exc

    if completed.returncode != 0 and payload.get("status") != "invalid":
        raise ValueError(
            "SpecPM validation command failed unexpectedly. "
            f"exit={completed.returncode}, stderr={completed.stderr.strip()}"
        )
    return payload


def reject_symlinks(root: Path) -> None:
    for path in root.rglob("*"):
        if path.is_symlink():
            relative = path.relative_to(root).as_posix()
            raise ValueError(f"Candidate contains unsupported symlink: {relative}")


def copy_candidate_atomically(candidate: Path, destination: Path, *, force: bool) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_destination = unique_sibling_path(destination, "tmp")
    backup_destination = unique_sibling_path(destination, "backup")
    backup_created = False
    try:
        shutil.copytree(
            candidate,
            temp_destination,
            symlinks=True,
            ignore=shutil.ignore_patterns(".git", ".DS_Store"),
        )
        if destination.exists():
            if not force:
                raise ValueError(f"Destination already exists: {destination}")
            destination.rename(backup_destination)
            backup_created = True
        temp_destination.rename(destination)
        if backup_created:
            shutil.rmtree(backup_destination)
    except Exception:
        if temp_destination.exists():
            shutil.rmtree(temp_destination)
        if backup_created and backup_destination.exists() and not destination.exists():
            backup_destination.rename(destination)
        raise


def unique_sibling_path(path: Path, suffix: str) -> Path:
    index = 1
    while True:
        candidate = path.with_name(f".{path.name}.{suffix}.{index}")
        if not candidate.exists():
            return candidate
        index += 1


def read_manifest_identity(manifest_path: Path) -> dict[str, str]:
    metadata = read_simple_metadata_block(manifest_path)
    package_id = metadata.get("id")
    version = metadata.get("version")
    if not package_id or not version:
        raise ValueError(f"specpm.yaml is missing metadata.id or metadata.version: {manifest_path}")
    return {"id": package_id, "version": version}


def read_simple_metadata_block(manifest_path: Path) -> dict[str, str]:
    metadata: dict[str, str] = {}
    in_metadata = False
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line == "metadata:":
            in_metadata = True
            continue
        if in_metadata and line and not line.startswith(" "):
            break
        if not in_metadata or not line.startswith("  ") or ":" not in stripped:
            continue
        key, raw_value = stripped.split(":", 1)
        value = parse_yaml_scalar(raw_value.strip())
        if isinstance(value, str):
            metadata[key] = value
    return metadata


def parse_yaml_scalar(value: str) -> str:
    if not value:
        return ""
    if value.startswith(("'", '"')):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return value.strip("'\"")
        return parsed if isinstance(parsed, str) else str(parsed)
    return value


def resolve_inside(root: Path, relative: str) -> Path | None:
    root = root.resolve()
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def infer_manifest_entry_path(manifest: Path, destination: Path) -> str:
    manifest = manifest.resolve()
    destination = destination.resolve()
    roots = [manifest.parent]
    if manifest.parent.name == "public-index":
        roots.insert(0, manifest.parent.parent)
    for root in roots:
        try:
            return destination.relative_to(root.resolve()).as_posix()
        except ValueError:
            continue
    raise ValueError(
        "Could not infer a relative manifest entry path. Pass --manifest-entry-path explicitly."
    )


def append_local_manifest_entry(manifest: Path, entry_path: str) -> dict[str, Any]:
    validate_manifest_entry_path(entry_path)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    entry_line = f"  - path: {entry_path}"
    if not manifest.exists():
        manifest.write_text(f"schemaVersion: 1\npackages:\n{entry_line}\n", encoding="utf-8")
        return {"path": str(manifest), "entry": entry_path, "updated": True}

    text = manifest.read_text(encoding="utf-8")
    lines = text.splitlines()
    if any(line.strip() == f"- path: {entry_path}" for line in lines):
        return {"path": str(manifest), "entry": entry_path, "updated": False}

    package_line_index = find_top_level_packages_line(lines)
    if package_line_index is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend(["packages:", entry_line])
    else:
        package_line = lines[package_line_index]
        stripped = strip_yaml_line_comment(package_line)
        if stripped.startswith("packages:") and stripped.removeprefix("packages:").strip() == "[]":
            lines[package_line_index] = "packages:"
            insert_at = package_line_index + 1
        elif stripped == "packages:":
            insert_at = end_of_packages_block(lines, package_line_index + 1)
        else:
            raise ValueError("Manifest packages field must be a block list or an empty list.")
        lines.insert(insert_at, entry_line)

    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": str(manifest), "entry": entry_path, "updated": True}


def strip_yaml_line_comment(line: str) -> str:
    return line.split("#", 1)[0].strip()


def validate_manifest_entry_path(entry_path: str) -> None:
    if not entry_path or not entry_path.strip():
        raise ValueError("Manifest entry path must be non-empty.")
    if "\n" in entry_path or "\r" in entry_path:
        raise ValueError("Manifest entry path must not contain newlines.")
    if "\x00" in entry_path:
        raise ValueError("Manifest entry path must not contain null bytes.")
    if "\\" in entry_path or (len(entry_path) >= 2 and entry_path[1] == ":"):
        raise ValueError("Manifest entry path must use POSIX-style relative paths.")
    if len(entry_path) > 512:
        raise ValueError("Manifest entry path is too long.")
    path = Path(entry_path)
    if path.is_absolute():
        raise ValueError("Manifest entry path must be relative.")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("Manifest entry path must not contain empty, current, or parent segments.")


def find_top_level_packages_line(lines: list[str]) -> int | None:
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            continue
        if stripped.startswith("packages:"):
            return index
    return None


def end_of_packages_block(lines: list[str], start: int) -> int:
    index = start
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            index += 1
            continue
        if not line.startswith((" ", "\t")):
            break
        index += 1
    return index
