# ``SpecHarvester``

AI-assisted harvesting pipeline for turning public repository metadata into
reviewable SpecPM candidate packages.

## Overview

SpecHarvester is a producer pipeline, not a package substrate. It collects
bounded evidence from public repository checkouts, drafts deterministic SpecPM
candidate files, validates them with SpecPM, and prepares them for controlled
promotion.

The current bootstrap supports:

- safe evidence collection from allowlisted static files;
- deterministic `harvest.json` snapshots with provenance and file digests;
- conservative draft generation for `specpm.yaml` and `specs/*.spec.yaml`;
- SpecPM validation before promotion;
- controlled promotion into accepted-source staging;
- trusted proposal automation that can prepare a pull request against
  `0al-spec/SpecPM`.

SpecHarvester does not execute harvested repository code, install harvested
dependencies, or publish generated candidates directly into a public registry.

## Source Documents

The canonical source files remain in the repository:

- `README.md`
- `docs/README.md`
- `docs/HOW_IT_WORKS.md`
- `docs/ARCHITECTURE.md`
- `docs/TRUST_BOUNDARY.md`
- `docs/SPECPM_PROPOSAL_AUTOMATION.md`
- `docs/ROADMAP.md`

This DocC site is a navigable documentation mirror built from those contracts.

## Boundary Statements

Generated package content is candidate metadata, not upstream-endorsed truth.

Package content can describe desired outputs. Package content cannot command
the host.

## Topics

### Start Here

- <doc:GettingStarted>
- <doc:Workflow>
- <doc:ProposalAutomation>

### Architecture

- <doc:Architecture>
- <doc:TrustBoundary>
- <doc:Roadmap>
