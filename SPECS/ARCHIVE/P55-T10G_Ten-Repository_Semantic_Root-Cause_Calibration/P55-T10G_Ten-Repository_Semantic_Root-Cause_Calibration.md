# P55-T10G Ten-Repository Semantic Root-Cause Calibration

## Objective

Run one bounded Codex 5.3 Spark calibration over ten preselected P55-T10C
repositories and determine whether the T10D repair-context, T10E product-profile,
and T10F relevant-intent-routing changes materially improve semantic proposals.

## Frozen Scope

- Targets: `axios-axios`, `n8n-io-n8n`, `firecrawl-firecrawl`,
  `bitcoin-bitcoin`, `excalidraw-excalidraw`, `openai-codex`,
  `thedotmack-claude-mem`, `angular-angular`, `electron-electron`, and
  `freecodecamp-freecodecamp`.
- Baseline: immutable P55-T10C report and proposal-record archive.
- Provider: Codex 5.3 Spark through the existing `codex exec` adapter.
- Attempt, repair, timeout, evidence, and output budgets remain those of the
  retained-corpus semantic campaign.
- No target substitution, threshold change, or recovery-provider run is allowed
  after results are observed.

## Deliverables

- A digest-bound calibration plan connecting every target to its P55-T10C
  repository, revision, candidate, packet, and baseline-record identity.
- A resumable runner that rebuilds current semantic-author input packs from the
  pinned P53 source and handoff evidence and runs only the ten frozen targets.
- A deterministic report and portable archive comparing purpose accuracy,
  generic-intent reuse and reduction, direct versus repaired completion,
  false novelty, provider failures, quality status, and estimated reviewer edit
  burden against P55-T10C.
- Per-target root-cause classification showing whether remaining failure comes
  from provider transport, repair, evidence/profile construction, routing,
  generic contradiction, or another quality diagnostic.
- Tests, durable evidence, documentation, validation report, and FLOW review.

## Frozen Success Criteria

- All ten targets have one terminal record and no unaccounted provider outcome.
- Purpose accuracy rate is at least `0.85`, schema-valid proposal rate is `1.0`,
  evidence-supported claim rate is at least `0.95`, and estimated reviewer edit
  burden is at most `0.25`, using the P55-T5 policy and failures in denominators.
- Generic-intent reuse is lower than the same ten P55-T10C baseline records.
- At least one previously repaired generic-reuse case either removes the generic
  intent or ends with an explicit contradiction/quality diagnosis rather than a
  silently accepted generic-only proposal.
- False novelty, duplicate experimental IDs, and duplicate experimental semantic
  stems are all zero.
- Raw prompts, raw responses, hidden reasoning, credentials, and machine-local
  paths are absent from durable evidence.

## Acceptance Criteria

- The plan fails closed on any target, baseline archive, source revision,
  candidate packet, model, policy, or digest drift.
- The run executes no repository code or package manager and performs no
  acceptance, materialization, canonicalization, SpecPM mutation, registry
  mutation, or publication.
- Comparison metrics and root-cause classes are reproducible from the durable
  records and immutable baseline.
- Full Python tests pass with at least 90% coverage; Ruff, formatting, Swift
  manifest/docs, JSON integrity, and diff checks pass.

## Dependencies

- P55-T10C immutable baseline evidence.
- P55-T10D preserved repair request context.
- P55-T10E deterministic semantic product profile.
- P55-T10F relevant-intent routing and generic contradiction gate.

## Non-Goals

- Revalidating all 46 generic-intent records; that remains P55-T10H.
- Running LM Studio or a quota-recovery model.
- Changing quality thresholds after execution.
- Treating a generated intent as canonical or approved.
