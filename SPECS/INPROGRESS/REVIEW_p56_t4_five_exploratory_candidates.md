# REVIEW REPORT - P56-T4 Five Exploratory Candidates

Date: 2026-09-06
Scope: origin/main..HEAD, retained experiment evidence, tests and FLOW handoff.

## Summary Verdict

Approve with comments for complete experimental outcome collection, not package
quality approval. Independent read-only subagent archive review found no
blockers. Main agent checked its findings and strengthened regression coverage.

## Correctness and Integrity

All five fixed targets and 38 original files are represented in the 58-member
archive. Member, candidate, README, preparation, protocol and retained-baseline
hashes agree. Recorded baseline selection precedes every generation start.
All original validation reports show zero errors; warnings and evidence defects
remain visible. No hidden repair or retry changed the measured outcomes.

## Security and Architecture

Archive members are regular relative files, without links, host paths or
user-identifying tar headers. Generated YAML and copied code remain untrusted
review content. No source execution, registry acceptance or publication was
performed. Instructions and source hash checks are not proven runtime isolation.
The skill and historical benchmark were not changed. Deferred T3 remains unmerged.

## Review Findings and Resolution

- Low: automated integrity tests lacked receipt/report agreement, README hash,
  baseline chronology and aggregate candidate-set checks. Added these checks,
  archive host-path/header checks and exact validator diagnostic comparison.
- Low: local SpecPM integration can skip without its optional dependency. The
  dedicated CI job imports specpm.core before pytest, so that job fails instead
  of silently skipping. Local explicit SpecPM run: 13 passed.
- Experimental findings: RTK altered a supposedly unchanged code excerpt and
  omitted provenance from package collection; other candidates have evidence
  gaps or warnings. Preserved as measured outcomes, not fixed in this run.

## Tests and Performance

Focused tests with the trusted local SpecPM checkout pass. Full coverage gate,
ruff checks and Swift build are recorded in the task validation report. No
production code, server or performance-critical runtime was changed.
Token usage is unavailable; no cost or model superiority conclusion is inferred.

## Follow-Up

No new task required: T5 already owns faithful side-by-side presentation, T6
human per-question usefulness/evidence review, T7 defect/effort synthesis and T8
the explicit decision on fixes or another labeled pilot. Preserve the originals
through those steps. FOLLOW-UP task creation is skipped because no uncovered
delivery blocker remains. PR uses the repository template; do not auto-merge T4.
