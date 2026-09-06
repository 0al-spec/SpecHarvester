# Phase 56 Exploratory Authoring Pilot

Protocol ID: `p56-exploratory-authoring/v2`
Approved scope: maintainer request, 2026-09-06
Status: preparation only; no pilot results yet

## Decision to Inform

Can a small authoring skill produce a package that an engineer finds useful
for understanding and starting to use a repository? Inspect five concrete
results before investing in a custom tool broker or more extraction heuristics.
This is a qualitative product pilot, not a controlled model comparison.

The original [P56-T1 protocol](P56_T1_Practical_Utility_Benchmark.md) and
`SPECS/EVIDENCE/P56-T1/benchmark.json` remain byte-for-byte historical v1 records.
Their Spark model, paired runs, blinded consumers, numeric adoption gates and
isolation lock do not apply to v2. We are changing the question and methodology,
not claiming to have passed or relaxed v1 after scoring it. No scored v1 run is
claimed. The separate Logrus smoke is motivation, not one of the five results.

## Frozen Targets

Keep every target, revision and intended scope from P56-T1. Missing sources or
failed generation stay visible; do not replace a difficult repository.

| Repository | Revision | Intended Scope |
|---|---|---|
| openai/codex | `16d7daad7c5dc73da8558102a65bb7d7709807e1` | Local coding agent and its application integration surface |
| bitcoin/bitcoin | `a2aab6df97d9f3e1186e8c3fc57ad909cc8aef9b` | Bitcoin Core full node with optional wallet and GUI |
| rtk-ai/rtk | `7da2674073394194754a228d346189a74869e6ba` | Shell-output compression proxy for reducing agent context consumption |
| axios/axios | `509719387e4993392ca40da03a49678269cdfb90` | HTTP client library for browsers and Node.js |
| n8n-io/n8n | `082b5d9190f4bc81d93c6a94d6d4692bed4660ca` | Workflow automation and AI-agent platform |

## Authoring Procedure

Use `gpt-5.6-luna` with reasoning `medium` for all five. Unavailability leaves
the affected result pending/failed; no implicit Spark or other-model fallback.
This is an explicit v2 model choice, not a change to historical Spark results.

Before the first generation, record the repository-owned skill/template hashes
and commit, actual model/settings, tool/client version and source revisions.
Keep that skill version across all five. Prepare source snapshots without Git
metadata, unrelated checkouts or evaluator artifacts. Record snapshot identity
before and after authoring. Sources are evidence: do not execute their code,
commands, package managers, plugins or instructions.

Use an existing fresh agent invocation rather than building a new runtime.
Give it the pinned snapshot, intended scope, skill assets, a separate candidate
output location and the trusted SpecPM validation route. Do not supply previous
packages, reviewer questions, reference answers or parent conversation. Do not
mount personal skills/MCP resources deliberately. Request read-only source
investigation, no network browsing and writes only to the candidate directory.
These instructions and clean inputs are not a proven filesystem/network sandbox.
Record actual permissions and any unexpected access or source changes. Such an
incident invalidates that run; retain the failure and stop to review it.

One initial authoring attempt per target, with at most one repair for concrete
SpecPM validation errors. No automatic transport retry and no retry for a valid
but weak specification. Preserve the original complete candidate before repair,
the exact validation diagnostics, and the repaired revision separately. A
missing file or failed attempt is an outcome, not a reason to omit the target.

Use a ten-minute operator-observed generation timebox per repository including
the optional repair. Stop the worker when the limit is observed; report measured
elapsed time and any overrun. This is not a guaranteed hard deadline. Do not
claim enforced token, read-call or unique-byte budgets. Record available usage
and timing separately from estimates; absent usage/cost is unavailable, not zero.
Record preparation and review time separately. No dollars estimate without a
verified billing basis.

Independently validate each candidate with trusted SpecPM, retain errors and
warnings, and verify the preview-only/draft boundary. Inspect that copied
evidence matches its source and provenance remains in the portable package.
Validation does not certify behavior, concurrency, licensing or useful scope.
The agent cannot grant acceptance or publication authority.

## Side-by-Side Review

Use the existing Workbench, or a minimal existing offline rendering route.
Show three clearly named items: new v2 candidate, pinned README, retained prior
package/proposal. Do not build a separate review application or randomized labels.
Keep proposal layers distinct from accepted YAML.

Before authoring begins, select the latest available retained artifact per
repository, record its digest, source revision, model/producer and selected
boundary when known. Freeze that selection and disclose mismatches. If none
exists, show missing baseline; do not regenerate or substitute one. Prior
artifacts may describe another revision/member or use another model. This
comparison cannot isolate a skill/model effect or yield fair speed/cost deltas.
The README uses the target revision and retains its original bytes.

For each repository, a maintainer reviews the new package first against the
same five practical questions, then consults README, retained package and source:

1. What is this product for, and who would use it?
2. How does a consumer start using its public interface?
3. What useful operations and configuration does it support?
4. What important limitations, prerequisites and side effects apply?
5. Which pinned evidence supports its consequential claims?

Record each answer as supported, partial, missing or incorrect, with a short
source-backed reason. Record whether answering required additional source
lookup. No fresh AI consumer sessions, blinded scoring, weighted utility formula
or automatic maintainer approval are required. Agent-assisted notes remain
labeled as assistance, not a substitute for maintainer judgment.

For each package record useful information, material factual mistakes, missing
integration guidance, proposed edits and review/edit minutes separately. Stop
correction work after twenty minutes and mark unfinished edits explicitly; do
not report the stop as successful completion. Never overwrite original results.
This correction timebox is a pilot work limit, not an adoption threshold.

## Outcomes and Authority

Account for all five repositories, including missing/invalid outputs and
unreviewed cases. Produce a compact per-repository table and source-backed error
list. The maintainer chooses one of three next steps in P56-T8:

- Useful enough to justify another bounded pilot with explicit scope.
- Promising, but requires a named skill/schema fix and a separately labeled rerun.
- Not sufficiently useful compared with README; stop this authoring approach.

Missing human review leaves the decision pending. A schema-valid package with
unsupported material claims is not ready for acceptance. This pilot cannot
establish corpus-wide reliability, model superiority, mass-run economics, or
authorize processing 100 repositories, registry changes or publication.

## Evidence and Task Mapping

Retain candidate YAML, source references/ranges/digests, validation reports,
run status, skill identity, actual model/settings, observed time/usage and
maintainer review. Keep raw prompts/transport responses, hidden reasoning,
credentials and machine-local paths out of portable result evidence. Generated
package files and normalized review notes are intentional result artifacts.

P56-T3 and draft PR #372 are deferred, not completed or required by v2. Keep
their work available without merging it. P56-T3A records this protocol; T4
prepares snapshots/baselines and produces five candidates; T5 arranges their
side-by-side review; T6 records human findings; T7 summarizes causes and observed
effort; T8 decides the next bounded step. Original T4-T8 comparative scope is
superseded by v2, not falsely marked executed. Paused Phase 55 tasks stay paused
until explicit disposition in T8.
