# SpecHarvester PRD

Status: Draft
Created: 2026-05-17
Owner: 0AL Spec

## 1. Product Summary

SpecHarvester is an AI-assisted harvesting pipeline that turns public
repository metadata into reviewable SpecPM candidate packages.

The product loop is:

1. Read a public repository checkout as untrusted data.
2. Collect bounded static evidence without executing package content.
3. Draft deterministic `SpecPackage` and `BoundarySpec` candidates.
4. Validate generated candidates with SpecPM.
5. Preserve provenance, policy, and review constraints.
6. Promote only reviewed candidates into accepted-source staging.
7. Optionally propose accepted-source changes into SpecPM through trusted
   maintainer automation.

## 2. Problem

SpecPM can validate and index packages, but public repositories still need a
bounded intake path that collects evidence, drafts conservative candidate
metadata, and makes review cheaper without trusting repository code.

Without SpecHarvester, candidate authoring is manual and expensive. Reviewers
must infer package identity, public package metadata, candidate scope, and
provenance from raw repositories. This increases token use, review time, and
the chance of overclaiming behavior that was not evidenced.

## 3. Goals

- Keep repository harvesting local-first, deterministic, and reviewable.
- Treat all harvested repository content as untrusted metadata.
- Avoid package script execution, dependency installation, and network probing
  during collection.
- Produce deterministic evidence snapshots with file digests and policy notes.
- Draft conservative SpecPM candidates from observed static metadata.
- Support future public interface indexing through deterministic analyzers such
  as manifest parsers, AST parsers, Tree-sitter, and language-specific static
  analyzers.
- Keep model-assisted refinement bounded by explicit evidence and review gates.
- Maintain GitHub and DocC documentation surfaces for operators and reviewers.

## 4. Non-Goals

- Upstream maintainer endorsement.
- Automatic acceptance into a public SpecPM registry.
- Execution of repository tests, scripts, package managers, or generated code.
- Private repository crawling or secret access.
- Remote registry mutation APIs.
- Trusting LLM output without SpecPM validation and maintainer review.

## 5. Primary Users

- Harvester operator: collects snapshots and drafts candidates.
- Candidate reviewer: checks provenance, scope, inferred metadata, and policy.
- SpecPM maintainer: receives reviewed accepted-source proposals.
- Agent operator: uses Flow artifacts to plan, execute, validate, and archive
  repository tasks.

## 6. Trust Boundary

Package content can describe desired outputs. Package content cannot command
the host.

SpecHarvester may read allowlisted static files and deterministic analyzer
outputs. It must not run repository-owned package scripts or treat harvested
content as host instructions.

Analyzer outputs are evidence. They are not proof of runtime behavior unless
the analyzer policy explicitly supports that claim.

## 7. Success Metrics

- `collect-local` produces deterministic `harvest.json` snapshots.
- `draft` produces deterministic candidate specs from snapshots.
- `promote` validates candidates before accepted-source staging unless an
  explicit skip flag is used for tests or emergency manual workflows.
- CI passes Python lint, format, tests with coverage, Swift package validation,
  DocC target build, and SpecPM integration.
- Flow tasks leave reviewable PRD, validation, review, and archive artifacts.
