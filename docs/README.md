# SpecHarvester Documentation

This directory is the operator and design entrypoint for SpecHarvester.

Use it the same way the SpecPM repository uses GitHub-facing documentation:
start from the workflow, then drill into architecture, trust boundaries, and
automation details.

Published DocC site:
[https://0al-spec.github.io/SpecHarvester/](https://0al-spec.github.io/SpecHarvester/).

## Read This First

1. [`../README.md`](../README.md): repository overview and GitHub workflow surface
2. [`HOW_IT_WORKS.md`](HOW_IT_WORKS.md): end-to-end operator flow
3. [`TRUST_BOUNDARY.md`](TRUST_BOUNDARY.md): non-negotiable execution rules
4. [`ANALYZER_SANDBOX_REQUIREMENTS.md`](ANALYZER_SANDBOX_REQUIREMENTS.md):
   requirements for future metadata-tool and build-tool analyzers
5. [`TRUSTED_CLASSIFIER_EVALUATION.md`](TRUSTED_CLASSIFIER_EVALUATION.md):
   registry and trust contract for optional external classifiers
6. [`LANGUAGE_NEUTRAL_SEMANTIC_EXTRACTION.md`](LANGUAGE_NEUTRAL_SEMANTIC_EXTRACTION.md):
   bounded README/API-contract semantic hints for manifest-poor repositories
7. [`REPOSITORY_SOURCE_MANIFESTS.md`](REPOSITORY_SOURCE_MANIFESTS.md):
   batch harvesting input manifest schema
8. [`BATCH_COLLECTION.md`](BATCH_COLLECTION.md): deterministic batch snapshot
   collection from local checkouts
9. [`BATCH_VALIDATION_REPORTS.md`](BATCH_VALIDATION_REPORTS.md): advisory
   confidence and policy reports for batch output
10. [`ACCEPTED_MANIFEST_ENTRIES.md`](ACCEPTED_MANIFEST_ENTRIES.md): prepare
   PR-ready accepted package manifest entries
11. [`GOVERNANCE_REPORTS.md`](GOVERNANCE_REPORTS.md): detect duplicate intent
   and capability claims across accepted and candidate metadata
12. [`NAMESPACE_UPSTREAM_REPORTS.md`](NAMESPACE_UPSTREAM_REPORTS.md): review
   namespace consistency and upstream relationship metadata across roots
13. [`SPECPM_PROPOSAL_AUTOMATION.md`](SPECPM_PROPOSAL_AUTOMATION.md): trusted
    proposal automation with preflight validation and diff-scope guardrails
14. [`ACCEPTED_PACKAGE_UPDATE_LIFECYCLE.md`](ACCEPTED_PACKAGE_UPDATE_LIFECYCLE.md):
   accepted package version immutability and update decision policy
15. [`ACCEPTED_PACKAGE_UPDATE_PROPOSALS.md`](ACCEPTED_PACKAGE_UPDATE_PROPOSALS.md):
   build PR-ready accepted package update artifacts
16. [`ACCEPTED_CANDIDATE_DIFF_REPORTS.md`](ACCEPTED_CANDIDATE_DIFF_REPORTS.md):
    compare accepted and candidate package metadata before update proposals
17. [`ACCEPTED_CANDIDATE_IMPACT_CLASSIFICATION_REPORTS.md`](ACCEPTED_CANDIDATE_IMPACT_CLASSIFICATION_REPORTS.md):
    classify accepted-candidate diff output by metadata, interface, license,
    provenance, capability, and intent impact
18. [`LICENSE_PROVENANCE_RISK_REPORTS.md`](LICENSE_PROVENANCE_RISK_REPORTS.md):
    review candidate and accepted packages for licensing and provenance risk
19. [`LOCAL_SMOKE_FIXTURES.md`](LOCAL_SMOKE_FIXTURES.md): reproducible local
    smoke fixtures for adjacent real repository checkouts
20. [`SPECNODE_INTEGRATION_CONTRACT.md`](SPECNODE_INTEGRATION_CONTRACT.md):
    typed artifact bundle and job contract for future SpecNode-assisted
    candidate refinement
21. [`SPECNODE_REFINE_PREVIEW_CONTRACT.md`](SPECNODE_REFINE_PREVIEW_CONTRACT.md):
    bounded `refine-preview` planning contract for compact model input
22. [`SPECNODE_PROVIDER_ADAPTER_CONTRACT.md`](SPECNODE_PROVIDER_ADAPTER_CONTRACT.md):
    OpenAI-compatible provider adapter boundary for local SpecNode execution
23. [`../SPECS/README.md`](../SPECS/README.md): Flow workflow for planning,
    implementing, validating, and archiving tasks

## Design References

- [`ARCHITECTURE.md`](ARCHITECTURE.md): component model and non-goals
- [`ROADMAP.md`](ROADMAP.md): implementation phases and future tracks
- [`TREE_SITTER_EVALUATION.md`](TREE_SITTER_EVALUATION.md): decision record for
  Tree-sitter as an optional syntax indexing layer
- [`TRUSTED_CLASSIFIER_EVALUATION.md`](TRUSTED_CLASSIFIER_EVALUATION.md):
  evaluation record for Linguist-compatible classifiers, Syft, ScanCode,
  Universal Ctags, and Tree-sitter
- [`LANGUAGE_NEUTRAL_SEMANTIC_EXTRACTION.md`](LANGUAGE_NEUTRAL_SEMANTIC_EXTRACTION.md):
  README/API-contract semantic extraction for manifest-poor repositories
- [`SPECPM_PROPOSAL_AUTOMATION.md`](SPECPM_PROPOSAL_AUTOMATION.md): trusted
  automation for proposing accepted-source diffs into SpecPM
- [`SPECNODE_INTEGRATION_CONTRACT.md`](SPECNODE_INTEGRATION_CONTRACT.md):
  trust boundary for future model-assisted candidate refinement through
  SpecNode
- [`SPECNODE_REFINE_PREVIEW_CONTRACT.md`](SPECNODE_REFINE_PREVIEW_CONTRACT.md):
  deterministic `refine-preview` plan shape for compact model input
- [`SPECNODE_PROVIDER_ADAPTER_CONTRACT.md`](SPECNODE_PROVIDER_ADAPTER_CONTRACT.md):
  LM Studio/OpenAI-compatible provider discovery, health, model listing, and
  execution policy boundary for SpecNode

## GitHub Process Surface

- Pull requests: [`.github/PULL_REQUEST_TEMPLATE.md`](../.github/PULL_REQUEST_TEMPLATE.md)
- Issue forms: [`.github/ISSUE_TEMPLATE`](../.github/ISSUE_TEMPLATE)
- CI: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)
- Cross-repository proposal automation:
  [`.github/workflows/propose-to-specpm.yml`](../.github/workflows/propose-to-specpm.yml)

## Operator Checklist

- Start from a public repository checkout pinned to a revision.
- Collect bounded static evidence into `harvest.json`.
- Draft deterministic candidate SpecPM files.
- Validate the candidate with SpecPM.
- Review provenance, scope, and inferred metadata.
- Prepare PR-ready accepted manifest entries for reviewed candidates.
- Promote only reviewed candidates into accepted-source staging.
