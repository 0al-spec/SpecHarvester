# P52-T4 Twenty-Repository Controlled Pilot

**Status:** Planned
**Phase:** Phase 52. Controlled Popular Repository Corpus with Codex Spark
**Task:** `P52-T4`
**Depends On:** `P52-T3` Five-Repository Controlled Calibration

## Goal

Run one bounded Phase 52 pilot over exactly twenty operator-provided, pinned,
clean local repository checkouts. First produce deterministic static-only
evidence. Only after it passes, and after the operator confirms that LM Studio
provider-side sensitive request/response logging is disabled, run separate
proposal-only LM Studio and Codex Spark controls against the same static draft
inputs.

The task measures whether the successful five-repository integration remains
reliable at a larger, deliberately mixed corpus. It is not a 50-100 repository
gate and grants neither model nor static output registry authority.

## Deliverables

- Add a P52-T4 manifest containing exactly twenty public, operator-provided
  local checkouts, immutable revisions, repository URLs, package identifiers,
  and shape/ecosystem labels.
- Add a dedicated controlled-pilot runner and CLI command. Preserve the
  P52-T3 exactly-five `controlled-calibration` contract and report schema.
- Reject a source when its checkout is missing, has a mismatched HEAD, has any
  staged, unstaged, or untracked change, uses a mutable `ref`, or is not one of
  the exact twenty manifest entries.
- Run the complete static-only baseline before opening an LM Studio connection
  or invoking Codex. Record per-repository completion, elapsed time, and a
  bounded concurrency receipt.
- Run LM Studio only with the existing request-side JSON Schema contract, not
  by altering LM Studio's Chat Template. Record sanitized status, aggregate
  usage, schema outcomes, and warnings without raw provider material.
- Run Codex Spark through P52-T2's read-only, ephemeral stage and schema-
  validated final-message handoff. Keep its execution receipt, schema result,
  and aggregate duration only.
- Emit a durable proposal-only report and a checked-in representative fixture;
  document the actual static/model outcomes, quality metrics, and whether the
  stop policy unlocks P52-T5.
- Add focused runner, CLI, report, and documentation-contract coverage.

## Acceptance Criteria

- The pilot uses exactly twenty existing clean local Git checkouts with a
  complete revision match. It never clones, fetches, restores, or modifies a
  checkout.
- Static-only collection finishes before either model branch begins. A static
  failure prevents both model branches and produces a bounded stopped report.
- The runner declares and records bounded concurrency. Parallel work cannot
  change report ordering, source identity, or the proposal-only boundary.
- LM Studio is invoked only after the operator-controlled provider-log-clean
  precondition is recorded as satisfied. `response_format.type: json_schema`
  remains request-side and raw prompts/responses are not persisted.
- Codex receives only compact allowlisted evidence in an ephemeral read-only
  stage; it has no original checkout, writable add-directory, network/provider
  endpoint, dependency installation path, package manager, harvested code, or
  adapter source. Only a schema-valid final message may enter the existing
  external `--model-output` handoff.
- Model sidecars remain proposal-only: they cannot accept packages or
  relations, publish metadata, seed baselines, remove `preview_only`, or become
  registry truth.
- The report evaluates the Phase 52 thresholds: static completion >=95%, Codex
  completion >=90%, schema-valid output >=98%, repository specificity >=80%,
  unsupported claims <=5%, and a human-review sample of at least ten percent
  and ten candidates. It explicitly records PASS, STOP, or BLOCKED; it does
  not silently retry a failed scale gate.
- Durable artifacts contain no raw prompts, raw provider responses, Codex
  stdout/stderr, session state, secrets, or chain-of-thought.

## Non-Goals

- Do not acquire additional repositories or repair source checkouts.
- Do not run the P52 50-100 static-only or Codex gates, triage their output, or
  make a Phase 52 exit decision.
- Do not install dependencies, invoke package managers, execute harvested code
  or adapters, accept packages or relations, publish registry metadata, seed
  baselines, or remove `preview_only`.
- Do not change a user's LM Studio Chat Template or provider logging settings.

## Validation Plan

- Run focused controlled-pilot, CLI, provider payload, external-handoff, and
  documentation-contract tests.
- Validate each durable JSON artifact with `python -m json.tool`.
- Verify a fixture-driven static-only run precedes any model receipt, and verify
  blocked/failed preconditions prevent model invocation.
- Run the Flow gates from `.flow/params.yaml`: full pytest with coverage >=90%,
  Ruff check and format check, Swift package manifest and DocC build, and
  `git diff --check`.
