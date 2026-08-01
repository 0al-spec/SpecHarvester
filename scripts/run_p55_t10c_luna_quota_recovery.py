#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from spec_harvester.retained_corpus_semantic_campaign import (
    CODEX_LUNA_MODEL,
    CampaignRunOptions,
    CodexSparkSemanticAuthorProvider,
    initialize_campaign,
    run_campaign_target,
)
from spec_harvester.retained_generic_intent_follow_up import (
    finalize_quota_recovery,
    load_quota_recovery_scope,
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
    parser.add_argument("--initial-report", type=Path, required=True)
    parser.add_argument("--initial-archive", type=Path, required=True)
    parser.add_argument("--work-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--finalize", action="store_true")
    parser.add_argument("--codex-command", default="codex")
    args = parser.parse_args()

    try:
        scope, targets, baseline_records, initial_records = load_quota_recovery_scope(
            initial_report_path=args.initial_report,
            initial_archive_path=args.initial_archive,
            plan_path=args.plan,
            source_manifest_dir=args.source_manifest_dir,
            source_root=args.source_root,
            handoff_root=args.handoff_root,
            readiness_evidence=args.readiness_evidence,
            baseline_report_path=args.baseline_report,
            baseline_archive_path=args.baseline_archive,
        )
        initialize_campaign(args.work_root, scope)
        if args.finalize:
            if args.output is None or args.archive is None:
                raise ValueError("Quota recovery finalization requires --output and --archive")
            report = finalize_quota_recovery(
                scope=scope,
                targets=targets,
                baseline_records=baseline_records,
                initial_records=initial_records,
                work_root=args.work_root,
                output_path=args.output,
                archive_path=args.archive,
            )
            print(json.dumps(report["summary"], sort_keys=True))
            return 0

        provider = CodexSparkSemanticAuthorProvider(
            command=args.codex_command,
            model=CODEX_LUNA_MODEL,
            reasoning_effort="low",
        )
        options = CampaignRunOptions()
        for position, target in enumerate(targets, start=1):
            print(
                json.dumps(
                    {
                        "event": "repository_started",
                        "position": position,
                        "selectedCount": len(targets),
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
