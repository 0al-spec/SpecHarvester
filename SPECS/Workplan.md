# SpecHarvester Workplan

Status: Draft
Created: 2026-05-17
Updated: 2026-05-29
Input: `PRD.md`, `docs/ROADMAP.md`, current repository implementation

## Working Rules

- Keep harvesting local-first and deterministic.
- Treat every harvested repository file as untrusted data.
- Prefer static metadata, AST, and parser output over LLM discovery.
- Do not execute package scripts, install harvested dependencies, or access
  secrets.
- Preserve evidence paths, file digests, analyzer versions, and policy notes.
- Use SpecPM validation before promotion.
- Keep generated candidates preview-only until reviewed.
- Keep Flow artifacts small enough to be useful in code review.

## Phase 0. Flow Operating Baseline

- [x] `P0-T1` Configure Flow operating scaffold.

Acceptance:

- `SPECS/COMMANDS/FLOW.md` exists.
- `SPECS/PRD.md` and `SPECS/Workplan.md` exist.
- `SPECS/INPROGRESS/next.md` identifies the next recommended task.
- `SPECS/ARCHIVE/INDEX.md` exists.
- Required quality gates are documented and locally runnable.

## Phase 1. Public Interface Indexing

- [x] `P1-T1` Define `PublicInterfaceIndex` snapshot schema.
- [x] `P1-T2` Add Python static public API analyzer using `ast`.
- [x] `P1-T3` Add JavaScript and TypeScript manifest/export analyzer.
- [x] `P1-T4` Evaluate Tree-sitter as the shared syntax indexing layer.
- [x] `P1-T5` Integrate public interface evidence into deterministic drafting.

Acceptance:

- Interface extraction runs without executing harvested repository code.
- Analyzer outputs include provenance, analyzer version, and source digests.
- `draft` can build richer `interfaces.inbound` entries from public interface
  evidence.
- LLM refinement can consume a compact public interface summary instead of raw
  source files.

## Phase 2. Analyzer Policy and Cache

- [x] `P2-T1` Add analyzer trust policy fields to harvest snapshots.
- [x] `P2-T2` Add per-file analyzer cache keyed by file digest and analyzer
  version.
- [x] `P2-T3` Add parse diagnostics and partial-index behavior.
- [x] `P2-T4` Document sandbox requirements for analyzers that need build
  tools.

Acceptance:

- Static analyzers fail closed and record diagnostics.
- Re-running harvest on unchanged files reuses cached analyzer results.
- Any analyzer requiring build tools is explicitly marked and sandboxed.

## Phase 3. Batch Harvesting

- [x] `P3-T1` Read repository source manifests from `inputs/*.yml`.
- [x] `P3-T2` Collect snapshots for selected repositories into deterministic
  candidate paths.
- [x] `P3-T3` Emit batch validation reports with confidence and policy notes.

Acceptance:

- Batch mode never executes package content.
- Batch outputs are deterministic for the same source revision and config.

## Phase 4. SpecPM Proposal Integration

- [x] `P4-T1` Prepare PR-ready accepted package manifest entries.
- [x] `P4-T2` Add proposal preflight checks for accepted-source diffs.
- [x] `P4-T3` Extend GitHub proposal automation documentation and validation.

Acceptance:

- Trusted maintainers can propose reviewed accepted-source changes into SpecPM.
- Ordinary pull requests cannot use write credentials for cross-repository
  mutation.

## Phase 5. Governance Reports

- [x] `P5-T1` Add duplicate intent and capability claim report.
- [x] `P5-T2` Add namespace and upstream relationship review report.
- [x] `P5-T3` Add license and provenance risk report.

Acceptance:

- Generated reports remain advisory review artifacts.
- Reports do not accept, reject, publish, install, or execute package content.

## Phase 6. Smoke-Test Feedback

- [x] `P6-T1` Discover nested Swift package manifests during static harvest.
- [x] `P6-T2` Infer candidate license metadata from allowlisted LICENSE files.
- [x] `P6-T3` Make namespace and upstream owner comparison case-insensitive.
- [x] `P6-T4` Add reproducible local smoke-test fixture documentation.

Acceptance:

- Swift repositories with nested `Package.swift` files are collected with useful
  package-manifest evidence without executing SwiftPM or package code.
- Generated candidates can infer common license identifiers from static LICENSE
  files when package manifests do not provide license metadata.
- Governance namespace/upstream reports do not flag casing-only GitHub owner
  differences as mismatches.
- Smoke testing remains local-only, deterministic, and clearly separated from
  committed generated candidate outputs.

## Phase 7. Smoke-Test Signal Quality

- [x] `P7-T1` Treat package namespace matches against upstream repository names
  as valid namespace evidence.
- [x] `P7-T2` Derive less generic Swift package intents from package products
  and manifests.
- [x] `P7-T3` Distinguish absent license evidence from ambiguous unknown license
  evidence.
- [x] `P7-T4` Add a compact local smoke triage summary for batch and governance
  report output.

Acceptance:

- Governance namespace/upstream reports avoid false positives when a package
  namespace matches the upstream repository name but not the GitHub owner.
- Swift-only candidates avoid duplicate generic metadata intents when static
  product or manifest evidence can support a more specific claim.
- License provenance reports explain whether `UNKNOWN` means no license evidence
  was found or license-like evidence was present but not classifiable.
- Local smoke output can be summarized into a stable review artifact without
  committing generated candidates.

## Phase 8. Accepted Specification Update Lifecycle

- [x] `P8-T1` Document accepted package update lifecycle and immutability policy.
- [x] `P8-T2` Add accepted-vs-candidate package diff report.
- [x] `P8-T3` Classify update proposals by metadata, interface, license,
  provenance, capability, and intent impact.
- [x] `P8-T4` Add PR-ready SpecPM update proposal flow for new accepted package
  versions.
- [x] `P8-T5` Add correction and errata path for fixing accepted metadata
  without treating upstream content as changed.
- [x] `P8-T6` Add accepted package version immutability guard for update
  proposals.

Acceptance:

- Accepted SpecPM package versions are treated as immutable registry evidence
  unless a correction path explicitly records the reason for metadata repair.
- Noticeable upstream module changes produce a new reviewed candidate from a
  pinned source revision and a reviewable diff against the currently accepted
  package version.
- Update proposals preserve audit trail: source revision, evidence digests,
  old/new package version, changed claims, validation status, and reviewer
  notes.
- SpecHarvester can propose update PRs to SpecPM, but SpecPM review and merge
  remain the acceptance boundary.
- Update preflight rejects silent mutation of an already accepted
  `package_id@version` unless an explicit correction path and audit record are
  present.

## Phase 9. Semantic Draft Quality

- [x] `P9-T1` Derive semantic intent claims from trusted static documentation and
  public API evidence.
- [x] `P9-T2` Build a deterministic semantic evidence index for domain-level
  draft intent generation.

Acceptance:

- Drafts prefer meaningful domain-level intent claims when deterministic DocC,
  PRD, README, or public interface evidence supports them.
- Swift package product intents remain available as fallback evidence, not as the
  primary claim when richer intent evidence exists.
- Harvested package-manifest evidence excludes generated dependency checkouts,
  build directories, fixtures, and historical drafts from primary package
  interface claims.
- Semantic draft generation receives compact ranked domain clusters from
  deterministic utilities rather than raw markdown heading bags or LLM
  inference.
- Domain clusters preserve evidence paths and support weak-model/refinement
  workflows without treating model output as registry authority.
- Generated candidates still remain preview-only and never execute package code,
  dependency installers, build scripts, or network probes.

## Phase 10. Language and Package Ecosystem Profiling

- [x] `P10-T1` Define a deterministic `ProjectProfile` schema for language,
  package ecosystem, package manager, manifest, confidence, provenance, and
  analyzer-plan evidence.
- [x] `P10-T2` Add manifest-first ecosystem detectors for Swift/SPM, JavaScript
  and TypeScript package managers, Python, Java/Kotlin, Go, PHP, C/C++,
  Objective-C/iOS, Ruby, and Rust without executing package code.
- [x] `P10-T3` Evaluate and integrate trusted language classification and
  vendored/generated-file filtering from established tools such as
  GitHub Linguist-compatible classifiers, `go-enry`, `Syft`, `ScanCode`, and
  Universal Ctags where licensing and deterministic operation are acceptable.
- [x] `P10-T4` Wire `ProjectProfile` into analyzer orchestration so
  `collect-batch` can recommend or emit public-interface indexes from existing
  static analyzers, including Python `ast` and JavaScript/TypeScript export
  analyzers, before `draft` runs.
- [x] `P10-T5` Add language-neutral semantic extraction for documentation-first
  repositories so README/API-contract evidence can produce meaningful intent
  clusters even when no supported package manifest is present.
- [x] `P10-T6` Add a multi-language smoke matrix covering local repositories and
  synthetic fixtures for npm, SPM, Gradle/Maven, Go modules, Composer, CMake,
  Xcode/CocoaPods, RubyGems, and Python packaging.

Acceptance:

- Repository classification is deterministic, local-only, and never executes
  package scripts, build systems, dependency installers, or network probes.
- `ProjectProfile` preserves evidence paths, file digests, detector versions,
  confidence reasons, and ambiguity diagnostics.
- Manifest evidence is primary when present, while language classifiers and file
  statistics only refine confidence or identify missing manifests.
- Analyzer orchestration produces compact public-interface and semantic evidence
  for weak-model drafting without requiring raw source dumps.
- External tool adoption is documented with license, trust boundary,
  determinism, vendored/generated filtering behavior, and fallback behavior when
  the tool is unavailable.
- Smoke coverage includes Swift, JavaScript/TypeScript, Python, Java/Kotlin, Go,
  PHP, C/C++, Objective-C/iOS, Ruby, and at least one documentation-first
  repository with no recognized package manifest.

## Phase 11. SpecNode Integration Bridge

- [x] `P11-T1` Define the SpecHarvester-to-SpecNode artifact bundle and typed
  job contract for model-assisted candidate refinement without granting model
  output file-system or shell authority.
- [x] `P11-T2` Add a bounded `refine-preview` planning contract that packages
  `harvest.json`, `ProjectProfile`, optional `PublicInterfaceIndex`,
  `semanticEvidenceIndex`, validation reports, and draft candidate metadata as
  compact model input.
- [x] `P11-T3` Add an OpenAI-compatible provider adapter boundary for local
  SpecNode execution, including LM Studio discovery, model listing, health
  checks, timeout, retry, temperature, and token-budget policy.
- [x] `P11-T4` Define schema-validated model output for candidate patch
  proposals, provenance, usage receipts, and rejection reasons before any
  generated changes can be applied.
- [x] `P11-T5` Add integration smoke coverage using a local SpecNode-compatible
  provider with weak-model drafting inputs, while preserving deterministic
  fallback when no provider is available.
- [x] `P11-T6` Capture LM Studio `gpt-oss` response compatibility by requiring
  OpenAI-compatible `json_schema` response format for structured output and a
  safe parser fallback for `gpt-oss` channel-wrapped JSON in text mode.

Acceptance:

- SpecHarvester remains the deterministic evidence producer and never treats
  model output as accepted registry truth.
- SpecNode owns local provider discovery, model execution, typed job policy,
  provenance, and usage receipt generation.
- Model-assisted refinement consumes compact deterministic artifacts instead of
  raw repository source dumps.
- The bridge rejects arbitrary prompts, shell execution, LLM tools, network
  expansion, and filesystem access outside the candidate workspace.
- Provider-specific behavior is optional and can be disabled without breaking
  `collect-local`, `collect-batch`, `draft`, validation, or smoke tests.
- LM Studio compatibility guidance documents that `json_object` is not assumed
  and that `json_schema` is the preferred structured-output mode for
  `openai/gpt-oss-20b`.

## Phase 12. Popular Repository Smoke Hardening

- [x] `P12-T1` Accept common public license filenames such as `LICENSE.txt` in
  strict public mode while keeping the current hard failure for repositories
  with no license-like file.
- [x] `P12-T2` Add a deterministic Go public interface analyzer or
  manifest-plus-source fallback for `go.mod` projects, producing compact
  package/function/type
  evidence without executing `go`, package scripts, tests, or network probes.
- [x] `P12-T3` Improve domain intent inference from public interface indexes,
  package metadata, README headings, and documentation evidence so popular web
  frameworks such as Flask and Gin do not collapse to only generic
  `intent.api.contract_surface` / `intent.developer.tooling_surface` claims.
- [x] `P12-T4` Align `PublicInterfaceIndex` evidence with the SpecPM validation
  contract by keeping SpecPM `0.2.0`'s known `public_interface_index` kind,
  preserving explicit artifact metadata, and adding CI validation coverage.
- [x] `P12-T5` Remove or remap generated evidence support targets that SpecPM does
  not currently declare, including `provides.capabilities.intentIds`, so
  generated candidates validate without avoidable advisory warnings.
- [x] `P12-T6` Promote the Flask/Gin popular-repository smoke scenario into
  reproducible local smoke documentation or synthetic tests covering Python with
  `LICENSE.txt`, Go module manifest-only behavior, SpecPM validation warnings,
  and governance triage output.

Acceptance:

- Strict public mode accepts allowlisted license filenames with safe extensions
  such as `.txt`, but still rejects repositories with no license evidence.
- Go repositories produce deterministic, local-only public interface or fallback
  evidence that is useful to weak-model drafting.
- Generated intents for popular web frameworks identify framework/domain
  semantics when supported by static evidence.
- SpecPM validation warnings caused by `public_interface_index` and generated
  support-target vocabulary are either eliminated or tracked as explicit
  cross-repository contract work.
- Flask and Gin smoke runs are reproducible and documented without committing
  generated `.smoke/` output.

## Phase 13. Prompted Refinement Quality Loop

- [x] `P13-T1` Define a versioned SpecNode refinement prompt contract that turns
  `compactModelInput`, output schema, evidence-reference rules, negative-claim
  policy, and confidence calibration into repository-owned deterministic prompt
  templates instead of ad-hoc runtime wording.
- [x] `P13-T2` Add a clean-context semantic review pass for generated
  `SpecNodeRefinementResult` proposals, where a second model sees only the
  deterministic evidence bundle, the generated candidate or patch proposal, and
  a strict review rubric, then emits typed findings instead of mutating the
  candidate directly.
- [x] `P13-T3` Add feedback-driven refinement retry orchestration that reuses the
  same immutable deterministic artifacts, converts semantic review findings into
  bounded retry directives, caps retry attempts, and records an audit trail from
  initial refinement through review and retry.

Acceptance:

- Prompt text used for SpecNode refinement is a versioned, reviewable contract
  with deterministic inputs, schema-bound outputs, and tests covering known
  weak-model failure modes such as describing SpecPM generation instead of the
  target package behavior.
- Evidence references are constrained to known artifact IDs or generated
  evidence IDs; unknown, collapsed, or invented references are rejected before a
  proposal can be considered reviewable.
- Semantic review runs with clean context: no first-pass prompt transcript, no
  chain-of-thought, no provider logs, no raw source access, and no authority to
  directly edit candidate files.
- Review findings use a typed taxonomy such as wrong package intent, unsupported
  capability claim, missing evidence reference, overconfident confidence score,
  unsafe negative claim, and schema-policy mismatch.
- Retry orchestration reuses the original deterministic evidence snapshot unless
  source artifacts changed, preserves attempt linkage, enforces a maximum retry
  count, and keeps all model output proposal-only.

## Phase 14. Live SpecNode Provider Smoke

- [x] `P14-T1` Add a manual LM Studio live retry smoke harness that exercises
  the SpecNode refinement feedback loop through an OpenAI-compatible local
  endpoint without making ordinary CI depend on local model infrastructure.

Acceptance:

- Live smoke is disabled by default and runs only when explicit environment
  variables provide a local OpenAI-compatible base URL and model ID.
- The harness can call LM Studio `/v1/chat/completions`, parse direct JSON or
  observed `gpt-oss` channel-wrapped JSON, and adapt responses into
  `SpecNodeCompatibleProvider` and `SpecNodeSemanticReviewer` test doubles.
- The smoke scenario proves a two-attempt feedback loop: first review requests
  revision, retry context is passed into the second provider call, and the final
  run records an approved or capped deterministic audit trail.
- The harness records provider/model metadata and token usage in local output
  without committing generated candidate artifacts, raw prompts, provider logs,
  secrets, or model chain-of-thought.
- Unit coverage exercises the adapter and skip behavior without requiring LM
  Studio; the live pytest path is explicitly opt-in and safe to skip in CI.

## Phase 15. Real Repository Refinement Validation

- [x] `P15-T1` Add a reproducible real-repository refinement
  validation plan that defines local checkout selection, safe input manifests,
  command sequences, expected SpecHarvester-side artifacts, scoring rubric, and
  non-committed output policy for `collect -> draft -> artifact bundle ->
  optional external refinement -> semantic review report` runs.
- [x] `P15-T2` Add a local-only validation runner or script template that can
  orchestrate SpecHarvester-owned collection, drafting, artifact packaging,
  validation, and reporting steps against operator-supplied public repository
  checkouts, optionally invoking an existing external SpecNode-compatible
  provider boundary without implementing SpecNode runtime responsibilities.
- [x] `P15-T3` Add a structured quality report format for real-repository
  refinement runs, including package intent accuracy, capability/evidence
  support quality, SpecPM validation status, retry effectiveness, token usage,
  deterministic analyzer coverage, and human-review notes.
- [x] `P15-T4` Run and document a representative local validation matrix across
  several repository shapes such as Swift/SPM, JavaScript/TypeScript, Python,
  Go, documentation-first, and mixed-language projects, recording only compact
  triage summaries and failure classes.
- [x] `P15-T5` Convert repeated real-repository validation failures into
  follow-up Workplan tasks for deterministic analyzers, prompt contracts,
  external SpecNode contract integration, SpecPM compatibility, or documentation,
  instead of tuning ad-hoc prompts from individual outputs.
- [x] `P15-T6` Align the P15-T2 local validation runner with the P15-T3
  structured quality report contract, ensuring the runner writes a stable
  `run-report.json`, records candidate artifact locations and step outcomes in
  the shape consumed by `quality-report`, and resolves the current
  `draft.json` mismatch by either deriving quality input from generated
  `specpm.yaml` and `specs/*.spec.yaml` artifacts or explicitly producing a
  documented draft summary artifact.

Acceptance:

- Real-repository validation remains local-only, opt-in, and safe for public
  checkout analysis: no package scripts, dependency installers, tests, build
  commands, registry calls, or arbitrary network probes are executed.
- The validation plan uses operator-supplied repository paths or manifests and
  does not commit harvested source snapshots, generated `.smoke/` outputs, raw
  prompts, provider transcripts, secrets, or model chain-of-thought.
- SpecHarvester does not implement SpecNode runtime, provider discovery, model
  execution, scheduling, provider lifecycle, or provider-specific orchestration;
  those remain SpecNode responsibilities behind the existing external contract.
- Each run preserves deterministic artifact references, source revisions,
  analyzer versions, file digests, SpecPM validation status, retry audit state,
  provider/model metadata, and token usage where available.
- Quality reporting distinguishes deterministic evidence gaps from model
  interpretation failures, SpecPM contract mismatches, and repository-specific
  ambiguity.
- Repeated failure classes become explicit Workplan follow-ups so improvements
  happen through analyzers, schemas, prompt contracts, or validation policy
  rather than hidden manual edits.

## Phase 16. Real Repository Signal Quality Hardening

- [x] `P16-T1` Count generated `public-interface-index.json` artifacts in
  structured quality-report analyzer coverage so Python and Go candidates with
  executed public API analyzers are not downgraded to `weak` coverage only
  because the coverage derivation misses colocated interface-index evidence.
- [x] `P16-T2` Improve license provenance classification for collected license
  files such as Flask's `LICENSE.txt`, preserving strict missing-license errors
  while distinguishing recognizable license text from genuinely ambiguous
  unknown license evidence in governance reports.
- [x] `P16-T3` Normalize package identity and namespace/upstream comparisons
  across hyphen, underscore, separator, and case variants so generated package
  IDs like `navigation_split_view.core` do not create low-signal namespace
  advisories for upstream repositories such as `NavigationSplitView`.
- [x] `P16-T4` Reduce broad duplicate semantic intent claims by adding
  deterministic evidence thresholds or repository-shape constraints for generic
  documentation/API/tooling intents before candidates are compared in
  governance reports.
- [x] `P16-T5` Rerun the representative local validation matrix after P16-T1
  through P16-T4 and document whether advisory counts, analyzer coverage, and
  failure classes improved without committing generated `.smoke/` artifacts.
- [x] `P16-T6` Add an advisory duplicate-code quality report that detects
  repeated implementation blocks in repository source, starts non-blocking for
  baseline collection, and can later be promoted to a fail-on-new-duplicates CI
  gate.
- [x] `P16-T7` Integrate an established duplicate-code detector backend,
  starting with Python `pylint` `duplicate-code`/`R0801`, behind the existing
  `SpecHarvesterCodeDuplicationReport` contract and run it as a non-blocking
  CI baseline check.
- [x] `P16-T8` Evaluate and integrate a multi-language duplicate-code detector
  backend such as `jscpd` behind `SpecHarvesterCodeDuplicationReport`, including
  licensing, deterministic JSON output, npm supply-chain, and CI ergonomics
  review before enabling it as an advisory baseline.
- [x] `P16-T9` Add lightweight architecture lint guardrails for the planned
  Elegant Objects refactor, covering helper/manager naming relapse,
  constructor I/O, static domain helpers, and duplicated manifest parser
  patterns before broad report-layer restructuring begins.
- [x] `P16-T10` Introduce a behavior-rich `SpecPackageManifest` object for
  reading `specpm.yaml` metadata, foreign artifacts, and claim sections as the
  first Elegant Objects seam before report modules are rewritten.
- [x] `P16-T11` Refactor accepted diff and namespace upstream reports to read
  manifests through `SpecPackageManifest`, reducing duplicated manifest parser
  code while preserving report JSON behavior.
- [x] `P16-T12` Introduce a behavior-rich report source records object for
  accepted/candidate `specpm.yaml` traversal, symlink handling, invalid manifest
  issue reporting, and deterministic record sorting across governance,
  namespace/upstream, and license provenance reports.
- [x] `P16-T13` Introduce a shared public API payload record object for
  validating cached analyzer entrypoints, symbols, diagnostics, and evidence
  paths across Python and Go public interface analyzers.
- [x] `P16-T14` Introduce a shared semantic keyword taxonomy object for
  documentation/API/tooling term groups currently duplicated between collector
  evidence extraction and draft semantic cluster generation.
- [x] `P16-T15` Introduce a shared public API analyzer options object for common
  source/package/output/trust inputs across Python, Go, and JS/TS analyzers
  while preserving language-specific analyzer behavior.
- [x] `P16-T16` Introduce a shared upstream issue evaluation object for
  namespace and license provenance reports so verified-upstream issue generation
  is represented once.
- [x] `P16-T17` Introduce behavior-rich real repository quality rating policy
  objects for duplicated draft/spec/source scoring guard clauses.
- [x] `P16-T18` Run a duplicate-code practical-minimum audit after P16-T15
  through P16-T17 and document whether any remaining builtin duplicate windows
  are intentional detector noise or require another refactor.

Acceptance:

- Signal-quality improvements are implemented through deterministic analyzers,
  report logic, normalization policy, or semantic evidence rules rather than
  one-off prompt edits.
- Each follow-up includes regression coverage using fixtures or scoped local
  smoke inputs for the real failure class it addresses.
- Static quality hardening can flag duplicated implementation policy such as
  allowlists, normalization predicates, schema fragments, and report issue-code
  logic before review has to catch drift manually.
- Established duplicate-code tools are preferred as primary detectors when
  their licensing, deterministic output, local-only execution, and CI ergonomics
  fit the repository.
- Architecture lint guardrails keep structural refactors reviewable by catching
  project-specific relapse risks that generic style linters do not understand.
- The local validation matrix can show whether advisory noise decreased while
  preserving strict public-source safety guarantees.
- Generated `.smoke/` inputs and outputs remain local-only and uncommitted.

## Phase 17. Elegant Objects Refactoring Strategy

- [x] `P17-T1` Add a deterministic procedural-style metrics report that counts
  top-level function span, method span, behavior-rich classes, DTO-only classes,
  largest functions, and module hotspots so EO progress is measured by behavior
  movement rather than subjective review impressions.
- [x] `P17-T2` Split the CLI execution shell from domain command behavior by
  introducing small command objects for selected `code-duplication-report`,
  `architecture-lint`, and report-generation flows while preserving parser
  flags, JSON error output, and exit-code behavior.
- [x] `P17-T3` Refactor report builders behind behavior-rich report objects one
  output contract at a time, starting with low-risk governance or accepted
  candidate reports and preserving report schemas, issue codes, and markdown
  output.
- [x] `P17-T4` Refactor public API analyzer pipelines into language-specific
  analyzer objects that use shared payload and option objects without hiding
  language-specific parse, diagnostic, symbol, or evidence decisions.
- [x] `P17-T5` Refactor collector and drafter behavior in thin vertical slices,
  adding characterization tests before moving repository profile, license
  inference, semantic evidence, intent profile, package draft assembly, or
  artifact-writing logic.
- [x] `P17-T6` Refactor SpecNode refinement orchestration after the report,
  analyzer, collector, and drafter seams are stable, keeping SpecHarvester-side
  provider, validation, retry, and unavailable-result objects inside the
  existing SpecNode contract boundary.

Acceptance:

- `docs/EO_REFACTORING_STRATEGY.md` remains the source strategy for sequencing,
  PR sizing, acceptance metrics, and stop conditions.
- Refactor tasks preserve public report schemas, CLI flags, exit codes, markdown
  output, issue codes, trust-boundary text, and SpecPM/SpecNode contracts unless
  a task explicitly changes them.
- Each implementation PR includes characterization coverage before moving mature
  procedural behavior.
- Procedural-style metrics show targeted top-level function span moving into
  named behavior-rich objects without counting DTO-only dataclasses as progress.
- `architecture-lint`, duplicate-code reports, full Python tests, coverage,
  ruff, Swift manifest, and DocC build remain green for refactor PRs that touch
  the relevant surfaces.

## Phase 18. Swift Public API Coverage

- [x] `P18-T1` Add a deterministic Swift public API analyzer that scans `.swift`
  sources for `public` and `open` declarations, emits `PublicInterfaceIndex`
  evidence, and plugs into project-profile analyzer orchestration without
  executing SwiftPM, build tools, package scripts, or repository code.

Acceptance:

- Swift public API extraction is deterministic, local-only, and records analyzer
  provenance, source digests, symbols, entrypoints, and diagnostics through the
  existing `PublicInterfaceIndex` contract.
- Swift/SPM project profiles can request the Swift analyzer through the existing
  analyzer-plan and orchestration registry.
- Drafting can consume the resulting `public-interface-index.json` through the
  existing BoundarySpec evidence path without Swift-specific drafter code.

## Phase 19. Static Spec Rendering

- [x] `P19-T1` Add a static HTML/JS renderer for generated SpecPM candidate
  packages, reading `specpm.yaml` and referenced `specs/*.spec.yaml` into a
  deterministic browser-safe JSON payload and emitting a self-contained static
  viewer without executing harvested repository code.

Acceptance:

- The renderer works on a local candidate directory and writes static assets
  suitable for GitHub Pages, file preview, or later extraction into a standalone
  repository.
- YAML parsing is performed by trusted local Python code using the same
  restricted, JSON-compatible assumptions expected by SpecPM, not by executing
  harvested package code or package scripts.
- The generated viewer presents package identity, capabilities, intents,
  BoundarySpec summaries, interfaces, evidence, effects, constraints, validation
  status, and raw normalized JSON.
- The implementation keeps the UI/data contract small enough to extract later
  and documents that SpecPM remains the validation and registry authority.

## Phase 20. Scoped Source Unit Harvesting

- [x] `P20-T1` Add a first-class source target model so `collect-local` and
  source manifests can harvest repository roots, scoped folders, or scoped files
  while preserving owning repository provenance, inherited root license evidence,
  and strict-public staged-change guarantees.
- [x] `P20-T2` Add deterministic Tuist manifest parsing for `Project.swift`,
  `Workspace.swift`, and `Tuist.swift`, extracting project names, targets,
  product/platform hints, and source globs without executing Tuist or Swift code.
- [x] `P20-T3` Evaluate `codegraph` as an optional local evidence adapter for
  multi-language source graph extraction, recording analyzer version, source
  digests, trust policy, schema stability, licensing, and performance before any
  default pipeline integration.
- [x] `P20-T4` Extend scoped-source validation with real monorepo smoke fixtures,
  including a Tuist-managed Swift folder, a single-file target, and at least one
  non-Swift folder target.
- [x] `P20-T5` Teach drafting/refinement prompts to distinguish repository,
  package, folder module, and single-file source-unit intent so generated specs
  do not overclaim package-manager ownership when only scoped evidence exists.
- [x] `P20-T6` Implement an explicit opt-in CodeGraph adapter boundary that
  never installs or downloads tools, records analyzer and executable
  provenance, and normalizes JSON or SQLite graph evidence into a
  SpecHarvester-owned `source_graph_index` evidence shape.
- [x] `P20-T7` Add a pinned CodeGraph interface compatibility guard that
  verifies the expected package version, binary availability contract, CLI JSON
  flags, and normalized schema mapping without indexing third-party projects in
  ordinary CI.
- [x] `P20-T8` Clean up stale DocC warnings by making
  `AcceptedPackageUpdateProposals` resolve as a documentation page and by
  replacing literal command references in real-repository quality docs with
  non-symbol code formatting.

Acceptance:

- Scoped folder/file collection never executes repository content, package
  scripts, Tuist, build tools, or network calls.
- Strict public mode still rejects staged changes and missing license evidence,
  but license evidence may be inherited from the owning checkout root.
- Source target metadata is preserved in `harvest.json`, batch output,
  provenance, and generated BoundarySpec evidence.
- Folder targets without package manifests can still produce useful source-unit
  specs from documentation and deterministic public API evidence when supported
  analyzers exist.
- Optional third-party graph tools such as `codegraph` remain explicit adapters
  with untrusted evidence provenance rather than required collector
  dependencies.
- Third-party graph adapter compatibility tests pin external versions and never
  require live network downloads or third-party project runtime execution in
  ordinary CI.
- DocC static generation completes without the stale
  `AcceptedPackageUpdateProposals`, `python -m spec_harvester quality-report`,
  and `specpm validate` warnings.

## Phase 21. Producer Candidate Bundle Contract

- [x] `P21-T1` Align SpecHarvester output planning with the SpecPM Producer
  Candidate Bundle Contract, documenting the required bundle layout,
  `producer-receipt.json` profile, output digest expectations, review boundary,
  and rejection diagnostics once the SpecPM contract PR is merged.
- [x] `P21-T2` Emit `producer-receipt.json` for generated candidate bundles with
  `apiVersion: specpm.receipts/v0`, `kind: SpecPMProducerReceipt`, profile
  `generated_spec_package_v0`, producer identity/version, subject package
  metadata, input evidence references, configuration summary or digest, output
  file roles, output SHA-256 digests, validation status, diagnostics status, and
  `humanReview` status.
- [x] `P21-T3` Emit `validation-report.json` and `diagnostics.json` alongside
  generated `specpm.yaml` and `specs/*.spec.yaml`, making validation result,
  warnings/errors, privacy/security notes, unstable-ID warnings, evidence-link
  gaps, and namespace/version overlap diagnostics machine-readable.
- [x] `P21-T4` Add a local candidate bundle preflight verifier that checks
  required files, receipt schema/profile, output hashes, validation report
  digest, diagnostics digest, stable generated IDs, evidence links, and review
  status before a generated bundle is proposed to SpecPM.
- [x] `P21-T5` Extend the static candidate viewer to show producer receipt,
  input provenance, output hashes, validation status, diagnostics summary,
  privacy/security caveats, and human review boundary without implying automatic
  SpecPM acceptance.
- [x] `P21-T6` Add SpecPM handoff documentation and examples for generated
  candidate bundles, including the distinction between SpecHarvester producing
  an evidence-rich candidate, SpecPM validating package shape, maintainers
  approving acceptance, and the public index publishing only reviewed sources.

Acceptance:

- SpecHarvester treats the SpecPM producer contract as a machine-verifiable
  handoff, not as automatic registry acceptance.
- Generated candidate bundles include `specpm.yaml`, `specs/*.spec.yaml`,
  `producer-receipt.json`, `validation-report.json`, and `diagnostics.json`.
- Receipt hashing avoids a self-hash problem: generated outputs are hashed in
  the receipt, while any receipt hash is handled by an external verifier or PR
  tooling rather than by the receipt itself.
- Public index acceptance remains gated by `humanReview.status == approved` or
  an explicit maintainer override recorded outside the generated bundle.
- Bundle preflight and viewer changes preserve existing SpecPM validation,
  static rendering, and trust-boundary behavior.

## Phase 22. Producer Bundle End-to-End Smoke

- [x] `P22-T1` Add an end-to-end candidate bundle smoke that builds one local
  fixture repository snapshot, drafts a SpecPM candidate bundle, runs producer
  preflight, renders the static viewer, and asserts the receipt, reports,
  preflight result, and viewer payload all agree on the same package identity,
  output hashes, diagnostics status, and review boundary.

Acceptance:

- The smoke uses only local fixture files and trusted SpecHarvester APIs.
- The smoke exercises the real producer path:
  collect -> draft -> preflight -> render.
- The generated bundle passes producer preflight and the rendered static
  payload exposes producer receipt panels for the same candidate.
- The smoke remains producer-side evidence only and does not imply SpecPM
  registry acceptance.

## Phase 23. SpecPM Intake Boundary Alignment

- [x] `P23-T1` Align SpecHarvester-to-SpecPM proposal automation with SpecPM
  producer bundle intake requirements so proposal artifacts and SpecPM pull
  request bodies explicitly include or link `producer-receipt.json`,
  `validation-report.json`, `diagnostics.json`, producer preflight evidence,
  static viewer evidence when available, and the accepted-source diff.
- [x] `P23-T2` Define a shared cross-repository fixture policy so SpecPM
  contract examples and SpecHarvester generated bundle examples cannot silently
  drift.
- [x] `P23-T3` Add SpecHarvester-side support for any future optional SpecPM CI
  preflight gate without making producer evidence registry authority.
- [x] `P23-T4` Integrate a future external registry acceptance decision record
  with SpecHarvester handoff outputs while keeping maintainer decisions outside
  generated receipts.

Acceptance:

- SpecHarvester proposal outputs use the same evidence vocabulary as SpecPM
  producer bundle intake.
- Producer bundle evidence remains review evidence, not automatic SpecPM
  acceptance.
- Remaining SpecPM/SpecHarvester boundary work is visible as explicit follow-up
  policy or implementation tasks.

## Phase 24. Harvested Spec Quality Depth

- [x] `P24-T1` Upgrade generated package specs from safe metadata previews to
  subject-focused preview contracts by enriching deterministic evidence and
  draft output with public interface/index signals, more precise evidence
  `supports` mappings for interfaces and compatibility, and less
  producer-centric summaries.

Motivation:

- The first real `xyflow.core` SpecPM proposal is safe and reviewable, but it is
  mostly an observed public package metadata contract.
- Review found that the generated package correctly avoids overclaiming, yet
  its manifest summary, BoundarySpec scope, interface evidence, and
  compatibility claims are still shallow.
- Downstream consumers need generated specs to describe the target package
  boundary more directly without treating harvested metadata, LM Studio review,
  or producer receipts as registry authority.

Goal:

- Keep generated candidates `preview_only` and maintainer-reviewed, while
  making the generated content more useful as a package contract.
- Use deterministic public evidence first: package manifests, exports, public
  interface indexes, analyzer outputs, and digests.
- Make evidence traceability explicit for `interfaces`, `compatibility`, and
  capability summaries instead of only supporting broad `intent/scope/provides`
  claims.
- Preserve the trust boundary: no package script execution, no dependency
  installation, no runtime behavior claims without evidence, and no direct
  model-authored file mutation.

Acceptance:

- A generated package such as `xyflow.core` can still validate as a SpecPM
  preview package, but its summary and scope describe the target package
  boundary rather than primarily describing the producer process.
- `interfaces.inbound` entries are backed by deterministic evidence such as
  package exports or `public-interface-index.json` records.
- `compatibility.languages` and `compatibility.platforms` are either
  evidence-backed or downgraded to clearly named ecosystem hints.
- BoundarySpec evidence `supports` entries cover capabilities, interfaces, and
  compatibility claims at a useful granularity.
- LM Studio or other model passes may provide bounded review notes, but model
  output remains review evidence only and is not treated as authoritative
  registry content.

## Phase 25. Package Set Monorepo Discovery

- [x] `P25-T1` Align SpecHarvester planning with the SpecPM package-set
  contracts, documenting how `Package Sets`, package relation vocabulary,
  package-set search semantics, registry metadata shape, monorepo discovery
  handoff, multi-package producer intake, and the `xyflow` reference scenario
  map onto SpecHarvester implementation work.
- [x] `P25-T2` Emit a deterministic workspace inventory for monorepos, including
  repository URL, exact revision, workspace manifests, package manifest paths,
  package ecosystem/name/version metadata, source target paths, proposed stable
  SpecPM package IDs, package roles, and privacy-safe evidence references.
- [x] `P25-T3` Draft package-set candidates alongside scoped member package
  candidates so a repository such as `xyflow` can produce `xyflow.workspace`,
  `xyflow.system`, `xyflow.react`, and `xyflow.svelte` without overwriting one
  package subject with another.
- [x] `P25-T4` Emit package relation proposal output for generated package-set
  bundles, starting with `contains` relations from aggregate workspace packages
  to scoped member packages and recording relation evidence as
  producer-observed review material.
- [x] `P25-T5` Extend candidate bundle preflight for bundle sets, checking
  unique package IDs, per-package required files, receipt/report digests,
  relation source/target existence, workspace inventory consistency, privacy
  status, and human review boundary without accepting packages automatically.
- [x] `P25-T6` Extend the static viewer to show package-set previews, member
  package cards, relation proposal badges, result scope examples, and
  producer-observed review status without hiding scoped packages under the
  aggregate package.
- [x] `P25-T7` Add an `xyflow` monorepo smoke fixture or local smoke scenario
  that exercises workspace inventory, package-set candidate generation, scoped
  member package generation, relation proposals, bundle-set preflight, and
  viewer output against the SpecPM reference scenario.

Motivation:

- SpecPM now defines package sets as aggregate discovery entrypoints, not
  inheritance. SpecHarvester needs matching producer behavior so monorepos can
  preserve broad repository intent while keeping scoped package evidence
  precise.
- The previous `xyflow.core` proposal showed that one generated package can
  either overclaim a whole repository or lose useful product-level discovery
  intent when scoped to a single package directory.

Goal:

- Teach SpecHarvester to produce reviewable multi-package candidate bundle sets
  for monorepos while preserving the SpecPM boundary: producer output is
  evidence, SpecPM validates and indexes, and maintainers decide acceptance.

Acceptance:

- Workspace inventory output is deterministic, privacy-safe, and pins the
  repository revision used for discovery.
- Package-set and member package candidates remain independently reviewable and
  validate as SpecPM preview packages.
- Relation proposals use the SpecPM relation vocabulary and remain
  `producer_observed` until maintainer review accepts them.
- Bundle-set preflight verifies integrity and consistency without executing
  harvested repository code, package scripts, build tools, or producer-generated
  prompts.
- Static viewer output makes aggregate and scoped package boundaries clear.
- The `xyflow` scenario can show `xyflow.workspace`, `xyflow.system`,
  `xyflow.react`, and `xyflow.svelte` as separate candidate subjects with
  explicit `contains` relations.

## Phase 26. Package-Set SpecPM Handoff Automation

- [x] `P26-T1` Add a package-set handoff proposal artifact that turns a
  generated package-set bundle into structured SpecPM review evidence with
  member package links, relation proposal links, bundle-set preflight status,
  viewer links, and an external registry acceptance decision boundary.
- [x] `P26-T2` Extend trusted SpecPM proposal automation or dry-run workflow
  inputs so package-set proposal artifacts can be generated and attached
  without granting cross-repository write credentials to untrusted events.
- [x] `P26-T3` Define the SpecPM-side package-set proposal intake checklist and
  evidence roles required before maintainers accept package members or
  relations.
- [x] `P26-T4` Add proposal-only package-set AI enrichment so operators can
  use local OpenAI-compatible providers such as LM Studio to suggest
  evidence-grounded summaries, capabilities, interfaces, confidence, and
  evidence gaps without mutating generated specs or accepting registry
  content.
- [x] `P26-T5` Add a proposal-only LLM package-set draft contract so
  deterministic workspace inventory can feed schema-bound model suggestions for
  selected members, exclusions, and `contains` relations before any generated
  package files are mutated.

Motivation:

- Phase 25 proves SpecHarvester can generate reviewable package-set bundles,
  but operators still need a handoff artifact that explains what should be
  reviewed in SpecPM.
- Package-set proposals include multiple candidate packages and relation
  proposals, so the existing single-package update proposal shape is too narrow.
- SpecPM must remain the validation, acceptance, and registry authority.

Goal:

- Convert generated package-set bundles into deterministic proposal evidence
  that a future SpecPM PR, issue, or CI preflight can consume without treating
  producer output as automatic acceptance.

Acceptance:

- Package-set handoff artifacts identify aggregate and scoped member packages,
  relation proposals, preflight status, viewer output, and registry acceptance
  decision boundary.
- The artifact is reviewable by humans and machine-readable by future SpecPM
  intake tooling.
- Proposal automation stays trusted-context only and does not publish or accept
  packages automatically.
- AI enrichment artifacts remain proposal-only, cite supplied compact evidence
  paths, record provider usage metadata, and emit diagnostics for unsupported
  model evidence paths.
- AI draft artifacts keep the original `LLM + schema` package-set idea explicit:
  inventory is evidence, the model proposes structure, and SpecPM plus
  maintainers remain the acceptance authority.

## Phase 27. Author-Ready Valid Drafts

- [x] `P27-T1` Document the author-ready draft quality bar so generated output
  is treated as a valid starter package for repository authors, not as a final
  accepted specification.
- [x] `P27-T2` Extend quality reporting with an `authorReadyDraft` verdict,
  quality dimensions, and author action items derived from validation reports,
  bundle preflight, AI draft diagnostics, AI enrichment diagnostics, and viewer
  metadata.
- [x] `P27-T3` Add a stop-policy summary to draft, package-set draft, AI draft,
  and AI enrichment flows so model iteration stops when remaining work is
  author-reviewable rather than generator-fixable.
- [x] `P27-T4` Extend the static viewer and handoff Markdown with author review
  checklists, weak claims, evidence gaps, and recommended edits.
- [x] `P27-T5` Run a real-repository author-ready draft calibration matrix and
  record how many author edits are needed to move valid starter packages toward
  curated specs.

Motivation:

- SpecHarvester should return to the original `LLM + schema` idea without
  pretending that model output can author the final package truth.
- Repository authors need a strong, personalized, valid starting package that
  is cheaper to edit than writing a spec from scratch.
- Without an explicit stop policy, generator and model loops will chase a
  misleading 100% target and risk generic wording, overclaims, or framework
  encyclopedia behavior.

Goal:

- Define and implement the product quality boundary for author-ready valid
  drafts: SpecHarvester produces valid, evidence-backed starter packages;
  authors and their agents complete semantic curation; SpecPM validates and
  decides registry acceptance.

Acceptance:

- The author-ready draft quality bar defines valid starter package hard gates,
  author-ready quality dimensions, non-goals, stop policy, and handoff
  expectations.
- Author-ready draft quality reports expose whether a draft is `author_ready_draft`,
  `needs_regeneration`, or `blocked` without treating that verdict as SpecPM
  acceptance.
- Static viewer and handoff outputs make author action items visible.
- Calibration on real repositories measures where generated drafts are useful,
  shallow, or misleading before expanding public self-service workflows.

## Phase 28. SpecPM Refresh Compare Handoff

- [x] `P28-T1` Add a fresh candidate refresh run contract that exports
  generated package-set bundles into the SpecPM
  `prepare-refresh-decision` fresh generated-root layout.
- [x] `P28-T2` Run real `xyflow` through
  `fresh-candidate-refresh-run` and SpecPM `prepare-refresh-decision`, then
  record whether the result is `no_update_required` or
  `manual_review_required`.
- [x] `P28-T3` Repeat the refresh compare loop on a second real repository
  with package-set output to check that the contract is not `xyflow`-specific.
- [x] `P28-T4` Add package-set role selection profiles for generic monorepos
  so operators can request a useful workspace/member package-set without
  ad hoc `--role member_package` knowledge.
- [x] `P28-T5` Define a first-submission or seeded-baseline workflow for
  repositories that do not yet have current SpecPM generated artifacts.

Motivation:

- SpecHarvester can produce package-set bundles and SpecPM can compare fresh
  generated artifacts against current registry evidence, but operators need a
  stable producer artifact between those two sides.
- Without a normalized fresh generated root, every registry refresh evaluation
  becomes manual file shuffling and risks confusing producer evidence with
  SpecPM authority.
- No-op refresh decisions should be evidence-backed and reproducible, not
  informal maintainer judgement.

Goal:

- Make generated package-set refresh evaluation a repeatable cross-repository
  loop: SpecHarvester prepares review evidence and filesystem layout; SpecPM
  compares contract-bearing files and drafts the refresh decision; maintainers
  decide whether anything should enter the registry.

Acceptance:

- `SpecHarvesterFreshCandidateRefreshRun` records source revision, package-set
  members, `<package_id>/<version>` artifact paths, `specpm.yaml` and
  `specs/*.spec.yaml` digests, and SpecPM consumer command metadata.
- The command records `producerEvidenceAuthority: evidence_only` and
  `noRegistryMutation: true`.
- The output can feed SpecPM's
  `specpm producer-bundle prepare-refresh-decision` helper without manual
  package directory reshaping.
- Real-repository follow-up runs decide whether generated candidates contain a
  contract delta before any registry update PR is opened.
- Generic monorepo refresh runs can select workspace/member package-set output
  through a named profile or preset.
- Missing-baseline repositories produce a clear first-submission or
  seeded-baseline handoff instead of a refresh-decision file.

## Phase 29. Autonomous Candidate Harvest MVP

- [x] `P29-T1` Add an autonomous candidate batch runner that takes a repository
  source manifest, collects deterministic evidence from local public checkouts,
  drafts package-set preview bundles, runs producer preflight, and optionally
  invokes a local LM Studio/OpenAI-compatible model for schema-bound AI draft
  and enrichment proposals.
- [x] `P29-T2` Add a SpecPM-facing candidate-layer intake policy for autonomous
  batch output so generated preview packages can be reviewed without implying
  accepted registry authority.
- [x] `P29-T3` Run the autonomous batch runner on a small popular-library set,
  record quality and stop-policy outcomes, and decide which candidates deserve
  curated SpecPM submission work.
- [x] `P29-T4` Add a single-package candidate fallback for repositories such
  as Flask and Gin where deterministic evidence and public interface indexes
  are available but package-set drafting selects no workspace members.
- [x] `P29-T5` Add bounded LM Studio/OpenAI-compatible JSON repair/retry
  for malformed local model output while preserving the no-raw-response
  persistence boundary.
- [x] `P29-T6` Re-run the mixed local corpus after fallback and retry support,
  record whether each repository produces a reviewable preview candidate, and
  decide whether the MVP is ready for larger popular-library scraping.

Motivation:

- The current pipeline can process one real repository well, but autonomous
  popular-library exploration still requires manual command chaining.
- The original product idea is `LLM + schema`: SpecHarvester should create a
  strong, repository-personalized valid starter package while leaving final
  semantic truth to authors, their agents, and SpecPM maintainers.
- Operators need a cost-controlled local model path for repeated scraping runs;
  LM Studio/OpenAI-compatible execution should be the default live enrichment
  surface, while CI remains provider-free.
- The first mixed corpus run exposed two concrete technical-debt items:
  single-package repositories can collect useful evidence while producing zero
  package candidates, and local model output can fail strict JSON parsing under
  real corpus load.

Goal:

- Provide an MVP operator command for autonomous candidate scraping into
  reviewable SpecPM preview artifacts, not automatic registry acceptance.

Acceptance:

- The runner consumes existing repository source manifests and local public
  checkouts; it does not clone repositories, browse the network, execute package
  scripts, install dependencies, or publish SpecPM registry content.
- Each processed repository records collect, workspace inventory, package-set
  draft, bundle-set preflight, optional AI draft, optional AI enrichment, and
  author-ready summary outputs in one machine-readable batch report.
- Live model execution is local and operator-controlled through LM Studio or
  another local OpenAI-compatible provider; raw prompts, raw responses, secrets,
  and chain-of-thought are not persisted.
- Generated package files remain `preview_only` producer evidence until
  explicit SpecPM-side review and acceptance.
- Single-package repositories such as Flask and Gin can produce one reviewable
  preview package candidate instead of only evidence with zero candidates.
- Local LM Studio JSON failures become bounded repair/retry diagnostics rather
  than silent success or lost deterministic artifacts.

## Phase 30. Limited Popular-Library Scraping Batch

- [x] `P30-T1` Define the limited popular-library corpus expansion plan,
  source-manifest shape, selection criteria, operator runbook, and non-authority
  boundaries before running a larger scrape.
- [x] `P30-T2` Run deterministic `--skip-ai` scraping over the selected limited
  popular-library corpus and record collection, candidate, relation, preflight,
  and stop-policy outcomes.
- [x] `P30-T3` Run the same limited corpus through live LM Studio/OpenAI-
  compatible AI draft and enrichment with cost/time caps, repair summaries, and
  bounded diagnostics.
- [x] `P30-T4` Produce a candidate-layer triage report that classifies each
  generated preview package as `candidate_layer_review_required`,
  `needs_regeneration`, `blocked`, or `not_for_intake`.
- [x] `P30-T5` Prepare SpecPM handoff dry-run evidence for selected candidates
  only, preserving `preview_only`, `producer_preview_evidence_only`, and
  external registry acceptance authority.

Motivation:

- P29 established that the autonomous candidate MVP can produce valid starter
  packages for Flask/Gin-style single-package repositories and xyflow-style
  package sets.
- The next risk is operational, not acceptance-related: a larger scrape can
  easily become an unbounded framework encyclopedia or an accidental registry
  intake path unless corpus selection, run limits, and review boundaries are
  explicit.
- Operators need a repeatable limited batch before any broad autonomous
  harvesting is attempted.

Goal:

- Expand from the three-repository quality gate to a small, bounded
  popular-library batch while keeping all output as preview evidence for human
  review.

Acceptance:

- The limited corpus is defined by local public checkouts and pinned revisions;
  the runner does not clone repositories, install dependencies, execute package
  scripts, browse arbitrary network resources, or publish registry metadata.
- The corpus includes a mix of single-package repositories and package-set or
  workspace-style repositories.
- Deterministic and live runs produce machine-readable corpus reports,
  operator-facing summaries, and bounded diagnostics.
- Candidate triage is explicit and does not treat generated output as accepted
  SpecPM registry truth.
- SpecPM handoff dry-run evidence is produced only for selected candidates and
  remains external to registry acceptance.

## Phase 31. Selected Candidate SpecPM Intake Handoff

- [x] `P31-T1` Define a selected candidate handoff proposal contract that turns
  P30-style selected candidate dry-run evidence into portable SpecPM review
  evidence without accepting packages or creating registry authority.
- [x] `P31-T2` Implement a `selected-candidate-handoff-proposal` producer helper
  that reads selected candidate bundles, producer preflight reports, and static
  viewer outputs, then emits JSON and Markdown handoff artifacts.
- [x] `P31-T3` Run the selected candidate handoff proposal helper on the real
  P30 selected candidates and record a dry-run handoff proposal fixture.
- [x] `P31-T4` Define the downstream SpecPM-side preflight expectations for
  `SpecHarvesterSelectedCandidateHandoffProposal` evidence.
- [x] `P31-T5` Record targeted regeneration requirements for deferred P30
  candidates before any package-set, warning-bearing, or identity-drift
  candidate can enter selected handoff.

Motivation:

- P30-T5 proves selected candidates can have digest-backed producer preflight
  and viewer evidence, but that fixture is a recorded dry run rather than a
  portable handoff artifact.
- SpecPM-side intake needs a stable evidence envelope before maintainers can
  review selected single-package candidates without rerunning SpecHarvester.
- Deferred candidates need an explicit regeneration track so the selected
  handoff path does not quietly absorb package-set identity drift or weak
  enrichment output.

Goal:

- Bridge P30 selected candidate evidence into a reviewable SpecPM handoff shape
  while preserving the boundary that SpecHarvester produces evidence and
  SpecPM owns validation, acceptance, registry metadata, and maintainer
  decisions.

Acceptance:

- Selected candidate handoff proposal artifacts identify selected candidates,
  deferred candidates, required evidence roles, producer preflight status,
  static viewer status, privacy/provenance boundaries, and external registry
  acceptance decisions.
- The proposal contract is explicit that passing producer preflight is review
  evidence only and does not accept packages, accept relations, seed baselines,
  remove `preview_only`, publish registry metadata, or create a SpecPM pull
  request.
- SpecHarvester-side docs and examples give SpecPM enough stable roles to build
  future consumer-side preflight without requiring SpecHarvester write
  credentials.

## Phase 32. Autonomous Deferred Candidate Regeneration and Intake Readiness

- [x] `P32-T1` Record the autonomous deferred candidate work plan that
  distinguishes completed P29 debt from current P30/P31 deferred-candidate
  debt, names task owners, and keeps broad autonomous scraping out of scope.
- [x] `P32-T2` Add a deferred candidate regeneration runbook that maps blocker
  classes to safe producer commands, expected artifacts, stop conditions, and
  non-authority boundaries.
- [x] `P32-T3` Run xyflow package-set identity regeneration as a dry run and
  record whether `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, and
  `xyflow.system` can enter selected handoff.
- [x] `P32-T4` Run single-package deferred candidate regeneration or repair for
  `cupertino.core` and `navigation_split_view.core`.
- [x] `P32-T5` Produce refreshed candidate-layer triage and selected handoff
  evidence for regenerated candidates that satisfy hard gates.
- [x] `P32-T6` Add or coordinate the SpecPM-side selected candidate handoff
  preflight for `SpecHarvesterSelectedCandidateHandoffProposal`.
- [x] `P32-T7` Record the limited corpus intake readiness decision after
  refreshed selected handoff evidence passes SpecPM-side preflight or remains
  explicitly deferred.

Motivation:

- P29 closed the first autonomous runner debt, and P30/P31 proved selected
  handoff evidence for three candidates, but six limited-corpus candidates
  remain deferred.
- The project needs a bounded way to regenerate or repair deferred candidates
  before any broader popular-library scraping is attempted.
- The work must keep SpecHarvester as a producer of preview evidence and
  SpecPM as the validation, acceptance, relation, baseline, and registry
  authority.

Goal:

- Turn the P30/P31 deferred-candidate findings into a reviewable sequence that
  can move candidates from `needs_regeneration` to selected handoff only when
  evidence is clean and maintainer review remains external.

Acceptance:

- The plan covers `xyflow.*` package-set identity regeneration,
  `cupertino.core` warning-bearing enrichment or author summary evidence, and
  `navigation_split_view.core` identity-drift resolution.
- Regeneration tasks use local pinned checkouts and do not clone, fetch,
  install dependencies, execute harvested code, publish registry metadata,
  accept packages, accept relations, seed baselines, or remove `preview_only`.
- Refreshed triage uses the existing candidate-layer states:
  `candidate_layer_review_required`, `needs_regeneration`, `blocked`, and
  `not_for_intake`.
- SpecPM-side preflight remains consumer review evidence only and does not make
  producer output authoritative.

## Phase 33. Bounded Corpus Expansion Planning

- [x] `P33-T1` Record the bounded corpus expansion plan in
  [`BOUNDED_CORPUS_EXPANSION_PLAN.md`](../docs/BOUNDED_CORPUS_EXPANSION_PLAN.md),
  defining the next source manifest requirements, five-repository limit,
  validation gate, stop conditions, author/maintainer handoff, and
  non-authority boundary before any broader autonomous scraping continues.
- [x] `P33-T2` Add the next-corpus source manifest fixture in
  [`NEXT_CORPUS_SOURCE_MANIFEST.md`](../docs/NEXT_CORPUS_SOURCE_MANIFEST.md)
  and `inputs/p33-next-corpus/repositories.yml` with pinned local checkout
  requirements, repository selection rationale, and no network discovery
  behavior.
- [x] `P33-T3` Run the next-corpus deterministic collection and draft dry run
  without AI, recording candidate counts, preflight outcomes, blocker classes,
  and the evidence page
  [`NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md`](../docs/NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md).
- [x] `P33-T4` Run the next-corpus live local-model draft/enrichment dry run
  with bounded JSON repair, provider receipts, and the evidence page
  [`NEXT_CORPUS_LIVE_LOCAL_MODEL_BATCH.md`](../docs/NEXT_CORPUS_LIVE_LOCAL_MODEL_BATCH.md).
- [x] `P33-T5` Produce next-corpus candidate-layer triage and selected handoff
  evidence with explicit selected, deferred, blocked, and not-for-intake
  states in
  [`NEXT_CORPUS_CANDIDATE_LAYER_TRIAGE.md`](../docs/NEXT_CORPUS_CANDIDATE_LAYER_TRIAGE.md).
- [x] `P33-T6` Coordinate or run the SpecPM-side preflight for the next-corpus
  selected handoff and record the next intake readiness decision.
- [x] `P33-T7` Create a durable next-corpus selected handoff artifact for
  `serena.core`, `transmission.core`, and `specpm.core`, or explicitly extend
  the SpecPM selected handoff consumer gate, so the selected scope can be
  machine-preflighted before maintainer intake review without fabricating
  per-file evidence digests.
- [x] `P33-T8` Record the next-corpus intake readiness decision using the
  passing durable selected handoff preflight result, preserving review evidence
  boundaries and stopping before registry acceptance, baseline seeding,
  relation acceptance, or `preview_only` removal in
  [`NEXT_CORPUS_INTAKE_READINESS_DECISION.md`](../docs/NEXT_CORPUS_INTAKE_READINESS_DECISION.md).

Motivation:

- Phase 32 intentionally stopped before broader autonomous scraping. The next
  expansion must be bounded, reviewable, and explicit rather than an open-ended
  framework crawl.
- The limited corpus is ready for author/maintainer review, but that does not
  mean SpecHarvester can ingest arbitrary popular repositories without a new
  source manifest, validation gate, and stop policy.

Goal:

- Define the next corpus expansion as a small, operator-selected local checkout
  batch that can produce review evidence without granting registry authority or
  silently expanding scope.

Acceptance:

- The plan defines repository count limits, source manifest requirements,
  validation gates, stop conditions, and non-authority boundaries before any
  new scrape runs.
- Every follow-up task remains local-only: no clone/fetch, no dependency
  install, no harvested code execution, no registry publication, no package or
  relation acceptance, and no `preview_only` removal.
- The next-corpus result must stop at author/maintainer review evidence unless
  a separate SpecPM maintainer acceptance flow is explicitly opened.

## Phase 34. AI-Enabled Candidate Curation

- [x] `P34-T1` Add an AI enrichment candidate patch proposal helper that turns
  a clean `SpecHarvesterPackageSetAIEnrichmentProposal` into a reviewable
  enriched candidate copy plus machine-readable patch report without accepting
  packages, mutating the source bundle, removing `preview_only`, or treating
  model output as registry truth.

Motivation:

- Live LM Studio/OpenAI-compatible enrichment already produces better
  repository-specific summaries and capabilities than deterministic drafting
  for repositories such as FastAPI.
- Today those improvements remain proposal JSON beside the generated bundle.
  Operators need a safe, deterministic handoff step that applies clean model
  proposals into a separate review candidate so AI-enabled usage becomes the
  normal review path.

Goal:

- Make AI enrichment practically useful by producing a reviewable enriched
  candidate artifact while preserving SpecHarvester as producer evidence and
  SpecPM as the validation, acceptance, and registry authority.

Acceptance:

- The helper reads a package-set AI enrichment proposal and a generated
  candidate bundle, rejects failed/warning proposals by default, and writes an
  enriched candidate copy plus patch report under an explicit output root.
- Applied changes are limited to reviewable summary/capability/interface
  enrichment from supported evidence paths.
- The source candidate bundle is not mutated, `preview_only` remains true,
  model output remains proposal evidence, and no SpecPM acceptance or registry
  publication is implied.
- CLI, docs, DocC, tests, and Flow archive record the boundary and the FastAPI
  comparison motivation.

- [x] `P34-T2` Add an optional autonomous batch output mode that applies clean
  AI enrichment proposals into enriched preview candidate copies and emits patch
  reports alongside the normal proposal-only artifacts without accepting
  packages, mutating source candidates, or publishing registry metadata.

Motivation:

- P34-T1 makes AI enrichment useful through an explicit operator command, but
  autonomous corpus runs still stop at sidecar proposal JSON unless the helper
  is invoked manually for each candidate.
- AI-enabled usage should become the practical review path when local
  LM Studio/OpenAI-compatible enrichment succeeds cleanly.

Goal:

- Let autonomous batch runs optionally emit author-reviewable enriched preview
  candidates for clean AI proposals while preserving deterministic validation,
  preview-only status, and non-authority boundaries.

Acceptance:

- The autonomous batch path exposes an explicit opt-in option for enriched
  preview output and keeps the default proposal-only behavior unchanged.
- Clean completed enrichment proposals produce copied enriched candidates plus
  `ai-enrichment-candidate-patch.json` reports; failed, warning-bearing, or
  diagnostic-bearing proposals remain sidecar-only and require regeneration or
  review.
- The output preserves `preview_only`, refreshes producer receipt digests,
  passes producer preflight where possible, and records summary counts in the
  batch report.
- Docs, DocC, tests, and a practical smoke show that AI-enabled autonomous
  runs can produce reviewable enriched candidates without implying SpecPM
  acceptance or registry publication.

## Phase 35. Curated Multi-Ecosystem Corpus Selection

- [x] `P35-T1` Document the corpus selection policy that prevents autonomous
  harvesting from becoming an open-ended crawl across every popular registry
  package. The policy must define importance signals, exclusion rules,
  ecosystem quotas, local checkout requirements, and the review boundary for
  selected sources.
- [x] `P35-T2` Define a machine-readable `SpecHarvesterCorpusPlan` format for
  curated source batches, including ecosystem, repository, package-family,
  category, selected-because reason codes, excluded-subpackage reason codes,
  source checkout pins, and non-authority statements.
- [x] `P35-T3` Add a candidate source classifier plan for distinguishing
  primary packages, package-set roots, plugins, examples, tooling, type-only
  packages, generated artifacts, internal utilities, and deprecated sources
  before drafting.
- [x] `P35-T4` Create the first multi-ecosystem seed corpus plan with a small
  bounded set of important repositories across JavaScript/TypeScript, Python,
  Rust, Go, and at least one additional ecosystem, without cloning, fetching,
  installing dependencies, executing harvested code, or publishing registry
  metadata.
- [x] `P35-T5` Add an explainable corpus selection report that records selected
  sources, rejected or deferred sources, importance signals, exclusion reasons,
  quota decisions, and the downstream autonomous-batch command plan.
- [x] `P35-T6` Run or document a dry-run readiness check for the selected
  corpus plan, proving that each selected repository has a pinned local
  checkout, a clear package-family target, expected ecosystem analyzer
  coverage, and an explicit stop condition before author/maintainer review.

Motivation:

- npm and other registry popularity searches return ecosystem plumbing,
  internal utilities, type packages, generated artifacts, and unrelated
  high-download packages alongside the libraries authors actually care about.
- SpecHarvester needs to support autonomous exploration of important
  libraries across ecosystems without turning into a crawler that collects
  every possible framework, shim, parser, or internal package.
- AI-enabled candidate generation is most useful when the source corpus is
  curated, bounded, explainable, and reviewable before any harvesting run.

Goal:

- Establish a bounded, multi-ecosystem corpus selection layer that chooses
  important repository/package-family targets for author-ready draft generation
  while keeping SpecHarvester local-first and SpecPM as the acceptance and
  registry authority.

Acceptance:

- The phase defines what makes a library important using multiple signals:
  dependency centrality, registry usage, public API richness, ecosystem
  archetype coverage, release/maintenance health, source availability,
  security/supply-chain relevance, and review value.
- The phase defines exclusion and deferral rules for internal utilities,
  types-only packages, generated-only packages, deprecated sources, examples,
  test fixtures, build tooling, and registry search noise.
- The corpus plan remains operator-selected and bounded by ecosystem quotas;
  it must not clone/fetch repositories, install harvested dependencies,
  execute harvested code, publish registry metadata, accept packages, accept
  relations, remove `preview_only`, or treat AI output as registry truth.
- Every selected source must explain why it was selected, which package-family
  or repository root it represents, which subpackages are excluded, and what
  evidence is required before running autonomous candidate generation.

## Phase 36. Repository Parsing Plugin System

- [x] `P36-T1` Document the repository parsing plugin contract, using the
  FastAPI `docs_src` over-capture as the first motivating case. The contract
  must distinguish public API evidence from semantic usage/documentation
  evidence and define how language/framework-specific rules can classify
  source roots, package roots, examples, docs, tests, generated files, and
  tooling without hardcoding every repository in the core analyzer.
- [x] `P36-T2` Add a machine-readable parser rule profile fixture for Python
  web frameworks that treats FastAPI package code as public interface evidence
  while treating `docs_src`, tutorials, examples, and tests as semantic usage
  evidence unless explicitly promoted by a plugin rule.
- [x] `P36-T3` Implement the first plugin-aware source classification hook in
  the collection/analyzer path, keeping default behavior backwards-compatible
  and requiring explicit opt-in for technology-specific rule profiles.
- [x] `P36-T4` Re-run the FastAPI AI-enabled candidate batch with the Python
  web-framework parser profile, compare evidence volume and claim quality
  against the P35/P34 FastAPI run, and record whether the output is closer to
  registry-review quality.

Motivation:

- The FastAPI rerun now produces a valid `author_ready_draft`, but the Python
  analyzer treats documentation tutorial files such as `docs_src/*` as public
  interface evidence. Those files are useful for intent and usage semantics,
  but they should not inflate the public API boundary.
- Repository structure differs by language, framework, and ecosystem. A
  single hardcoded analyzer rule will either underfit real repositories or
  become a pile of one-off exceptions.
- SpecHarvester needs a bounded extension point where repository parsing rules
  can evolve per technology without turning autonomous harvesting into a
  global, unreviewable crawler.

Goal:

- Introduce a plugin-shaped parsing policy layer that can classify repository
  paths by evidence role before candidate drafting: public interface evidence,
  semantic usage evidence, docs, examples, tests, generated artifacts, tooling,
  internal implementation, or ignored paths.

Acceptance:

- The phase defines a stable plugin contract before implementation: inputs,
  outputs, rule precedence, default fallback behavior, safety boundaries, and
  review evidence emitted by plugin decisions.
- The FastAPI case is represented as a general Python web-framework profile,
  not a repository-specific special case.
- Documentation and tutorial sources remain available to LLM/semantic
  enrichment as usage evidence, while public API indexes focus on package
  surfaces intended for consumers.
- Plugin decisions remain producer-side evidence only: they do not publish
  registry metadata, accept packages or relations, remove `preview_only`, or
  treat AI output as registry truth.

## Phase 37. Repository Profile Plugin Selection

- [x] `P37-T1` Document a language- and framework-agnostic repository profile
  selection contract. The contract must define profile detection inputs,
  candidate scoring, selection modes, conflict behavior, operator overrides,
  and a replayable decision artifact without naming any language or framework
  as normative.
- [x] `P37-T2` Add a machine-readable `SpecHarvesterRepositoryProfileDetection`
  fixture format that records detected candidate profiles, confidence,
  evidence paths, rejected profiles, selected profile, fallback profile,
  override source, diagnostics, and non-authority statements.
- [x] `P37-T3` Implement an opt-in repository profile detection CLI/report
  surface that reads only static repository evidence and emits the detection
  artifact without collecting source files, installing dependencies, executing
  harvested code, invoking AI, or drafting packages.
- [x] `P37-T4` Connect repository profile selection to autonomous candidate
  batch as an explicit `auto | none | <profile-id>` decision layer, preserving
  backwards-compatible generic behavior when confidence is low, ambiguous, or
  disabled.
- [x] `P37-T5` Define generic workspace/member discovery hints produced by
  profiles: package-set root, member packages, meta packages, primary
  packages, CLI/bridge packages, plugin packages, examples, tests, docs,
  generated artifacts, internal utilities, and evidence-only sources.
- [x] `P37-T6` Add cross-ecosystem profile fixtures that prove the selection
  contract is not Python-specific: one workspace-shaped fixture, one
  single-package fixture, one nested-package fixture, and one ambiguous
  multi-signal fixture.
- [x] `P37-T7` Re-run a real repository with profile auto-selection and record
  a quality comparison against manual targeting. FastMCP may be used as the
  motivating validation case, but the report must evaluate the generic
  subsystem: detection evidence, selected profile, confidence, overrides,
  public-interface precision, topology hints, and author-ready output quality.
- [x] `P37-T8` Make repository profile detection consume harvested package
  manifest evidence when workspace inventory has no manifest records. The
  FastMCP real run showed `harvest.json` can see a root package manifest while
  `workspace-inventory.json` reports no manifests, causing auto-selection to
  fall back despite available static evidence.

Motivation:

- The FastMCP dry run showed that an explicit target can produce a better
  starter package than a generic repository-wide run, but the operator should
  not have to hand-author targets for every repository shape.
- Plugin selection must be explainable and reviewable. A hidden heuristic that
  silently decides between workspace, single-package, nested-package, or
  framework profiles would make generated packages hard to audit.
- Repository layout is ecosystem-specific, but the selection subsystem should
  remain ecosystem-neutral: language/framework plugins may provide evidence,
  while the core policy chooses, records, and exposes the decision.

Goal:

- Introduce a repository profile selection layer that chooses or rejects
  candidate plugins from static evidence, records why a profile was selected,
  and keeps profile choice as producer-side evidence rather than registry
  authority.

Acceptance:

- The phase defines `detect candidates -> score evidence -> select or
  fallback -> record decision` as the common shape for all repository profile
  plugins.
- Explicit CLI and manifest overrides take precedence over auto-detection;
  auto-detection only selects a profile when confidence is high and conflicts
  are absent.
- Ambiguous, low-confidence, missing, or conflicting profile signals fall back
  to generic behavior with diagnostics instead of silently selecting a
  technology-specific profile.
- Detection reads static repository evidence only: manifests, lock/workspace
  files, package metadata, directory layout, and allowlisted metadata files.
- The subsystem does not clone/fetch repositories, install dependencies,
  execute harvested code, invoke package managers, run AI, publish registry
  metadata, accept packages or relations, remove `preview_only`, or treat AI
  output as registry truth.
- Real-repository validation may use FastMCP, FastAPI, or another local
  checkout, but the phase output must describe reusable plugin selection
  behavior rather than repository-specific special cases.

## Phase 38. Repository Plugin Subsystem

- [x] `P38-T1` Document a language- and framework-agnostic repository plugin
  subsystem contract. The contract must define plugin registration, static
  evidence producers, applicability checks, deterministic selection boundaries,
  declared capabilities, authority limits, diagnostics, and non-goals without
  making Python, JavaScript, FastAPI, FastMCP, npm, Cargo, Go, SwiftPM, Maven,
  Gradle, or any other ecosystem normative.
- [x] `P38-T2` Add a machine-readable repository plugin registry fixture that
  records plugin ids, versioned contracts, provided evidence kinds, input
  requirements, safety constraints, applicability signals, and declared output
  artifacts.
- [x] `P38-T3` Add a plugin applicability report fixture that evaluates several
  generic plugins against static repository evidence and records selected,
  rejected, fallback, and blocked decisions without running plugin code.
- [x] `P38-T4` Connect plugin registry and applicability output to autonomous
  candidate batch as sidecar producer evidence, preserving existing parser and
  repository profile behavior unless a high-confidence plugin decision is
  explicitly selected.
- [x] `P38-T5` Add cross-ecosystem plugin subsystem fixtures that cover
  manifest-backed single packages, workspaces, documentation-heavy
  repositories, nested package roots, and ambiguous mixed layouts.
- [x] `P38-T6` Run one real repository through the plugin subsystem evidence
  path and compare it with the current Phase 37 profile selection behavior.

Motivation:

- Phase 36 introduced parser profile hooks, and Phase 37 introduced repository
  profile selection. The next layer should unify these ideas into a broader
  plugin subsystem instead of growing one-off profile mechanisms.
- The subsystem must let future language/framework plugins provide static
  evidence and applicability signals while the core pipeline remains
  deterministic, auditable, and ecosystem-neutral.
- Plugins must be explicit review evidence. They must not become hidden
  heuristics that silently decide package claims, registry acceptance, or
  public metadata.

Goal:

- Define a repository plugin subsystem that can register plugins, evaluate
  applicability from static evidence, record diagnostics, and expose
  deterministic producer-side decisions before analyzer path selection,
  package-set drafting, AI proposals, or SpecPM handoff.

Acceptance:

- The phase keeps plugin contracts language- and framework-agnostic.
- Plugin selection reads static local evidence only and never executes
  harvested code, package managers, dependency installation, network calls, or
  AI.
- Plugin output remains producer-side evidence and does not accept packages,
  accept relations, publish registry metadata, remove `preview_only`, or treat
  plugin decisions as registry truth.
- Parser profiles and repository profiles can be represented as plugin roles
  without rewriting existing behavior in the initial contract task.

## Phase 39. Static Repository Plugin Applicability Evaluator

- [x] `P39-T1` Document the static repository plugin applicability evaluator
  plan. The plan must describe how SpecHarvester can turn the P38 registry,
  collected evidence, repository profile detection, workspace inventory,
  harvest snapshots, and operator labels into a deterministic
  `SpecHarvesterRepositoryPluginApplicabilityReport` without loading or
  executing plugin code.
- [x] `P39-T2` Add a machine-readable static plugin evidence envelope fixture
  that enumerates available evidence kinds, paths, digests, source identity,
  and authority boundaries before applicability evaluation.
- [x] `P39-T3` Implement a deterministic static applicability evaluator helper
  that reads the plugin registry plus evidence envelope and emits selected,
  rejected, fallback, and blocked plugin decisions.
- [x] `P39-T4` Add a `repository-plugin-applicability-detect` CLI/report
  surface for the static evaluator, including JSON output and regression
  tests.
- [x] `P39-T5` Integrate static evaluator output into
  `autonomous-candidate-batch` as an opt-in auto sidecar path while preserving
  explicit sidecar input behavior and keeping `appliedToDrafting: false`.
- [x] `P39-T6` Run a real multi-repository static evaluator validation over
  existing local checkouts, comparing FastMCP, FastAPI, and xyflow style
  repository shapes without cloning, installing dependencies, running package
  managers, executing harvested code, or invoking AI.

Motivation:

- Phase 38 proved the plugin applicability contract with fixtures and one real
  sidecar run. The next layer should remove hand-authored applicability
  sidecars by deriving them deterministically from collected static evidence.
- The evaluator should answer "which plugin role applies here?" from declared
  registry inputs and evidence availability, not from hidden ecosystem
  heuristics or executable plugin code.

Goal:

- Provide a deterministic, auditable static evaluator that produces
  `SpecHarvesterRepositoryPluginApplicabilityReport` artifacts from existing
  producer evidence and can later support runtime adapters without weakening
  trust boundaries.

Acceptance:

- Evaluation reads declared plugin metadata and collected static evidence only.
- Missing required input evidence produces `blocked`, `fallback`, or
  `rejected` decisions instead of silent selection.
- The evaluator never loads third-party plugin code, executes plugins, clones
  repositories, installs dependencies, invokes package managers, executes
  harvested code, runs AI, accepts packages or relations, publishes registry
  metadata, removes `preview_only`, or treats plugin decisions as registry
  truth.
- The existing explicit sidecar path remains valid and takes precedence over
  auto-generated applicability evidence when an operator supplies one.

## Phase 40. Repository Plugin Adapter Contract

- [x] `P40-T1` Document a language- and framework-agnostic repository plugin
  adapter contract. The contract must define adapter identity, versioned
  manifests, declared input evidence, output artifacts, execution modes,
  sandbox expectations, diagnostics, and authority boundaries without making
  Python, JavaScript, FastAPI, FastMCP, npm, Cargo, Go, SwiftPM, Maven,
  Gradle, or any other ecosystem normative.
- [x] `P40-T2` Add a machine-readable
  `SpecHarvesterRepositoryPluginAdapterManifest` fixture that records adapter
  ids, contract versions, supported roles, required and optional evidence
  kinds, declared outputs, execution mode, sandbox requirements, capability
  requests, and non-authority statements.
- [x] `P40-T3` Add a repository plugin adapter preflight report fixture that
  validates one or more adapter manifests against a static evidence envelope,
  records allowed, rejected, fallback, and blocked adapter decisions, and
  refuses unsafe execution or missing required evidence before any adapter code
  can run.
- [x] `P40-T4` Define adapter execution policy for future local adapters:
  default disabled execution, static-only mode, bounded local trusted mode,
  path allowlists, no dependency installation, no package manager invocation,
  no network discovery, no harvested code execution, and explicit operator
  opt-in for every non-static mode.
- [x] `P40-T5` Connect adapter manifest and preflight output to
  `autonomous-candidate-batch` as review-only producer evidence while keeping
  the existing static evaluator path unchanged unless an operator explicitly
  supplies adapter evidence.
- [x] `P40-T6` Record a cross-ecosystem adapter contract fixture matrix for
  manifest-backed single packages, workspaces, documentation-heavy
  repositories, nested package roots, and ambiguous mixed layouts without
  loading third-party adapter code.
- [x] `P40-T7` Run a real local adapter-contract validation over existing
  pinned checkouts, comparing FastMCP, FastAPI, xyflow, and at least one
  additional ecosystem shape when available, while proving that adapters remain
  producer-side evidence only.

Motivation:

- Phase 39 can now derive plugin applicability reports from static evidence,
  but the next layer needs a contract for future adapter implementations
  before any plugin runtime exists.
- The adapter layer must let ecosystem-specific analyzers declare what they
  need and what they emit without letting those analyzers silently decide
  package claims, relation acceptance, registry publication, or public
  metadata.
- Planning the adapter boundary before implementation keeps broad popular
  library scraping bounded: plugin precision can improve evidence quality
  without turning SpecHarvester into a crawler that collects every framework
  signal in the world.

Goal:

- Define the repository plugin adapter boundary that future language,
  framework, package-manager, documentation, or public-interface analyzers must
  satisfy before they can participate in the candidate pipeline.

Acceptance:

- The phase keeps adapter contracts language- and framework-agnostic.
- Static applicability evaluation remains the default safe path; adapter
  execution is disabled unless a future task adds explicit operator-controlled
  execution policy.
- Adapter manifests and preflight reports are machine-readable producer
  evidence and never accept packages, accept relations, seed baselines, remove
  `preview_only`, publish registry metadata, or treat adapter output as
  registry truth.
- Adapter inputs must be declared evidence artifacts with safe relative paths,
  digests, and authority labels.
- Unsafe modes such as dependency installation, package manager invocation,
  network discovery, harvested code execution, and unbounded local tool
  execution are rejected or blocked by default.

## Phase 41. Trusted Local Adapter Runtime Readiness

- [x] `P41-T1` Document the trusted local adapter runtime readiness plan and
  add the next-task scaffold for turning Phase 40 adapter contracts into a
  future opt-in runtime without enabling adapter execution yet.
- [x] `P41-T2` Add a machine-readable
  `SpecHarvesterTrustedLocalAdapterRunRequest` fixture that records operator
  opt-in, adapter manifest/preflight references, declared input artifacts,
  safe relative read path allowlists, output directory policy, resource
  budgets, environment policy, network policy, dependency policy, package
  manager policy, and non-authority statements.
- [x] `P41-T3` Add a trusted local adapter run preflight report fixture that
  validates run requests before execution and rejects unsafe paths, missing
  digests, missing operator opt-in, network access, dependency installation,
  package manager invocation, harvested code execution, unbounded process
  execution, and undeclared outputs.
- [x] `P41-T4` Implement a disabled-by-default trusted local adapter runner
  skeleton that can validate a request and emit a no-execution report without
  loading third-party adapter code or running adapter processes.
- [x] `P41-T5` Connect trusted local adapter run reports to
  `autonomous-candidate-batch` as explicit review-only producer evidence while
  preserving the default static evaluator and existing adapter sidecar paths.
- [x] `P41-T6` Run a real local trusted-adapter readiness validation over
  existing pinned checkouts, comparing FastMCP, FastAPI, xyflow, and Gin while
  proving no adapter process, package manager, dependency installer, network
  discovery, harvested code, or AI execution occurred.

Motivation:

- Phase 40 defines adapter manifests, preflight evidence, disabled execution
  policy, batch evidence handoff, fixture matrix coverage, and real local
  validation. The next layer should prepare for a future trusted local adapter
  runtime without weakening those boundaries.
- The runtime readiness phase must specify operator opt-in, path allowlists,
  resource budgets, environment restrictions, output digest requirements, and
  review-only authority before any adapter process can be launched.
- This keeps ecosystem-specific plugin precision possible while preventing
  hidden adapter execution from becoming a source of package claims, relation
  acceptance, registry publication, or `preview_only` removal.

Goal:

- Prepare the contract, request, preflight, no-execution skeleton, and evidence
  handoff needed for future trusted local adapter execution while keeping the
  initial implementation disabled-by-default and non-authoritative.

Acceptance:

- Trusted local adapter work remains language- and framework-agnostic.
- No task may enable default adapter execution.
- Every request must require explicit operator opt-in and safe relative path
  allowlists before any future process launch.
- Missing digests, unsafe paths, network access, dependency installation,
  package manager invocation, harvested code execution, AI execution, and
  unbounded local tools are rejected or blocked before execution.
- Adapter runtime artifacts remain producer-side review evidence and never
  accept packages, accept relations, seed baselines, publish registry metadata,
  remove `preview_only`, or treat adapter output as registry truth.

## Phase 42. Trusted Local Adapter Runtime Sandbox

- [x] `P42-T1` Document the trusted local adapter runtime sandbox plan and add
  the next-task scaffold for turning Phase 41 no-execution readiness into a
  future explicitly approved sandboxed adapter runtime without enabling adapter
  execution yet.
- [x] `P42-T2` Add a machine-readable
  `SpecHarvesterTrustedLocalAdapterSandboxContract` fixture that records
  adapter package identity, sandbox policy identity, operator approval
  requirements, filesystem/environment/network/dependency policy, output
  verification, audit records, and non-authority statements before any runtime
  implementation.
- [x] `P42-T3` Add a trusted local adapter sandbox preflight report fixture that
  validates `SpecHarvesterTrustedLocalAdapterSandboxContract` identity,
  operator approval requirements, process/filesystem/environment/dependency/
  network policy, output verification, audit requirements, and non-authority
  boundaries before any sandbox runner implementation.
- [x] `P42-T4` Add disabled trusted local adapter sandbox runner validation that
  checks sandbox contract and sandbox preflight report linkage while preserving
  no adapter code loading, no process spawning, no dependency installation, no
  network access, and no registry authority.
- [x] `P42-T5` Add an explicitly approved synthetic trusted local adapter
  sandbox run fixture that records operator approval binding, sandbox runner
  validation input, synthetic adapter output candidates, output digests, audit
  records, and non-authority statements without running a real adapter process.
- [x] `P42-T6` Add a synthetic trusted local adapter sandbox run verifier that
  checks P42-T5 fixture identity, linked artifact digests, approval binding,
  synthetic output byte sizes/digests, audit requirements, and no-real-execution
  boundaries without enabling real adapter execution.
- [x] `P42-T7` Add a real local trusted adapter sandbox run readiness gate that
  checks the P42-T6 verifier report plus explicit real-run prerequisites,
  sandbox runtime availability, filesystem/output policy, audit requirements,
  and operator approval requirements while still refusing to load adapter code
  or spawn adapter processes.
- [x] `P42-T8` Add an explicit real local trusted adapter sandbox run request
  fixture that records a future real-run review request, scoped operator
  approval requirements, verifier/readiness references, runtime policy,
  filesystem/output/audit declarations, and non-authority statements while
  still refusing to load adapter code or spawn adapter processes.
- [ ] `P42-T9` Add an explicit real local trusted adapter sandbox run request
  preflight fixture that validates the P42-T8 request identity, prerequisite
  verifier/readiness evidence requirements, scoped approval binding, runtime
  policy, filesystem/output/audit declarations, and non-authority statements
  while still refusing to grant execution permission or spawn adapter
  processes.

Motivation:

- Phase 41 proves the request, preflight, disabled runner report, batch handoff,
  and real local readiness validation path. The next layer must define the
  sandbox contract before any adapter process can run.
- Real adapter execution needs more than operator opt-in: process isolation,
  adapter package identity, dependency isolation, environment sealing,
  filesystem allowlists, output verification, and replayable approval must be
  documented first.
- Planning the sandbox boundary keeps future ecosystem-specific adapters useful
  for quality without turning SpecHarvester into an unbounded local execution
  engine.

Goal:

- Define the language- and framework-agnostic sandbox/runtime boundary that
  future trusted local adapter execution must satisfy before implementation.

Acceptance:

- The phase starts with documentation and machine-readable planning only.
- Synthetic approved runs remain fixtures until the sandbox runner implementation
  and real adapter execution gates are reviewed separately.
- Synthetic approved run verification remains a producer-side review gate and
  must not execute adapters.
- No task may enable adapter execution by default.
- Any future runtime must require explicit operator approval, bounded process
  execution, safe input allowlists, sealed environment, dependency isolation,
  network-deny-by-default policy, output digests, and review-only authority.
- Runtime outputs remain producer-side evidence and never accept packages,
  accept relations, seed baselines, publish registry metadata, remove
  `preview_only`, or treat adapter output as registry truth.
