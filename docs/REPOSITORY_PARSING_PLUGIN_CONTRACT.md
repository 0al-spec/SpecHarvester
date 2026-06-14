# Repository Parsing Plugin Contract

Status: Phase 36 contract plan.

SpecHarvester can already produce a valid starter package for FastAPI, but the
latest FastAPI rerun shows a precision gap: `docs_src/*` tutorial files are
valuable semantic usage evidence, yet they should not be treated as
`public_interface` evidence for `fastapi.core`.

This contract defines a future plugin-shaped parsing policy layer for
language/framework-specific repository rules. It is not a plugin
implementation and it is not a FastAPI special case.

## Problem

Repository layout is not uniform:

- Python web frameworks may keep executable documentation examples under
  `docs_src/`;
- JavaScript monorepos may mix public packages, examples, internal utilities,
  generated artifacts, and tests in the same workspace;
- Rust, Go, Swift, and documentation-first repositories expose different
  package roots and public interface conventions.

A single hardcoded analyzer rule will either over-capture examples and tests
or under-capture real public package surfaces.

## Goal

Repository parsing plugins classify repository paths before analyzer output is
used as candidate evidence.

They should separate:

- `public_interface`: source paths intended to define the consumer-facing API;
- `semantic_usage`: documentation, tutorials, examples, and snippets useful
  for intent, terminology, and local-model enrichment;
- `documentation`: prose or structured docs;
- `example`: demo/tutorial code;
- `test`: tests and fixtures;
- `generated`: generated source or checked-in build output;
- `tooling`: build, lint, codegen, CI, or repository-maintenance code;
- `internal`: implementation-only code not intended as package identity;
- `ignored`: paths that should not participate in candidate evidence.

## Non-Goals

Repository parsing plugins do not:

- clone or fetch repositories;
- install dependencies;
- execute harvested code, tests, package scripts, or build tools;
- call package registries;
- publish registry metadata;
- accept packages or relations;
- seed baselines;
- remove `preview_only`;
- treat AI output as registry truth.

## Contract Shape

A future machine-readable parser decision artifact should use a versioned
shape:

```json
{
  "apiVersion": "spec-harvester.repository-parsing-plugin/v0",
  "kind": "SpecHarvesterRepositoryParsingPluginDecision",
  "schemaVersion": 1,
  "authority": "producer_path_classification_only"
}
```

The artifact is producer review evidence. It explains how paths were
classified; it does not make generated package claims authoritative.

## Plugin Inputs

Parser plugin inputs are only local, bounded, reviewable inputs:

- repository source manifest metadata;
- resolved local checkout path;
- selected repository id and package family;
- expected revision or ref from the source manifest;
- detected ecosystem and labels;
- workspace inventory when available;
- package manifests and package roots;
- analyzer plan ids;
- optional operator-selected parser profile id.

Plugins must not perform network discovery, dependency installation, code
execution, or registry lookups.

## Plugin Outputs

Parser plugin outputs are path classification decisions:

```json
{
  "path": "docs_src/first_steps/tutorial001.py",
  "role": "semantic_usage",
  "subrole": "example",
  "appliesToPackageId": "fastapi.core",
  "reasonCodes": ["documentation_example", "not_package_root"],
  "confidence": "high",
  "publicInterfaceEligible": false,
  "semanticUsageEligible": true
}
```

Required fields:

- `path`: repository-relative path;
- `role`: primary evidence role;
- `appliesToPackageId`: candidate package id or package family;
- `reasonCodes`: machine-readable rationale;
- `confidence`: `high`, `medium`, `low`, or `blocked`;
- `publicInterfaceEligible`: whether the path may enter
  `public_interface_index`;
- `semanticUsageEligible`: whether the path may support intent or AI
  enrichment.

## Rule Precedence

Parser rule precedence is deterministic:

Rule application should be deterministic:

1. explicit operator override;
2. selected parser profile rule;
3. language/package manager rule;
4. generic repository classifier rule;
5. conservative default fallback.

The conservative fallback should prefer `semantic_usage` or `ignored` over
`public_interface` when a path looks like documentation, example, test,
fixture, generated output, or tooling.

## Evidence Roles

| Role | Meaning | Public interface eligible |
| --- | --- | --- |
| `public_interface` | Consumer-facing package/API surface. | yes |
| `semantic_usage` | Usage examples, docs snippets, README examples, tutorials. | no |
| `documentation` | Prose or structured docs. | no |
| `example` | Demo/tutorial project or file. | no |
| `test` | Test files, test fixtures, mock examples. | no |
| `generated` | Generated code or checked-in build output. | no by default |
| `tooling` | Build, lint, codegen, CI, repository tooling. | no |
| `internal` | Internal implementation not exposed as package identity. | maybe, only when package profile says so |
| `ignored` | Excluded path. | no |

## FastAPI Motivating Case

For FastAPI, a future Python web-framework profile should treat package code
such as `fastapi/` as public interface evidence and treat `docs_src/`,
tutorials, examples, and tests as semantic usage evidence unless an explicit
plugin rule promotes a path.

That means:

```text
fastapi/
  -> public_interface

docs_src/
docs/
tests/
  -> semantic_usage, documentation, example, or test
```

The documentation remains useful. It can inform intent, terminology,
capabilities such as HTTP routing and OpenAPI generation, and local AI
enrichment. It should not create public API symbols such as tutorial
`read_item()` functions or example `app` variables.

## Analyzer Interaction

Parser decisions should be consumed before public interface indexes are
assembled:

```text
source manifest
  -> repository parser plugin decisions
  -> analyzer path selection
  -> public_interface_index
  -> draft candidate
  -> AI enrichment / quality report / handoff
```

Semantic usage evidence may still be available to:

- README/API-contract semantic hints;
- package-set AI enrichment requests;
- author-ready quality reports;
- static viewer context;
- maintainer review notes.

It should be labeled separately from public interface evidence in reports and
handoff artifacts.

## Decision Report

Future parser plugin output should summarize:

- selected profile id and version;
- matched rules and unmatched fallback count;
- counts by role;
- public-interface path count;
- semantic-usage path count;
- ignored path count;
- blocked paths and stop reasons;
- operator overrides;
- non-authority statements.

The report should be hashable and referenceable from producer receipts and
handoff artifacts.

## Parser Profile Fixture

P36-T2 adds the first machine-readable parser profile fixture:

```text
tests/fixtures/repository_parsing_profiles/python-web-framework-v0.example.json
```

The fixture uses:

```json
{
  "apiVersion": "spec-harvester.repository-parsing-profile/v0",
  "kind": "SpecHarvesterRepositoryParsingProfile",
  "schemaVersion": 1,
  "authority": "producer_path_classification_profile_only",
  "profile": {
    "id": "python.web_framework.v0"
  }
}
```

It records rule precedence, evidence roles, path role rules, fallback behavior,
sample FastAPI-like decisions, and non-authority statements.

The fixture treats `fastapi/` package code as `public_interface` evidence and
treats `docs_src/`, docs, examples, and tests as non-public-interface evidence
by default:

```text
fastapi/applications.py
  -> public_interface
  -> publicInterfaceEligible: true

docs_src/first_steps/tutorial001.py
  -> semantic_usage
  -> publicInterfaceEligible: false
  -> semanticUsageEligible: true

tests/test_applications.py
  -> test
  -> publicInterfaceEligible: false
```

## Plugin-Aware Classification Hook

P36-T3 makes the Python web-framework profile executable for static analyzer
path selection. The hook is explicit opt-in:

```bash
PYTHONPATH=src python -m spec_harvester collect-batch inputs \
  --out output \
  --emit-interface-indexes \
  --parser-profile python.web_framework.v0
```

The same profile can be passed through autonomous candidate batch runs:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch inputs \
  --out output \
  --lm-studio-model openai/gpt-oss-20b \
  --parser-profile python.web_framework.v0
```

When no parser profile is selected, the analyzer keeps its previous behavior.
When `python.web_framework.v0` is selected, Python paths classified with
`publicInterfaceEligible: false` are excluded from
`public-interface-index.json` entrypoints. Package records include
`repositoryParsingProfile` and `pathClassification` review metadata so a
maintainer can see why paths were included or excluded.

The hook currently supports only `python.web_framework.v0`. Unknown parser
profile ids fail closed with a clear error.

## Safety Boundary

Plugin decisions are producer-side evidence only.

They do not publish registry metadata. They do not accept packages or
relations. They do not seed baselines. They do not remove `preview_only`. They
do not treat AI output as registry truth.

SpecPM and maintainers remain the validation, acceptance, relation, and
registry authority.

In short: the contract does not publish registry metadata, does not accept
packages or relations, does not remove `preview_only`, and does not treat AI
output as registry truth.

## Follow-Up Work

- `P36-T2`: add a machine-readable Python web-framework parser profile
  fixture.
- `P36-T3`: implement the first plugin-aware source classification hook.
- `P36-T4`: rerun FastAPI with the parser profile and compare evidence volume
  and claim quality against the current AI-enabled draft.
