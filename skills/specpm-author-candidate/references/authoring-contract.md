# Complete Candidate Contract

Contract version: 1. Target format: specpm.dev/v0.1.
This guide is self-contained; implementation/runtime receipts belong to the
caller, not new fields inside a BoundarySpec.

## Output Layout

```text
candidate/
  specpm.yaml
  specs/main.spec.yaml
  evidence/
```

One package can reference several BoundarySpecs. Keep all paths relative to the
package root (including evidence paths inside nested specs), with no symlinks
or traversal. Include actual referenced files. Use JSON-compatible YAML:
no aliases, anchors, custom tags or multiple documents.

## Field Mapping

| Information | Supported location | Authoring decision |
| --- | --- | --- |
| Identity, summary, license, credited author | manifest metadata | Credit the spec author, not an invented upstream endorsement. |
| Candidate authority | manifest preview_only; spec metadata.status | true and draft until an explicit later review action. |
| Useful purpose/scenario | intent.summary; capability summary | Consumer + outcome; enough detail to distinguish products with the same stack. |
| Product boundary and non-goals | scope.boundedContext, includes, excludes | Explain excluded members, unsupported use and partial coverage. |
| Callable behavior | provides.capabilities | Nonempty objects with id, role: primary/supporting, summary. |
| Package index | index.provides.capabilities | Exact union of capability IDs from referenced specs. |
| Existing canonical intent mapping | capability intentIds and manifest index.provides.intents | Optional, exact approved IDs only; both lists must agree. |
| Entry points and examples | interfaces.inbound/outbound | id, kind, summary; inputs/outputs describe names and media types where useful. Include invocation, return/error behavior in summary. |
| Runtime prerequisites and restrictions | constraints | id, level: MUST/SHOULD/MAY, statement. Express observed constraints, not desired implementation changes. |
| Known external capability dependency | requires.capabilities and index.requires.capabilities | Only identified capabilities. A language/package dependency is not automatically a SpecPM capability dependency. |
| Platform/language compatibility | compatibility | Source-backed platforms/languages; omitted or empty means unestablished, not universal. |
| Mutations, reads and external calls | effects.sideEffects | A mapping containing a list of id/kind/summary objects, not a bare list. Empty is no declared effects, not proof of purity. |
| Source grounding | evidence | id, kind, package-relative path, supports. Cite source bytes, not generated claims citing themselves. |
| Concrete implementation file copy | implementationBindings | Optional; point only to included, verified files. Do not pretend external checkout paths are portable. |
| Uncertainty | provenance.sourceConfidence; scope.excludes; evidence notes | intent/boundary/behavior: high/medium/low/unknown. Label unknown coverage explicitly, distinguishing it from a documented non-goal. |

Use an evidence note file for source revision, original relative path, line/byte
range and digest plus unresolved questions. Reference that file as documentation,
but do not use author-written notes alone to prove implementation behavior.
Keep source excerpts separately with `kind: source/documentation/test/example/
package_manifest`, as appropriate. A local file's existence proves neither
authenticity nor that its contents support the claim; source review is separate.

Supported interface kinds include library, cli, http, file, event, queue,
plugin, config and schema. Effect kinds include filesystem_read/write,
network_read/write, database_read/write, process_spawn, environment_read/write,
log_write, event_emit, message_publish and state_mutation.

`supports` may name `intent.summary`, `scope`, `scope.includes`, `scope.excludes`,
`provides.capabilities.<id>`, `interfaces.inbound.<id>`,
`interfaces.outbound.<id>`, `constraints.<id>` or
`effects.sideEffects.<id>` or `provenance.sourceConfidence`. IDs must exist in
the same BoundarySpec; structural targets such as `scope` do not need an ID.
Do not append `.intentIds` to a support target.

## Data-Flow Review

For each source-supported external interaction, identify the outgoing data,
destination, returned data, and enabling conditions (provider, flags, deployment
or configuration). Record material flows in `effects.sideEffects` and connect
them to evidence with `supports`; do not add a new schema field or execute code
to establish the flow.

- Sending application data to another service is `network_write`, even if the
  purpose is to obtain an answer and no remote persistent mutation is established.
  A response can be described in the same summary or a separate `network_read`
  effect; it must not replace the outgoing effect.
- A CLI/SDK using a remote AI provider sends prompts and may send supplied images
  or repository context. Describe only the data categories supported by evidence,
  the configured destination and relevant conditions. A local executable does
  not establish local-only processing; do not claim every deployment is remote.
- HTTP method names, "read-only API" labels and absence of local file writes do
  not prove absence of disclosure. Inspect request payloads, parameters and
  authentication handling when supported by the allowed sources. Never copy
  actual credentials or user data into evidence.
- Do not infer network traffic merely from an SDK name, or invent exact endpoints,
  uploaded files or retention policies. If these are not established, state the
  unknowns while preserving any established outbound flow. Local-only processing
  should not acquire a speculative network effect.

For example, a documented CLI sends a prompt and an optional image to a configured
remote inference API and returns generated text. `network_read: fetch an answer`
is incomplete. Use `network_write` describing the prompt/optional image transfer
and configured service, with response receipt in the summary or a separate effect.
This is a synthetic teaching example, not evidence about the target repository.

Before handoff, compare each effect's kind and summary with its supporting source.
Validation accepts both network kinds; source-file hashes prove integrity, not
the correctness of this classification. Repeat the check across the package's
interfaces instead of fixing only the first similar case found.

## Completeness without Invention

A useful package answers what a consumer can accomplish, the entry point they
would use, input/output shape, prerequisites and significant failure/side-effect
boundaries. It need not enumerate every private function or dependency.
Missing facts remain visible as unknowns instead of plausible guesses.

The starter is intentionally an abstract, synthetic contract. The worked
example describes a fictional documented interface and illustrates richer
content; it is not an executed implementation or a quality calibration result.
Neither asset's namespace, license or capabilities should leak into a target.

## Validation Meaning

A zero-error report is necessary, not sufficient. Review warning codes, missing
source support, boundary choice and factual qualifiers separately. The assets
intentionally emit the preview_only_package warning; do not remove the candidate
flag to get a warning-free report. A real candidate may have other warnings:
retain and explain them instead of asserting readiness.

Package validation cannot establish namespace ownership, intent canonicality,
license permission, runtime safety or publication approval. No new transport
schema, acceptance mechanism or dependency resolver is introduced here.
