# P53-T5 First-Five Static-Only Pilot

## Objective

Run the first five P53 wave-1 repositories through the existing deterministic
static collection path. This is a bounded pilot inside P53-T5, not completion
of the full 100-repository task.

## Selected Sources

- `public-apis-public-apis`
- `freecodecamp-freecodecamp`
- `affaan-m-ecc`
- `spf13-cobra`
- `ultraworkers-claw-code`

## Required Boundaries

- Use `--skip-ai`.
- Do not invoke Codex, LM Studio, adapters, package managers, or harvested code.
- Keep output proposal/preview-only and do not mutate registry truth.
- Preserve pinned source revision and checkout provenance in every record.

## Deliverables

- One static-only batch report for exactly five selected repositories.
- Deterministic collected snapshots and preview candidate evidence.
- Execution-boundary summary and failure/skip reasons.
- Validation report recording the exact command and observed counts.

## Acceptance

- Exactly five selected IDs are processed.
- Static collection completes or records bounded per-source failures.
- AI is disabled and no adapter/package-manager/code execution occurs.
- Full static-only output remains preview-only and unaccepted.
