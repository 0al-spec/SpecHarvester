#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from spec_harvester.retained_corpus_semantic_campaign import (
    CampaignRunOptions,
    CodexSparkSemanticAuthorProvider,
    finalize_campaign,
    initialize_campaign,
    load_campaign_scope,
    run_campaign_target,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-manifest-dir", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--handoff-root", type=Path, required=True)
    parser.add_argument("--readiness-evidence", type=Path, required=True)
    parser.add_argument("--work-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--wave", action="append")
    parser.add_argument("--repository", action="append")
    parser.add_argument("--finalize", action="store_true")
    parser.add_argument("--codex-command", default="codex")
    parser.add_argument("--codex-model", default="gpt-5.3-codex-spark")
    parser.add_argument("--timeout-seconds", type=float, default=300)
    parser.add_argument("--json-repair-max-attempts", type=int, default=1)
    parser.add_argument("--provider-max-attempts", type=int, default=2)
    args = parser.parse_args()

    try:
        scope, targets = load_campaign_scope(
            source_manifest_dir=args.source_manifest_dir,
            source_root=args.source_root,
            handoff_root=args.handoff_root,
            readiness_evidence=args.readiness_evidence,
        )
        initialize_campaign(args.work_root, scope)
        if args.finalize:
            if args.wave or args.repository or args.output is None or args.archive is None:
                raise ValueError("Full finalization requires output and archive without subsets")
            report = finalize_campaign(
                scope=scope,
                targets=targets,
                work_root=args.work_root,
                output_path=args.output,
                archive_path=args.archive,
            )
            print(json.dumps(report["summary"], sort_keys=True))
            return 0

        selected = [
            target
            for target in targets
            if (not args.wave or target.wave in args.wave)
            and (not args.repository or target.repository_id in args.repository)
        ]
        if not selected:
            raise ValueError("Campaign subset selected no repositories")
        provider = CodexSparkSemanticAuthorProvider(
            command=args.codex_command, model=args.codex_model
        )
        options = CampaignRunOptions(
            timeout_seconds=args.timeout_seconds,
            json_repair_max_attempts=args.json_repair_max_attempts,
            provider_max_attempts=args.provider_max_attempts,
        )
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
