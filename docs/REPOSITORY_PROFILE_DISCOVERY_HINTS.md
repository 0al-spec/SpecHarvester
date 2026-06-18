# Repository Profile Discovery Hints

Status: Phase 37 generic vocabulary.

Repository profile detection can emit advisory downstream hints after it
selects or overrides a repository profile. These hints are intentionally
language- and framework-agnostic. They describe likely path roles inside a
repository. The hint boundary does not accept packages, does not accept
relations, does not remove `preview_only`, and does not publish registry
metadata.

## Artifact Shape

The generic vocabulary is versioned as:

```json
{
  "apiVersion": "spec-harvester.repository-profile-hints/v0",
  "kind": "SpecHarvesterRepositoryProfileHintVocabulary",
  "schemaVersion": 1,
  "authority": "producer_profile_hint_vocabulary_only"
}
```

The fixture is:

```text
tests/fixtures/repository_profile_detection/generic-hint-vocabulary.example.json
```

Each hint records:

- `hint`: stable machine-readable hint id;
- `title`: human-readable label;
- `pathSubject`: what the path denotes;
- `summary`: short meaning;
- `consumerAction`: safe default reviewer/consumer action;
- `nonAuthorityStatements`: explicit boundary statements.

## Generic Vocabulary

| Hint | Path subject | Safe consumer action |
| --- | --- | --- |
| `package_set_root` | workspace root | review as candidate package-set root |
| `member_package` | package root | review as candidate member package |
| `meta_package` | package root | review as meta or aggregate package |
| `primary_package` | package root | review as primary public package |
| `cli_package` | package root | review as command-line surface |
| `bridge_package` | package root | review as adapter or bridge package |
| `plugin_package` | package root | review as extension surface |
| `example_package` | package root | exclude from primary members unless explicitly selected |
| `test_package` | package root | exclude from public interface claims by default |
| `documentation_source` | documentation path | use as semantic usage evidence |
| `generated_artifact` | source or output path | treat as generated or build output |
| `internal_utility` | package or source path | exclude from primary public claims by default |
| `evidence_only` | evidence path | retain as evidence without candidate identity |

## Current Producers

Current generic package-set detection emits:

- `package_set_root` for detected workspace roots;
- `member_package` for member package manifest parents;
- `documentation_source` for documentation paths.

P37-T5 does not make every hint producer active. It defines the shared
vocabulary so future profile plugins can emit the same ids without inventing
language-specific names.

## Non-Authority Boundary

Repository profile discovery hints are producer-side evidence only.

They do not:

- accept packages;
- accept relations;
- publish registry metadata;
- remove `preview_only`;
- treat profile hints as registry truth;
- mutate source candidates;
- replace maintainer review.

Consumers may use hints to explain proposed scope, prepare reviewer UI, or
queue future drafting decisions. Consumers must not silently promote a hint
into accepted registry state.

## Relationship to Profile Selection

Repository profile selection answers:

```text
Which profile should apply to this repository?
```

Discovery hints answer:

```text
What likely role does this path play under the selected profile?
```

Parser profiles still answer a different question:

```text
Which files are public interface evidence, semantic usage evidence, tests,
examples, generated artifacts, or internal tooling?
```

These layers can be composed, but none of them is registry authority.
