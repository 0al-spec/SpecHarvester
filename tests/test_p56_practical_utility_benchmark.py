from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "SPECS/EVIDENCE/P56-T1/benchmark.json"


def test_frozen_benchmark_has_complete_source_bound_evaluator_cases() -> None:
    benchmark = json.loads(BENCHMARK.read_text())
    assert benchmark["authority"] == "evaluation_only"
    assert benchmark["authoringInputAllowed"] is False
    assert benchmark["schemaVersion"] == 1
    repositories = benchmark["repositories"]
    assert len(repositories) == 5
    assert len({item["repository"] for item in repositories}) == 5
    assert {"openai/codex", "bitcoin/bitcoin"} <= {item["repository"] for item in repositories}
    for repository in repositories:
        assert len(repository["revision"]) == 40
        int(repository["revision"], 16)
        assert repository["scope"]
        sources = repository["sources"]
        assert "README.md" in sources
        for path, sha256 in sources.items():
            assert not PurePosixPath(path).is_absolute()
            assert ".." not in PurePosixPath(path).parts
            assert len(sha256) == 64
            int(sha256, 16)
        questions = repository["questions"]
        assert len(questions) == 5
        assert {item["category"] for item in questions} == {
            "discovery",
            "integration",
            "operations",
            "limitations",
            "evidence",
        }
        for question in questions:
            assert question["question"]
            assert len(question["facts"]) == 2
            assert all(question["facts"])
            assert question["sources"]
            assert set(question["sources"]) <= sources.keys()
            assert set(question["sourceSpans"]) == set(question["sources"])
            for start, end in question["sourceSpans"].values():
                assert isinstance(start, int) and isinstance(end, int)
                assert 1 <= start <= end
    protocol = ROOT / benchmark["protocolPath"]
    assert hashlib.sha256(protocol.read_bytes()).hexdigest() == benchmark["protocolSha256"]
    expected = benchmark.pop("benchmarkSha256")
    canonical = json.dumps(benchmark, sort_keys=True, separators=(",", ":")).encode()
    assert hashlib.sha256(canonical).hexdigest() == expected
