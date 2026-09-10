# Discovery Coverage and Claim Review

Help a consumer find the package for a concrete need and distinguish it from
plausible alternatives. More YAML, evidence files or capability IDs is not the
goal. Apply this inside the caller's scope and budgets, without scanning the
whole repository or introducing another analyzer.

## Source-First Inventory

Use the overview to locate relevant public docs, examples, API/configuration
definitions and focused source. Record consumer outcomes and selection-changing
distinctions, not a catalogue of symbols. For each important group, note the
entry point, source location and material conditions or uncertainty. Include
only the runtime, adapter, transport, error or resource-limit questions that
matter to this product; unrelated checklist items are not missing features.

When an existing package is in the read allowlist, form this inventory before
using its capability list as a baseline. Then check both its fields and packaged
evidence. Information may already have been collected but never surfaced in the
spec. Record that as a representation gap, not newly discovered source evidence.
If prior package content was already visible, say so; do not claim a blind pass.
Unavailable or disallowed baselines do not block ordinary source-first authoring.

Keep a compact table or bullets in the existing author note. Useful columns are
consumer need, source path/range, material qualifiers, coverage state, actual
spec path/field or ID, and remaining gap/reason. No JSON transport or separate
coverage schema is required. These are findings, not hidden reasoning transcripts.

## Reconcile with Discoverable Fields

Map the inventory to `intent.summary`, capability summaries, interfaces,
constraints and scope. A mention in raw evidence alone does not let a consumer
find or compare the feature. Reflect distinguishing behavior in the appropriate
fields while retaining its source support.

Use these descriptive states for the chosen boundary:

| State | Meaning |
| --- | --- |
| covered | Actual spec fields communicate the supported behavior and its selection-critical conditions. Name those fields/IDs and the evidence. |
| partial | Some behavior is represented, but a material distinction or condition is missing. Name the gap. |
| missing | Reviewed sources establish relevant in-scope behavior, but the spec does not communicate it. Evidence-only mentions belong here. |
| excluded | A deliberate boundary decision is explicit in `scope.excludes`, with its reason. This does not mean the software lacks the feature. |
| unknown | The allowed evidence or remaining budget cannot establish the answer. Record the question instead of asserting absence. |

For a revision, retain a concise before/after disposition for material changes.
For a new candidate, one current-state map is enough. These labels are author
assessments, not coverage percentages, maintainer ratings or search benchmarks.
Do not mark everything covered or move an inconvenient gap to excluded simply
to make a report green. Budget-limited omissions stay explicit in the handoff;
they do not authorize a broader run.

Group related options into meaningful user-facing capabilities. A small tool
may need only one. Use more than one only when it helps selection, invocation or
comparison; do not split a capability just to raise counts or match every query.

## Qualifiers and Revision Safety

For each consequential claim, preserve the subject, operation, direction and
conditions established by its source. In particular, when applicable:

- Distinguish request/upload limits from response/download limits; record units,
  defaults and compressed/decompressed measurement only when supported. A bound
  on one does not establish a bound on the other or a general safety guarantee.
- Preserve runtime/adapter/platform differences, experimental status, opt-in
  flags, disabled behavior and error/partial-output semantics. Do not union the
  capabilities of several adapters into a guarantee for all deployments.
- Separate built-in behavior from recipes, hooks, plugins or caller-owned policy.
  An example implementing retry through a hook does not prove automatic retries;
  it can support a qualified extension scenario when that is useful and in scope.
- During revisions compare existing prerequisites, constraints, exclusions,
  compatibility and effects with the new draft. Keep still-supported facts;
  explain corrections or removals using current allowed evidence or an explicit
  scope change. Do not blindly preserve an unsupported old claim.

For example, a fictional exporter may cap each input line at a configured byte
limit but stream unlimited output rows. Do not summarize this as "bounds output
size." If it requires a runtime feature or polyfill, a richer feature list must
not drop that prerequisite. This example is not evidence about the target.

## Claim-to-Excerpt Check

Use the field guide's `supports` syntax and verify the named files and spec
fields/IDs exist. Then re-read each included source range against the material
assertion, including its qualifiers. A nearby heading, type name or matching
digest does not prove the claim. Type declarations establish exposed names and
shapes, not every runtime behavior described in a summary.

If the supporting explanation falls outside the retained range, include that
range unchanged with correct provenance when permitted and within budget.
Otherwise narrow the assertion or disclose the unresolved gap. Never extend a
line-number label without copying and checking the corresponding source bytes.
Keep author notes separate from source excerpts and preserve permitted notices.

Before handoff, read the candidate as a consumer would: which needs would lead
to this package, which important condition might rule it out, and what remains
unknown? Illustrative discovery questions are not measured search results.
Report newly represented facts separately from clearer organization of old facts.
Name only the consequential decisions needing human review; do not make the
maintainer reread a raw inventory to find them. Schema and integrity checks do
not establish semantic correctness or readiness for mass authoring/publication.
