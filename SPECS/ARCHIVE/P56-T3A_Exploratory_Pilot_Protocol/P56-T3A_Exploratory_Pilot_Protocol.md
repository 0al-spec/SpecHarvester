# P56-T3A Exploratory Pilot Protocol

Status: Completed
Date: 2026-09-06
Dependencies: P56-T1, P56-T2
Review subject: p56_t3a_exploratory_pilot_protocol

## Objective

Replace the pending heavyweight comparative execution with a small, explicitly
labeled exploratory pilot. The maintainer approved the simpler plan after the
Luna-medium Logrus smoke. Preserve the original benchmark, not its unexecuted
runtime obligations as new pilot prerequisites.

## Deliverables and Acceptance

- New versioned protocol: same five repositories/revisions/scopes; Luna medium;
  one original candidate per repository; bounded validation repair; human
  side-by-side review using five practical questions.
- Explain historical baseline mismatches, measurement limitations, unknown cost,
  unproven isolation and absence of mass-run/publication authority.
- Retain P56-T1 protocol and benchmark bytes unchanged. Do not relabel Logrus
  smoke or historical Spark evidence as results of the new pilot.
- Mark P56-T3 deferred and keep #372 unmerged. Add this task and revise T4-T8
  with a clear dependency order and outcome-based decision.
- Add regression coverage for protocol identity, unchanged pins and workflow
  lifecycle. No new runner, provider calls or generated repository packages.
- Complete FLOW archive/review and open a separate PR against main.

## Validation

Run focused documentation/benchmark tests, full pytest coverage >=90%, lint,
format, configured Swift gates and diff checks. Record actual results only.

---
**Archived:** 2026-09-06
**Verdict:** PASS for preparation only
