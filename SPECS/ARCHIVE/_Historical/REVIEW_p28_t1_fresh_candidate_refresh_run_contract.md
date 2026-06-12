# REVIEW P28-T1 — Fresh Candidate Refresh Run Contract

Date: 2026-06-12
Verdict: PASS

## Review Subject

P28-T1 adds a producer-side `fresh-candidate-refresh-run` command and
`SpecHarvesterFreshCandidateRefreshRun` artifact for exporting generated
package-set bundles into the SpecPM `prepare-refresh-decision` fresh
generated-root layout.

## Findings

No actionable issues found.

## Checks Reviewed

- Builder and CLI tests cover the `xyflow` package-set smoke fixture.
- Safety coverage rejects escaped candidate paths before copying files.
- Docs-contract tests require the artifact identity, layout, SpecPM consumer
  command, expected artifacts, and authority boundary.
- CLI smoke confirmed normalized output for `xyflow.workspace`,
  `xyflow.react`, `xyflow.svelte`, and `xyflow.system`.

## Residual Risk

The P28-T1 command does not run SpecPM. That is intentional for the authority
boundary. P28-T2 should run the exported fresh root through SpecPM's
`producer-bundle prepare-refresh-decision` helper on a real `xyflow` run after
the SpecPM stacked PRs are available to the target environment.

## Follow-Up

No new follow-up task is required beyond the already recorded Phase 28 tasks:

- `P28-T2` real `xyflow` refresh compare run.
- `P28-T3` second real repository refresh compare run.
