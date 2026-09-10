# Evidence Context

All Rowpick content in this package is synthetic teaching material by 0AL Spec,
not evidence about a public repository or a model-generated pilot result.
The original source is the adjacent command.md, included in full and unchanged.
There is no upstream Git revision to claim for this fictional source.

The example keeps documented CLI semantics and error/partial-output behavior
in the package instead of reducing the purpose to a language category.
Behavior confidence is low because no implementation or runtime test was
inspected. Installation, platform support and resource limits remain unknown.
Empty capability dependencies mean none are declared here, not that a runtime
has no dependencies. No canonical intent mapping is claimed.

## Discovery Coverage Example

This is an illustrative author assessment against the fictional documentation,
not proof of runtime behavior, a measured coverage percentage or human approval.
The source is still [command.md](command.md); this note is not behavior evidence.
Field IDs below belong to [the BoundarySpec](../specs/main.spec.yaml).

| Consumer need or decision | Source lines in command.md | State | Represented fields or remaining gap |
| --- | --- | --- | --- |
| Select matching records without a query engine | 6-16 | covered | `intent.summary`, `provides.capabilities.example.rowpick.filter`, `interfaces.inbound.filter_cli`: exact top-level string matching, including missing/non-string non-matches. |
| Read a local file without replacing it | 13, 18-19 | covered | `interfaces.outbound.input_file`, `constraints.filesystem_access`, `effects.sideEffects.input_read`: readable input required; input is not modified. |
| Decide whether streamed output is complete | 19-22 | covered | `interfaces.inbound.filter_cli`, `constraints.partial_output`: exit 0 includes zero matches; exit 2 can leave earlier stdout rows. |
| Run nested-field queries, joins or regular expressions | 15-16 | excluded | `scope.excludes`: the fictional command explicitly does not offer these operations. |
| Choose for a specific platform or resource budget | 24-25 | unknown | `scope.excludes` plus this note: installation, platform support, throughput and memory limits are unestablished, not unsupported or unlimited. |

Only one capability is needed here. The useful distinctions live in its summary,
interface, constraints and scope; adding a capability per condition would not
improve the example. A reviewer should focus on whether the partial-output
behavior and unknown runtime/resource requirements are acceptable for their use.

In a real candidate, replace this note with the caller's repository/revision,
source-relative paths, excerpt ranges, digests and redistribution notices.
Do not manufacture these values or promote this note to implementation evidence.
