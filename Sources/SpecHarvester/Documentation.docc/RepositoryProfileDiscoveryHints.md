# Repository Profile Discovery Hints

Repository profile discovery hints are a generic vocabulary for advisory path
roles emitted by repository profile detection.

The vocabulary artifact is:

```json
{
  "apiVersion": "spec-harvester.repository-profile-hints/v0",
  "kind": "SpecHarvesterRepositoryProfileHintVocabulary",
  "schemaVersion": 1,
  "authority": "producer_profile_hint_vocabulary_only"
}
```

The fixture lives at:

```text
tests/fixtures/repository_profile_detection/generic-hint-vocabulary.example.json
```

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

Current generic package-set detection emits `package_set_root`,
`member_package`, and `documentation_source`.

## Boundary

Hints are producer-side evidence only. The hint boundary does not accept
packages, does not accept relations, does not publish registry metadata, does
not remove `preview_only`, and does not treat profile hints as registry truth.
It also does not mutate source candidates or replace maintainer review.

Profile selection answers which profile applies. Discovery hints answer what
likely role a path plays under that profile. Parser profiles still decide file
evidence roles such as public interface, documentation, example, test,
generated, or internal.
