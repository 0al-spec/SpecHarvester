# P56-T1 Practical Utility Benchmark

## Objective

Freeze an executable comparison of complete agent-authored SpecPM packages,
the current SpecHarvester pipeline, and pinned README content on five diverse
repositories before generating either arm.

## Deliverables

- Versioned experiment protocol with exact models, budgets, scoring, failures,
  source isolation, blinded review, and numerical adoption thresholds.
- Five pinned source revisions, product boundaries, and evaluator-only
  questions/reference answers with source citations and content hashes.
- Validation of benchmark completeness and referenced source identities.
- Archived task report and P56-T2 handoff; a focused stacked PR above #369.

## Acceptance

All five repositories include five scored questions covering discovery,
integration, operations, limitations, and evidence. Answers are grounded in
pinned sources. Authoring workers never receive the questions or answer key.
Both generation arms use one declared model/settings and equal upper budgets.
Invalid/failed/missing outputs remain in denominators. README comparison and
source-assisted evaluation have explicit access rules and costs. Historical
P55 gates remain unchanged. No candidate generation or publication runs here.

## Work Plan

1. Verify source inventory and independently evaluate protocol feasibility.
2. Freeze readable protocol and a digest-bound machine-readable benchmark.
3. Verify source bindings, run repository quality gates, and archive.
4. Obtain fresh independent review; integrate fixes and publish a single PR.

## Orchestration

Two read-only GPT 5.6 Luna agents at high reasoning research source answers
and experimental validity independently. The main agent owns all edits and Git
state. A fresh read-only reviewer checks the integrated artifact.
