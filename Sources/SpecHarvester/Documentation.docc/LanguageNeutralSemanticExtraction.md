# Language-Neutral Semantic Extraction

SpecHarvester can extract bounded `semanticHints` from allowlisted Markdown so
manifest-poor repositories still produce reviewable semantic evidence.

## Purpose

Some public repositories expose their value primarily through a README, API
contract, OpenAPI guide, schema validation notes, workflow automation docs,
developer tooling instructions, or a documentation knowledge base rather than a
supported package manifest.

For those repositories, `collect-local` records compact deterministic
`semanticHints` instead of raw documentation bodies. `draft` can then use those
hints as advisory evidence for intent IDs.

## Evidence Shape

The collector may attach `semanticHints` to documentation records for root
`README` files, `docs/*.md`, `SPECS/PRD/*.md`, and DocC Markdown under
`Sources/*/Documentation.docc/`.

The stored hints are bounded language-neutral terms such as:

- `api contract`
- `OpenAPI`
- `schema`
- `request`
- `response`
- `validation`
- `workflow automation`
- `CLI`
- `developer tooling`
- `documentation`

SpecHarvester must not store raw README, API contract, OpenAPI, schema
validation, workflow automation, developer tooling, or documentation knowledge
base bodies in `harvest.json`.

## Drafting Behavior

The drafter combines repository metadata, package manifest metadata, Markdown
headings, `semanticHints`, and optional `PublicInterfaceIndex` symbol names.

Language-neutral semantic clusters include:

- `api.contract_surface` with `intent.api.contract_surface`
- `metadata.schema_validation` with `intent.metadata.schema_validation`
- `workflow.automation_pipeline` with `intent.workflow.automation_pipeline`
- `developer.tooling_surface` with `intent.developer.tooling_surface`
- `documentation.knowledge_base` with
  `intent.documentation.knowledge_base`

When no supported package manifest exists, this semantic profile can replace
the generic `intent.package.public_repository_metadata` fallback. The generated
BoundarySpec records `semantic_intent_static_evidence` and
`semanticEvidenceIndex.clusters` with evidence paths and matched terms.

## Trust Boundary

Allowed:

- Read allowlisted Markdown bytes from a pinned local checkout.
- Extract headings and deterministic semantic terms.
- Include compact hints and file digests in `harvest.json`.
- Use semantic clusters as review evidence.

Forbidden:

- Execute harvested repository code.
- Install harvested dependencies.
- Run package managers, build tools, tests, package scripts, or language
  servers.
- Fetch remote documentation or schemas.
- Treat semantic hints as accepted SpecPM registry truth.

The full GitHub-facing contract is
`docs/LANGUAGE_NEUTRAL_SEMANTIC_EXTRACTION.md`.
