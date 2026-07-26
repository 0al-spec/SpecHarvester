# P52-T9 Phase 52 Exit Decision

P52-T9 records a `go_with_guardrails_for_maintainer_disposition` decision for
the controlled 50-repository corpus. It makes the resulting proposal-only
evidence available for human maintainer disposition; it does not approve
automatic package acceptance, registry promotion, or corpus expansion.

## Basis

P52-T7 processed all 50 repositories with 100% Codex completion,
schema-validity, and repository-specificity rates, and zero unsupported claims.
Its historical strict static rate was 96% (48/50). P52-T10 then confirmed that
the two missing outcomes were filename-policy false negatives: pinned `uv` and
`actix-web` each now have two recognized license files and no
`missing_license_file` error. The original P52-T6 48/50 report remains intact.

P52-T8 triaged the 50 static packages and 50 Spark draft sidecars. Its two
license caveats are resolved by P52-T10, so no remaining Phase 52 blocker
prevents maintainer disposition.

The durable record is
`tests/fixtures/phase_52_exit_decision/p52-t9-phase-52-exit-decision.example.json`.

## Evidence Version Transition

P52-T8 retains the P52-T7 fixture digest that existed when triage was recorded:
`sha256:949cb6f...`. The current P52-T7 fixture is
`sha256:a711e4d...` because its P52-T8 review corrected static
execution-boundary fixture fields. No Codex quality metric, proposal, or
registry-authority outcome changed. P52-T9 records both identities explicitly
instead of silently treating the two evidence versions as interchangeable.

## Guardrails

- Maintainers may inspect and explicitly disposition the selected evidence.
- No package or relation is accepted automatically.
- Registry truth, metadata publication, baseline seeding, and `preview_only`
  removal remain prohibited.
- Expansion beyond the approved 50-source corpus needs a separate planned phase
  and explicit operator selection.

## Boundary

P52-T9 did not rerun collection, invoke AI, clone or fetch repositories,
install dependencies, invoke package managers, execute harvested code, run
adapters, or persist raw prompts, provider responses, secrets, or
chain-of-thought.
