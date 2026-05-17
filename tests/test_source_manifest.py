from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.cli import main
from spec_harvester.source_manifest import read_repository_source_manifests


def test_read_repository_source_manifests_normalizes_enabled_entries_deterministically(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    (inputs / "z.yml").write_text(
        """
repositories:
  - id: zeta
    repository: https://github.com/example/zeta
    revision: zzz
    checkout: ../checkouts/zeta
    packageId: zeta.core
    labels: [python, docs]
  - id: disabled
    repository: https://github.com/example/disabled
    revision: ddd
    enabled: false
""",
        encoding="utf-8",
    )
    (inputs / "a.yml").write_text(
        """
repositories:
  - id: alpha
    repository: git@github.com:example/alpha.git
    ref: main
""",
        encoding="utf-8",
    )

    records = read_repository_source_manifests(inputs)

    assert records == [
        {
            "id": "alpha",
            "repository": "git@github.com:example/alpha.git",
            "revision": None,
            "ref": "main",
            "checkout": None,
            "packageId": None,
            "labels": [],
            "sourceManifest": {"path": "a.yml", "entryIndex": 0},
        },
        {
            "id": "zeta",
            "repository": "https://github.com/example/zeta",
            "revision": "zzz",
            "ref": None,
            "checkout": "../checkouts/zeta",
            "packageId": "zeta.core",
            "labels": ["docs", "python"],
            "sourceManifest": {"path": "z.yml", "entryIndex": 0},
        },
    ]


def test_read_repository_source_manifests_can_include_disabled_entries(tmp_path: Path) -> None:
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    (inputs / "repos.yml").write_text(
        """
repositories:
  - id: disabled
    repository: https://github.com/example/disabled
    revision: ddd
    enabled: false
""",
        encoding="utf-8",
    )

    assert read_repository_source_manifests(inputs) == []
    assert read_repository_source_manifests(inputs, include_disabled=True)[0]["id"] == "disabled"


def test_read_repository_source_manifests_rejects_duplicate_ids(tmp_path: Path) -> None:
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    for name in ("a.yml", "b.yml"):
        (inputs / name).write_text(
            """
repositories:
  - id: duplicate
    repository: https://github.com/example/repo
    revision: abc
""",
            encoding="utf-8",
        )

    with pytest.raises(ValueError, match="Duplicate repository id"):
        read_repository_source_manifests(inputs)


def test_read_repository_source_manifests_rejects_duplicate_keys_per_entry(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    (inputs / "repos.yml").write_text(
        """
repositories:
  - id: demo
    id: changed
    repository: https://github.com/example/demo
    revision: abc
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="duplicate key 'id'; first defined on line 3"):
        read_repository_source_manifests(inputs)


def test_read_repository_source_manifests_rejects_invalid_shapes(tmp_path: Path) -> None:
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    (inputs / "invalid.yml").write_text(
        """
repositories:
  - id: invalid
    repository: ssh://github.com/example/repo
    revision: abc
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="unsupported repository URL"):
        read_repository_source_manifests(inputs)

    (inputs / "invalid.yml").write_text(
        """
repositories:
  - id: missing-revision
    repository: https://github.com/example/repo
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="requires exactly one of revision or ref"):
        read_repository_source_manifests(inputs)

    (inputs / "invalid.yml").write_text("repositories:\n    id: bad\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unsupported indentation"):
        read_repository_source_manifests(inputs)


def test_cli_source_manifests_prints_deterministic_json(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    (inputs / "repos.yml").write_text(
        """
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc123
""",
        encoding="utf-8",
    )

    result = main(["source-manifests", str(inputs)])

    assert result == 0
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "ok"
    assert output["repositoryCount"] == 1
    assert output["repositories"][0]["id"] == "demo"


def test_read_repository_source_manifests_rejects_missing_input_directory(
    tmp_path: Path,
) -> None:
    with pytest.raises(ValueError, match="directory does not exist"):
        read_repository_source_manifests(tmp_path / "missing")


def test_read_repository_source_manifests_rejects_malformed_yaml_subset(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    manifest = inputs / "repos.yml"

    manifest.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="manifest is empty"):
        read_repository_source_manifests(inputs)

    manifest.write_text("sources:\n  - id: demo\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expected top-level repositories list"):
        read_repository_source_manifests(inputs)

    manifest.write_text("repositories:\n", encoding="utf-8")
    with pytest.raises(ValueError, match="repositories must contain at least one entry"):
        read_repository_source_manifests(inputs)

    manifest.write_text("repositories:\n- id: demo\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unsupported indentation"):
        read_repository_source_manifests(inputs)

    manifest.write_text("repositories:\n  - id\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expected key: value"):
        read_repository_source_manifests(inputs)

    manifest.write_text("repositories:\n  - : demo\n", encoding="utf-8")
    with pytest.raises(ValueError, match="key must be non-empty"):
        read_repository_source_manifests(inputs)


def test_read_repository_source_manifests_rejects_bad_field_types(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    manifest = inputs / "repos.yml"

    manifest.write_text(
        """
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    unexpected: value
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="unsupported keys"):
        read_repository_source_manifests(inputs)

    manifest.write_text(
        """
repositories:
  - id:
    repository: https://github.com/example/demo
    revision: abc
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="id must be a non-empty string"):
        read_repository_source_manifests(inputs)

    manifest.write_text(
        """
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    enabled: yes
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="enabled must be a boolean"):
        read_repository_source_manifests(inputs)

    manifest.write_text(
        """
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    labels: docs
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="labels must be a list of strings"):
        read_repository_source_manifests(inputs)

    manifest.write_text(
        """
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout:
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="checkout must be a non-empty string"):
        read_repository_source_manifests(inputs)

    manifest.write_text(
        """
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    ref: main
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="requires exactly one of revision or ref"):
        read_repository_source_manifests(inputs)


def test_read_repository_source_manifests_parses_comments_quotes_and_empty_lists(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    (inputs / "repos.yml").write_text(
        """
# comment before document
repositories:
  - id: "demo#literal" # trailing comment
    repository: "https://github.com/example/demo"
    revision: abc
    packageId: 'demo.core'
    labels: []
    enabled: true
""",
        encoding="utf-8",
    )

    records = read_repository_source_manifests(inputs)

    assert records[0]["id"] == "demo#literal"
    assert records[0]["packageId"] == "demo.core"
    assert records[0]["labels"] == []


def test_read_repository_source_manifests_treats_apostrophes_as_plain_scalar_data(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    (inputs / "repos.yml").write_text(
        """
repositories:
  - id: demo
    repository: https://github.com/example/o'connor # trailing comment
    revision: abc'def # trailing comment
""",
        encoding="utf-8",
    )

    records = read_repository_source_manifests(inputs)

    assert records[0]["repository"] == "https://github.com/example/o'connor"
    assert records[0]["revision"] == "abc'def"
