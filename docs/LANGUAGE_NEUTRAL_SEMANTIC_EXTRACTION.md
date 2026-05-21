# Language-Neutral Semantic Extraction

Status: Bootstrap contract
Scope: P10-T5, documentation-first repositories

## TL;DR

SpecHarvester extracts bounded `semanticHints` from allowlisted Markdown so
manifest-poor repositories can still produce reviewable intent evidence. The
collector stores compact phrases, not raw documentation bodies, and the drafter
uses those hints only as advisory static evidence.

This path is meant for public SpecPM.dev candidates where a README, API
contract, OpenAPI guide, schema validation guide, workflow automation document,
developer tooling manual, web framework public API, or documentation knowledge
base may be the strongest public signal available.

## Evidence Contract

The collector may attach `semanticHints` to documentation records in
`harvest.json` when an allowlisted Markdown file contains deterministic terms.
Supported documentation paths include root `README` files, `docs/*.md`,
`SPECS/PRD/*.md`, and DocC Markdown under `Sources/*/Documentation.docc/`.

`semanticHints` are intentionally small:

- normalized language-neutral terms such as `api contract`, `OpenAPI`,
  `schema`, `request`, `response`, `validation`, `workflow automation`, `CLI`,
  `developer tooling`, `web framework`, `route`, `middleware`, `handler`, and
  `documentation`;
- bounded by a fixed limit;
- sorted by the project-owned term order;
- derived without executing repository code, package managers, package scripts,
  build tools, or network probes.

SpecHarvester must not store raw README, API contract, OpenAPI, schema
validation, workflow automation, developer tooling, or documentation knowledge
base bodies in `harvest.json`.

## Drafting Behavior

The drafter combines repository names, package manifest metadata, Markdown
headings, `semanticHints`, and optional `PublicInterfaceIndex` symbols into a
small semantic corpus.

Language-neutral clusters do not require Swift, Python, JavaScript, or any
other language context. Current deterministic clusters are:

- `web.framework_surface` with `intent.web.framework_surface`;
- `web.http_routing` with `intent.web.http_routing`;
- `web.middleware_pipeline` with `intent.web.middleware_pipeline`;
- `web.request_response_context` with
  `intent.web.request_response_context`;
- `api.contract_surface` with `intent.api.contract_surface`;
- `metadata.schema_validation` with `intent.metadata.schema_validation`;
- `workflow.automation_pipeline` with
  `intent.workflow.automation_pipeline`;
- `developer.tooling_surface` with `intent.developer.tooling_surface`;
- `documentation.knowledge_base` with
  `intent.documentation.knowledge_base`.

When no supported package manifest exists, a semantic profile can replace the
generic `intent.package.public_repository_metadata` fallback. The generated
BoundarySpec then records `semantic_intent_static_evidence` with evidence paths
and a `semanticEvidenceIndex` cluster list.

When a supported package manifest exists, only domain-specific semantic clusters
that are strong enough to describe the package capability, such as Swift/iOS or
web framework clusters, replace the manifest's generic intent IDs. Generic
language-neutral API or tooling clusters remain review evidence unless no better
manifest capability exists.

## Review Semantics

These intent IDs are advisory. They help reviewers find likely web frameworks,
API contract, schema validation, workflow automation, developer tooling, or
documentation knowledge base packages. They are not registry acceptance,
upstream endorsement, runtime behavior evidence, or proof that a schema, API, or
HTTP route is valid.

Reviewers should check:

- source repository and revision provenance;
- whether evidence paths are relevant and public;
- whether `semanticEvidenceIndex.clusters[*].matchedTerms` are enough for the
  claimed `intent.*` IDs;
- whether a missing manifest is expected for the package type;
- whether generated candidate text remains conservative.

## Safety Rules

Allowed:

- Read allowlisted Markdown bytes from a pinned local checkout.
- Extract headings and deterministic semantic terms.
- Include compact `semanticHints` and SHA-256 digests in `harvest.json`.
- Use semantic clusters as BoundarySpec review evidence.

Forbidden:

- Execute harvested repository code.
- Run package managers, tests, build tools, package scripts, or language
  servers.
- Install harvested dependencies.
- Fetch remote documentation or schemas.
- Store full raw documentation bodies in generated candidate artifacts.
- Treat semantic hints as canonical SpecPM registry truth.

## Operator Example

```bash
python3 -m spec_harvester collect-local /path/to/repo \
  --repository https://github.com/example/contract-hub \
  --revision <commit-sha> \
  --out candidates/contract-hub

python3 -m spec_harvester draft candidates/contract-hub \
  --package-id contract_hub.core \
  --out candidates/contract-hub
```

Expected review evidence in the generated BoundarySpec:

```yaml
evidence:
  - id: semantic_intent_static_evidence
    kind: documentation
    paths:
      - README.md
    semanticEvidenceIndex:
      schemaVersion: 1
      clusters:
        - id: api.contract_surface
          intentId: intent.api.contract_surface
```

The exact cluster set depends on the deterministic terms found in the
allowlisted documentation.
