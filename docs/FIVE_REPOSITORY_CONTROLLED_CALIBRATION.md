# Five-Repository Controlled Calibration

Status: P52-T3 live controlled calibration, passed.

P52-T3 validates the first live Phase 52 integration over exactly five
operator-provided pinned local checkouts: Flask, Gin, xyflow, FastAPI, and
FastMCP. It compares deterministic static evidence, an LM Studio control, and
the schema-validated Codex Spark external-model handoff. All model output
remains proposal-only evidence.

The durable compact report is:

```text
tests/fixtures/controlled_calibration/
  p52-t3-five-repository-controlled-calibration.example.json
```

Its SHA-256 digest is:

```text
sha256:9d33c7fec360f131eb564d83815ee6c2ba628fec9a16e1801ea6f990250b85bf
```

## Corpus

The input manifest is
[`inputs/p52-five-repository-calibration/repositories.yml`](../inputs/p52-five-repository-calibration/repositories.yml).
The runner first verified that every checkout existed, was a Git worktree, and
had the manifest's exact revision.

| Repository | Revision | Static-only | LM Studio | Codex Spark |
| --- | --- | --- | --- | --- |
| Flask | `954f5684e4841aad84a8eec7ace7b81a0d3f6831` | passed | completed, warnings | completed |
| Gin | `5f4f9643258dc2a65e684b63f12c8d543c936c67` | passed | completed, warnings | completed |
| xyflow | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` | passed | completed | completed |
| FastAPI | `9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263` | passed | completed, warnings | completed |
| FastMCP | `3b8538e2422a1c43fdb69661c610de7985b785f2` | passed | completed | completed |

## Runner

The `controlled-calibration` command performs these stages in order:

```bash
PYTHONPATH=src python -m spec_harvester controlled-calibration \
  inputs/p52-five-repository-calibration \
  --out <run-root> \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --codex-model gpt-5.3-codex-spark
```

1. It verifies the exactly-five source policy and pinned checkout revisions.
2. It runs the static-only batch before either model path.
3. It calls LM Studio directly for draft and enrichment proposals with
   `response_format.type: json_schema`; no request file is written to the
   durable output.
4. For each Codex call, it creates an ephemeral compact evidence stage,
   invokes `codex exec --sandbox read-only --ephemeral --ignore-user-config
   --skip-git-repo-check`, validates the final message against the P52-T2 JSON
   Schema, and only then uses the existing `--model-output` handoff.

The Codex stage receives no original checkout, writable add-directory,
dependency-installation path, package manager, harvested-code execution path,
or provider endpoint. It retains only bounded receipt fields and proposal
artifacts.

## Results

All five static preflights passed. LM Studio used `openai/gpt-oss-20b` and made
13 proposal calls, consuming 122,284 prompt tokens and 5,076 completion tokens
(127,360 total). Every LM Studio receipt recorded
`responseFormat: json_schema`; SpecHarvester persisted neither raw prompt,
response, nor chain-of-thought data.

Flask, Gin, and FastAPI have proposal-level warning diagnostics such as
`excluded_package_also_selected`, `selected_member_role_unknown`, or
`refined_summary_missing`. These are review signals in proposal sidecars, not
hard failures and not registry changes. xyflow and FastMCP completed without
those diagnostics.

Codex used `gpt-5.3-codex-spark` through `codex-cli 0.145.0`. All five calls
returned exit code `0`, validated against the final-message schema, produced a
repository-specific package-set proposal, and had zero unsupported claims.
The five recorded Codex durations totalled 144,923 ms.

| Quality metric | Required | Result | Verdict |
| --- | ---: | ---: | --- |
| Static completion | >=95% | 100% (5/5) | passed |
| Codex completion | >=90% | 100% (5/5) | passed |
| Schema-valid Codex output | >=98% | 100% (5/5) | passed |
| Repository-specific Codex proposal | >=80% | 100% (5/5) | passed |
| Unsupported claim rate | <=5% | 0% (0/5) | passed |

During the first bounded Codex attempt, Flask and Gin returned a formally valid
but empty `selectedMembers` list. The runner now explicitly requires at least
one selected inventory package for P52's non-empty inventories. The final full
calibration above was rerun with that rule and passed all thresholds.

## Privacy And Authority

The report's privacy fields apply to **SpecHarvester durable artifacts**. The
runner deletes its temporary Codex request, final-message, and evidence-stage
files; it writes no raw prompts, raw model responses, stdout/stderr transcript,
session state, secrets, or chain-of-thought.

LM Studio server logging is operator-managed and outside SpecHarvester's
control. An operator must disable any LM Studio setting that records sensitive
request/response data before treating a live run as provider-log-clean. This
does not alter the proposal-only boundary or the report's statement about
SpecHarvester artifacts.

P52-T3 does not clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code or adapters, accept packages or
relations, publish registry metadata, seed baselines, remove `preview_only`,
or treat static, LM Studio, or Codex output as registry truth.

## Decision

The P52-T3 quality gate is passed and unlocks planning and execution of
P52-T4, the twenty-repository controlled pilot. It does not approve a
50-100 repository corpus, package acceptance, relation acceptance, or registry
promotion.

## References

- [`CONTROLLED_REPOSITORY_CORPUS_PLAN.md`](CONTROLLED_REPOSITORY_CORPUS_PLAN.md)
- [`CODEX_SPARK_EXTERNAL_MODEL_ADAPTER_CONTRACT.md`](CODEX_SPARK_EXTERNAL_MODEL_ADAPTER_CONTRACT.md)
- [`PACKAGE_SET_AI_DRAFT_PROPOSAL.md`](PACKAGE_SET_AI_DRAFT_PROPOSAL.md)
- [`PACKAGE_SET_AI_ENRICHMENT.md`](PACKAGE_SET_AI_ENRICHMENT.md)
