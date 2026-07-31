#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from spec_harvester.experimental_intent_calibration import (
    ExperimentalIntentCalibrationOptions,
    run_experimental_intent_calibration,
)
from spec_harvester.semantic_author_pass import CodexSparkSemanticAuthorProvider


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--rubric", type=Path, required=True)
    parser.add_argument("--candidate-root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source-manifest-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--codex-command", default="codex")
    parser.add_argument("--codex-model", default="gpt-5.3-codex-spark")
    parser.add_argument("--timeout-seconds", type=float, default=240.0)
    args = parser.parse_args()
    try:
        report = run_experimental_intent_calibration(
            plan_path=args.plan,
            rubric_path=args.rubric,
            candidate_root=args.candidate_root,
            source_root=args.source_root,
            source_manifest_dir=args.source_manifest_dir,
            provider=CodexSparkSemanticAuthorProvider(
                command=args.codex_command, model=args.codex_model
            ),
            output_path=args.output,
            options=ExperimentalIntentCalibrationOptions(timeout_seconds=args.timeout_seconds),
        )
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}))
        return 2
    print(json.dumps(report["decision"], sort_keys=True))
    return 0 if report["decision"]["p55T10CUnblocked"] else 1


if __name__ == "__main__":
    sys.exit(main())
