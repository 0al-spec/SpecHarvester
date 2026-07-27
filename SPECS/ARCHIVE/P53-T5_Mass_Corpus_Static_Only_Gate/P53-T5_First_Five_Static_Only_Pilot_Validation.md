# P53-T5 First-Five Static-Only Pilot Validation

Date: 2026-07-27
Status: Passed as a bounded pilot; full P53-T5 remains open

## Scope

This run covered five pinned P53 repositories:

- `public-apis-public-apis`
- `freecodecamp-freecodecamp`
- `affaan-m-ecc`
- `spf13-cobra`
- `ultraworkers-claw-code`

The run used the existing `autonomous-candidate-batch` path with `--skip-ai`.
It was static-only and preview-only: no AI provider, Codex worker, repository
plugin adapter, trusted local adapter, package manager, dependency installation,
build, or registry mutation was allowed.

## Command

```text
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch inputs/p53-mass-corpus \
  --out /tmp/p53-t5-first-five-static-only \
  --select public-apis-public-apis \
  --select freecodecamp-freecodecamp \
  --select affaan-m-ecc \
  --select spf13-cobra \
  --select ultraworkers-claw-code \
  --skip-ai \
  --repository-profile-selection auto
```

## Results

| Measure | Result |
| --- | ---: |
| Batch status | `passed` |
| Selected / processed repositories | `5 / 5` |
| Static collection status | `ok` |
| Collected repositories | `5` |
| Failed repositories | `0` |
| Preflight passes | `5` |
| Profile detections | `5` |
| Profile selected / fallback | `3 / 2` |
| AI mode | `disabled` (`operator_disabled`) |
| AI draft proposals | `0` |
| AI enrichment proposals | `0` |
| Adapter evidence sidecars | `0` |
| Authority | `producer_preview_evidence_only` |

The batch inventory correctly skipped the other `95` repositories. The raw
runtime artifacts remain at `/tmp/p53-t5-first-five-static-only` for local
inspection; the repository records the reproducible command and disposition,
not machine-local temporary output.

## Disposition

The five-repository static-only pilot is acceptable as evidence to continue the
bounded rollout. It does not by itself complete the full 100-repository
P53-T5 gate. The next decision is to review the collected artifact quality and
then either expand to the remaining wave-one repositories or record a focused
follow-up before scaling.
