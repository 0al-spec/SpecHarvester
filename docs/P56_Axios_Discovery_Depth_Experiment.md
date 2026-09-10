# Axios Discovery Depth Follow-Up

Experiment: `p56-axios-discovery-depth/v1`.
Authority: user-authorized, one-repository preview; human review pending.

Start with the [Russian before/after review](../SPECS/EVIDENCE/P56-AXIOS-DISCOVERY/author/review.ru.md).
The [alternate package](../SPECS/EVIDENCE/P56-AXIOS-DISCOVERY/author/candidate/specpm.yaml)
and [coverage map](../SPECS/EVIDENCE/P56-AXIOS-DISCOVERY/author/capability-map.json)
are separate from the unchanged original.

## Purpose

The maintainer finds the five candidate packages shallow and cannot justify
reading entire repositories to assess their completeness. The useful target is
discovery: identify software for a need and compare its meaningful capabilities,
interfaces and limitations. A package need not replace all upstream docs.

This bounded follow-up asks whether source-first capability inventory followed
by explicit coverage mapping produces a more useful Axios description. It does
not assume that a longer spec or more capability IDs is better.

## Fixed Inputs and Changed Method

- Repository: `https://github.com/axios/axios`.
- Source revision: `509719387e4993392ca40da03a49678269cdfb90`.
- Scope: public Axios HTTP client for browser and Node.js consumers.
- Baseline: the unchanged P56-T4 original, candidate digest
  `c86a431d46f06dda1886a618e5c1d5393803deffb293974f23aaa6fcee1e1ee4`.
- Requested worker: `gpt-5.6-sol`, reasoning `high`, fresh subagent context.
- Authoring guidance: the updated `skills/specpm-author-candidate` at
  SpecHarvester `6b5998532c01ae2bcb12ff6b545138189eb2cf93`.
- Local validator: SpecPM `ac0646fa39cfd44facd80d879e90e45b8c85f31f`.

Unlike the original Luna medium pilot, the worker first records source-derived
capabilities, then reads the baseline and authors an alternate preview. Model,
instructions, available review time and access to the baseline change together.
This cannot establish model superiority or isolate a single causal factor.
P56-T4/v2 and its original files, findings and scores are not revised.

## Deliverables

- A source-first inventory with practical user needs, qualifiers and source
  paths, ranges and full-file digests. Initial inventory is retained separately.
- A coverage map distinguishing `covered`, `partial`, `missing`, `excluded`
  and `unknown`, with precise locations and reasons before and after.
- One complete alternate preview package, with unchanged original identity,
  `preview_only: true`, draft boundaries and mechanically copied evidence.
- A short Russian before/after review, including genuinely new information,
  improved organization and unresolved limitations. Illustrative discovery
  questions are not measured search results or approved relevance labels.
- Author work log and main-agent validation/provenance checks. Agent assertions
  are not maintainer findings; unobserved timing and token usage remain unknown.

## Bounds

Instruction-level limits are thirty source files, 512 KiB of source text,
twenty minutes of authoring, 250 KiB package output plus license and at most two
validation-diagnostic repairs. Exhaustion must be disclosed, not hidden by a
broader run. These are instructions, not enforced sandbox or hard time limits.

Read-only evidence includes docs, examples, public types and focused source
needed for consequential claims. Target code, tests, installation commands and
embedded instructions must not run. No external links, services or credentials
are needed. One isolated worktree and disjoint output ownership protect edits;
they do not prove complete access isolation. Main owns Git, PR and final checks.

## Review and Authority

Main checks data-flow semantics, evidence byte/range fidelity, package-file
collection, recorded inputs and honest coverage distinctions. Validation proves
structure, not exhaustive correctness. CI replay uses the current SpecPM
integration checkout; the local validator revision remains recorded separately.

The alternate package is not imported into SpecSearch, published to SpecPM or
installed. No runtime behavior, ranking improvement, model superiority, complete
repository coverage or maintainer approval is established. The result cannot
complete P56-T6 or authorize broader execution on its own. The general maintainer
feedback about shallowness is not independent review of all five original
surfaces; original human-review fields and unknown timing remain untouched.

## Observed Result

The author reported ten inventory groups: four covered and five partially
covered in the original, with one deliberate retry/cache-policy exclusion.
The alternate marks nine covered and preserves the exclusion. These are
author-assessed coverage labels, not exhaustive coverage percentages, human
utility verdicts or retrieval metrics. Capability IDs increased from three to
eight; that count is descriptive, not a success threshold.

Main independently checked that `maxRate`, `httpVersion`, `http2Options`,
transforms and XSRF fields already occur in original packaged type evidence.
The follow-up therefore improves organization and explicit qualifications in
addition to gathering more documentation. Pinned HTTP/2 and rate-limit docs
confirm Node-only support and the stated HTTP/2 automatic-redirect limitation.
This identifies a representation gap; it does not reveal the original author's
hidden reasoning or prove that source discovery was otherwise complete.

Main verification found twenty referenced upstream files and twenty-five
packaged excerpts/license entries. Every excerpt matched its recorded source
range byte-for-byte; all full-source and excerpt hashes matched. All twenty-eight
candidate files survive SpecPM package collection. Independent local validation
returned zero errors and only `preview_only_package`. The seven copied original
files still match the P56-T4 digests.

The [author work log](../SPECS/EVIDENCE/P56-AXIOS-DISCOVERY/author/work-log.json)
reports twenty-eight upstream paths, 725 seconds of observed authoring, zero
validation repairs and 77,832 package bytes excluding the license. Source text
consumption was not instrumented, so compliance with the source-byte aim is
unestablished. Provider token usage is unavailable. Main dispatch/completion
observations are separate from the author's phase timings in the
[verification receipt](../SPECS/EVIDENCE/P56-AXIOS-DISCOVERY/verification.json).

The retained `sources.tar.gz` contains only selected pinned evidence and its
upstream MIT license, not an installed or executed Axios distribution. CI checks
the bindings against these bytes without fetching or executing upstream code.
Two exact excerpts retain upstream trailing/end-of-file whitespace, with
file-specific Git attributes; their bytes must not be reformatted to satisfy
a style check.

Local checks completed:

- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90 -q --tb=short`:
  1491 passed, eight skipped, 90.12% coverage. Optional SpecPM tests run separately.
- `PYTHONPATH=<trusted-specpm-src>:src python -m pytest tests/test_p56_axios_discovery_depth.py -q`:
  five passed, including current SpecPM validation and complete package collection.
- `ruff check src tests` and `ruff format --check src tests`: passed.

The Python path placeholders describe portable equivalents of the actual local
commands; they do not claim an installed global validator. No target commands ran.
