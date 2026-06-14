# Repository Parsing Plugin Contract

Status: Phase 36 contract plan.

SpecHarvester can produce a valid FastAPI starter package, but the latest
FastAPI rerun shows a precision gap: `docs_src/*` tutorial files are useful
semantic usage evidence, not public interface evidence for `fastapi.core`.

This document defines a future plugin-shaped parsing policy layer for
language/framework-specific repository rules. It is not a plugin
implementation and it is not a FastAPI special case.

## Goal

Repository parsing plugins classify repository paths before analyzer output is
used as candidate evidence.

They separate:

- `public_interface`;
- `semantic_usage`;
- `documentation`;
- `example`;
- `test`;
- `generated`;
- `tooling`;
- `internal`;
- `ignored`.

## Contract Shape

Future machine-readable decisions should use:

```json
{
  "apiVersion": "spec-harvester.repository-parsing-plugin/v0",
  "kind": "SpecHarvesterRepositoryParsingPluginDecision",
  "schemaVersion": 1,
  "authority": "producer_path_classification_only"
}
```

The artifact is producer review evidence. It explains path classification. It
does not make generated package claims authoritative.

## Inputs

Plugins receive local, bounded, reviewable inputs:

- repository source manifest metadata;
- resolved local checkout path;
- selected repository id and package family;
- expected revision or ref;
- detected ecosystem and labels;
- workspace inventory;
- package manifests and package roots;
- analyzer plan ids;
- optional operator-selected parser profile id.

Plugins must not perform network discovery, dependency installation, code
execution, or registry lookups.

## Outputs

Each plugin emits path classification decisions:

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

Required fields are `path`, `role`, `appliesToPackageId`, `reasonCodes`,
`confidence`, `publicInterfaceEligible`, and `semanticUsageEligible`.

## Rule Precedence

Rules apply deterministically:

1. explicit operator override;
2. selected parser profile rule;
3. language/package manager rule;
4. generic repository classifier rule;
5. conservative default fallback.

The fallback prefers `semantic_usage` or `ignored` over `public_interface` for
documentation, examples, tests, fixtures, generated output, and tooling.

## FastAPI Motivating Case

A future Python web-framework profile should treat `fastapi/` package code as
public interface evidence and treat `docs_src/`, tutorials, examples, and
tests as semantic usage evidence unless an explicit plugin rule promotes a
path.

Documentation remains valuable. It can support intent, terminology,
capabilities such as HTTP routing and OpenAPI generation, and local AI
enrichment. It should not create public API symbols such as tutorial
`read_item()` functions or example `app` variables.

## Analyzer Interaction

```text
source manifest
  -> repository parser plugin decisions
  -> analyzer path selection
  -> public_interface_index
  -> draft candidate
  -> AI enrichment / quality report / handoff
```

Semantic usage evidence may still be available to README/API-contract
semantic hints, package-set AI enrichment requests, author-ready quality
reports, static viewer context, and maintainer review notes.

## Decision Report

Future parser plugin output should summarize selected profile id and version,
matched rules, unmatched fallback count, counts by role, public-interface path
count, semantic-usage path count, ignored path count, blocked paths, operator
overrides, and non-authority statements.

The report should be hashable and referenceable from producer receipts and
handoff artifacts.

## Parser Profile Fixture

P36-T2 adds the first machine-readable parser profile fixture:

```text
tests/fixtures/repository_parsing_profiles/python-web-framework-v0.example.json
```

The fixture uses `apiVersion:
spec-harvester.repository-parsing-profile/v0`, `kind:
SpecHarvesterRepositoryParsingProfile`, `schemaVersion: 1`, `authority:
producer_path_classification_profile_only`, and profile id
`python.web_framework.v0`.

It records rule precedence, evidence roles, path role rules, fallback behavior,
sample FastAPI-like decisions, and non-authority statements.

The fixture treats `fastapi/` package code as `public_interface` evidence and
treats `docs_src/`, docs, examples, and tests as non-public-interface evidence
by default.

```text
fastapi/applications.py -> public_interface
docs_src/first_steps/tutorial001.py -> semantic_usage
tests/test_applications.py -> test
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
