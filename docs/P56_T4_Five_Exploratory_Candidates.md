# P56-T4 Five Exploratory Candidate Packages

Date: 2026-09-06. Protocol: `p56-exploratory-authoring/v2`.
Outcome: complete collection with review findings, **not a quality PASS**.

Five fresh `gpt-5.6-luna` agents with medium reasoning each produced one
original candidate. No repair or quality retry ran. Independent SpecPM
validation found zero errors and seven warnings. Pinned source inventories
were unchanged. Human practical-utility review remains pending in T6.

| Repository | Original files | SpecPM warnings | Observed author seconds |
|---|---:|---:|---:|
| openai/codex | 6 | 1 | 218 |
| bitcoin/bitcoin | 7 | 2 | 190 |
| rtk-ai/rtk | 9 | 1 | 328 |
| axios/axios | 7 | 1 | 216 |
| n8n-io/n8n | 9 | 2 | 280 |

Every package is preview-only with a draft boundary. All receive the expected
preview warning; Bitcoin additionally uses unknown interface kind `network_read`
and n8n repeats `instance_ai_configuration` as a document ID. Warnings do not
authorize the protocol's validation-error repair. Originals are unchanged.

## Evidence Findings

- RTK has a material fidelity defect: its purported unchanged runner excerpt
  removes the source's conditional newline behavior. Source/range metadata also
  misses included lines. Its provenance file is retained in our archive but is
  omitted by SpecPM's package-file collection. No actual pack/publish was run.
- Bitcoin has inaccurate excerpt ranges and incomplete packaged evidence for
  its source-supported system-isolation recommendation.
- Codex OS minima/logging claims are supported by `docs/install.md`, but that
  source is absent from the packaged evidence trail. Its CLI/SDK focus is not
  comprehensive app-server coverage; T6 must judge scope usefulness.
- n8n's license excerpt changes tab indentation to spaces, not license wording.
- Axios source hashes and excerpt line membership checked without a detected
  mismatch. This is not exhaustive verification of its semantic claims.

These are bounded static AI/operator findings, not human utility scores. A
read-only audit helper accidentally opened an Axios manifest outside its three
target scope; that read was excluded from its findings and did not change any
author context or output. No exhaustive access audit or runtime test is claimed.

## Retained Artifacts

`SPECS/EVIDENCE/P56-T4/generation-report.json` binds every archive member,
original candidate digest, validation receipt, source identity and timing.
`P56-T4_Original_Candidates.tar.gz` contains all 38 original files, independent
validation/receipts, pinned READMEs and available root license files. Treat code
and YAML as inert, untrusted review content. Upstream licenses remain applicable;
archive inclusion grants no additional rights or publication authority.

`preparation.json` records the frozen skill, source export exclusions, validator
revision and actual permissions. `baseline-lock.json` binds the complete retained
P53-T14 package sets and separately identified semantic records in existing
committed archives. Baselines were frozen before generation, not rerun. Codex
and n8n historical principal boundaries are narrower; semantic bundle IDs differ
from retained candidate bytes. RTK's historical semantic proposal was rejected.
Do not splice these into invented historical materializations.

The author transport was fresh desktop subagents, not the deferred T3 runner.
Requested settings come from spawn arguments; provider token usage and client
version were unavailable, not zero. Times are operator-observed, not hard caps.
Source mode 0444 and instructions do not prove isolation: host access was
unrestricted and network available. Raw prompts/responses were not exported into
this evidence package; this does not assert absence from platform logs.

T5 presents the original, README and both retained baseline types side by side.
T6 records per-question answers, errors/unknowns and source lookups separately
for each surface. T7 reports findings/cost limitations; T8 makes the decision.
Historical v1 gates remain unchanged. No acceptance, registry writes or
publication ran, and no superiority or large-corpus readiness is established.
