# P56-T2 Complete Spec Authoring Skill

The repository-owned entry point is
[specpm-author-candidate](../skills/specpm-author-candidate/SKILL.md).
Contract version 1 targets `specpm.dev/v0.1`. Copy the entire skill directory
into a caller-controlled environment; do not copy the maintainer checkout or
evaluator artifacts. It has no dependency on personal installed skills.

## Delivered Surface

- An investigative workflow following the intended product, not the first
  manifest, with justified boundaries and explicit unknowns.
- A field guide mapping scenarios, interfaces, constraints, dependencies,
  effects, evidence and uncertainty into existing SpecPM fields.
- A valid abstract starter and a fictional Rowpick example with partial-output
  failure behavior, read effects and explicit unknowns.
- Independent SpecPM validation in CI, including negative binding tests.

The example is teaching material, not an AI run or real-repository quality
evidence. Neither example belongs to the frozen pilot corpus. The skill contains
no benchmark questions, answers, repository identities or scoring thresholds.
Precise natural-language purpose does not depend on inventing canonical intent
IDs; mappings are optional and require an approved caller-provided catalog.

## Invocation Contract

The caller supplies pinned source identity, intended scope, read allowlist,
output directory, trusted validation tool and resource/repair budgets. The
worker produces complete candidate files, not the historical semantic-patch
transport. This task does not connect the skill to that transport or introduce
a second provider adapter. T3 chooses and enforces the file-producing runner.

For the Phase 56 experiment, T3 takes budgets from T1 and locks skill/template
hashes before T4. It must isolate source reads and output writes, keep evaluator
data inaccessible and preserve validation/usage receipts. Skill instructions
alone do not enforce runtime protections.

Output remains preview_only and draft. Validation cannot grant publication
authority or establish factual quality. Unknown license, platform support,
dependency resolution and runtime behavior must not become plausible defaults.

## Compatibility and Verification

The workflow adapts SpecPM's MIT-licensed specpm-author-spec guidance. Fields
were checked against SpecPM commit `8a5ce3dece3d18bf8f601a5a599520bd520c7839`,
especially validate_manifest, validate_boundary_spec, evidence support targets
and the Package Model guide. CI validates against the checked-out SpecPM version
to detect drift. Record the actual validator version in T3's pre-run lock.

From this repository with an adjacent SpecPM checkout:

```sh
PYTHONPATH=../SpecPM/src:src .venv/bin/python -m pytest tests/test_authoring_skill_assets.py -q
PYTHONPATH=../SpecPM/src .venv/bin/python -m specpm.cli validate skills/specpm-author-candidate/assets/template --json
PYTHONPATH=../SpecPM/src .venv/bin/python -m specpm.cli validate skills/specpm-author-candidate/assets/example --json
```

Both assets should have zero errors and only preview_only_package. The normal
Python-only job checks portable structure without requiring SpecPM; external
validator tests explicitly skip there and run in the mandatory integration job.
No harvested source command, live authoring provider or registry operation runs.
