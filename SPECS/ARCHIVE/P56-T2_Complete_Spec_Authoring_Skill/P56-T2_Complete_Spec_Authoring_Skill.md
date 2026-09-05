# P56-T2 Complete Spec Authoring Contract and Repository Skill

## Objective

Provide a self-contained source-investigating authoring skill and complete,
valid SpecPM templates without extending the analyzer or running the experiment.

## Deliverables

- Repository-owned skill with bounded input/output and candidate-only authority.
- Supported-field authoring guide, valid starter package and a worked synthetic
  example outside the frozen benchmark corpus.
- Source-to-claim evidence and explicit unknown/non-goal handling; no required
  keyword copying, generic intent reuse or novelty quota.
- Structural regression tests and real SpecPM validation in the integration CI.
- FLOW validation/archive/review artifacts and a PR; T3 next-task handoff.

## Acceptance

Both asset packages validate with zero errors and only the intentional
preview_only warning. Capability indexes match declarations; evidence paths
and support targets resolve. Copying the skill alone supplies all its referenced
resources, without personal skills, evaluator data or sibling repositories.
The skill describes investigation, not execution of untrusted source code.
Unknown behavior is not silently represented as a guarantee or dependency.
The worked example is explicitly synthetic, not a real provider result.

## Execution

The main agent authors all skill, example, contract and test changes. Subagents
may perform service checks only. T1 benchmark and its frozen budgets remain
unchanged; runner enforcement belongs to T3, generation to T4.

Run focused asset tests, skill validation, external SpecPM validation, full
pytest/coverage, Ruff, Swift manifest/build and diff hygiene before archiving.

---
**Archived:** 2026-09-06
**Verdict:** PASS
