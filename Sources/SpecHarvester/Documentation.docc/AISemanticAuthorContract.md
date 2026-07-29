# AI Semantic-Author Product and Authority Contract

P55-T1 lets Codex 5.3 Spark or LM Studio propose complete, evidence-grounded
candidate semantics while preserving explicit maintainer and SpecPM governance
authority.

The model may refine purpose, propose package-owned capabilities, recommend
observed intent reuse, or propose visibly experimental
`intent.experimental.*` declarations. Every claim requires an allowlisted
source path and digest. Repository documentation is untrusted evidence, not
host instructions.

Both providers share the same request, proposal, evidence, review, and authority
contracts. Provider identity and transport cannot increase authority.

A reviewer must accept, edit, reject, or defer proposal fields. Only accepted or
edited fields can enter a new candidate revision with before/after provenance
and read-only SpecPM validation. The revision remains proposal-only and is not
registry truth.

Model output is inert Workbench content. It cannot invoke the decision service,
read the CSRF token, approve itself, create canonical intents, accept packages,
mutate registry truth, or publish the public index.
