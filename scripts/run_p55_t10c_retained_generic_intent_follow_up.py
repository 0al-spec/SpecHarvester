#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from spec_harvester.retained_corpus_semantic_campaign import (
    CODEX_SPARK_MODEL,
    CampaignRunOptions,
    CodexSparkSemanticAuthorProvider,
    initialize_campaign,
    run_campaign_target,
)
from spec_harvester.retained_generic_intent_follow_up import (
    build_follow_up_plan,
    finalize_follow_up,
    load_follow_up_scope,
    write_follow_up_plan,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--source-manifest-dir", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--handoff-root", type=Path, required=True)
    parser.add_argument("--readiness-evidence", type=Path, required=True)
    parser.add_argument("--baseline-report", type=Path, required=True)
    parser.add_argument("--baseline-archive", type=Path, required=True)
    parser.add_argument("--work-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--review-sample", type=Path)
    parser.add_argument("--repository", action="append")
    parser.add_argument("--freeze-plan", action="store_true")
    parser.add_argument("--finalize", action="store_true")
    parser.add_argument("--codex-command", default="codex")
    parser.add_argument("--codex-model", default=CODEX_SPARK_MODEL)
    args = parser.parse_args()

    common = {
        "source_manifest_dir": args.source_manifest_dir,
        "source_root": args.source_root,
        "handoff_root": args.handoff_root,
        "readiness_evidence": args.readiness_evidence,
        "baseline_report_path": args.baseline_report,
        "baseline_archive_path": args.baseline_archive,
    }
    try:
        if args.codex_model != CODEX_SPARK_MODEL:
            raise ValueError(f"P55-T10C requires Codex model {CODEX_SPARK_MODEL}")
        if args.freeze_plan:
            if (
                any(
                    value is not None
                    for value in (args.work_root, args.output, args.archive, args.review_sample)
                )
                or args.finalize
                or args.repository
            ):
                raise ValueError("Plan freezing cannot run or finalize targets")
            plan, _scope, _targets, _records = build_follow_up_plan(**common)
            write_follow_up_plan(args.plan, plan)
            print(
                json.dumps({"targetCount": len(plan["targets"]), "planSha256": plan["planSha256"]})
            )
            return 0

        if args.work_root is None:
            raise ValueError("P55-T10C execution requires --work-root")
        scope, targets, baseline_records = load_follow_up_scope(plan_path=args.plan, **common)
        initialize_campaign(args.work_root, scope)
        if args.finalize:
            if (
                args.repository
                or args.output is None
                or args.archive is None
                or args.review_sample is None
            ):
                raise ValueError("Full finalization requires output, archive, and review sample")
            report = finalize_follow_up(
                scope=scope,
                targets=targets,
                baseline_records=baseline_records,
                work_root=args.work_root,
                output_path=args.output,
                archive_path=args.archive,
                review_sample_path=args.review_sample,
            )
            print(json.dumps(report["summary"], sort_keys=True))
            return 0

        selected = [
            target
            for target in targets
            if not args.repository or target.repository_id in args.repository
        ]
        if not selected:
            raise ValueError("P55-T10C subset selected no repositories")
        provider = CodexSparkSemanticAuthorProvider(
            command=args.codex_command, model=args.codex_model
        )
        options = CampaignRunOptions()
        for position, target in enumerate(selected, start=1):
            print(
                json.dumps(
                    {
                        "event": "repository_started",
                        "position": position,
                        "selectedCount": len(selected),
                        "repositoryId": target.repository_id,
                    },
                    sort_keys=True,
                ),
                file=sys.stderr,
                flush=True,
            )
            record = run_campaign_target(
                target,
                scope=scope,
                work_root=args.work_root,
                provider=provider,
                options=options,
            )
            print(
                json.dumps(
                    {
                        "event": "repository_finished",
                        "repositoryId": target.repository_id,
                        "status": record["status"],
                        "qualityStatus": record.get("qualityReport", {}).get("status"),
                    },
                    sort_keys=True,
                ),
                file=sys.stderr,
                flush=True,
            )
        return 0
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
