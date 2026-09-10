# T6 bounded reference notes

AI assistance only. No human scores, verdicts, or timing measurements. Commands below are quoted reference instructions, not executed actions.

Paths below are relative to the P56-T5 comparison bundle unless identified as upstream references. Read only the five frozen README files, five named principal specs, and five `semantic.json` records. No new candidates, source checkouts, linked evidence files, or principal manifests were inspected. No project execution, network, git, or PR actions were performed.

Old-package inspection is limited to the named principal members below. The full retained sets of **4/1/1/1/77** packages, respectively, were **not exhaustively reviewed**. Missing means absent from the inspected surface, not necessarily absent from the project or other retained members.

## README surfaces

### Codex: `openai-codex/README.md`

1. **Purpose/consumer?** Local coding agent for developers; introductory text distinguishes CLI, IDE, desktop, and cloud experiences.
2. **Getting started?** `Quickstart`: install with `npm install -g @openai/codex` or Homebrew/standalone installer; run `codex`, select ChatGPT sign-in. API-key setup is linked, not supplied inline.
3. **Operations/config?** Installer source fallback is documented; `CODEX_INSTALLER_USE_RELEASES_OPENAI_COM=false` forces GitHub Releases. `codex app` opens the desktop experience. Runtime configuration, approval, and sandbox settings are missing inline.
4. **Limits/prerequisites/effects?** Platform-specific installation and binary architecture choices are given, alongside account-plan guidance and Apache-2.0 licensing. Installers download software. Runtime permission boundaries and coding-operation effects are not described.
5. **Evidence?** Installation examples and upstream references `docs/install.md`, `docs/contributing.md`, `LICENSE`; external documentation/auth links. No embedded runtime test results; linked material was not read.

### Bitcoin: `bitcoin-bitcoin/README.md`

1. **Purpose/consumer?** `What is Bitcoin Core?`: software connects to the peer network and fully validates downloaded blocks/transactions; optional wallet and GUI. Also addresses contributors.
2. **Getting started?** Links ready-to-use binaries and upstream `doc/build-*.md`. Actual node startup, first synchronization, and wallet setup commands are missing.
3. **Operations/config?** Development and testing workflows are described, including `ctest` and `build/test/functional/test_runner.py`. Node configuration, RPC setup, backup, and recovery procedures are missing.
4. **Limits/prerequisites/effects?** `master` is not guaranteed stable; release tags identify stable versions. Tests require enabled build support/dependencies. Network downloading is explicit; storage requirements are missing. Security-critical monetary risk and MIT licensing are stated.
5. **Evidence?** Upstream `src/test/README.md`, `/test`, `doc/developer-notes.md`; README describes Windows/Linux/macOS CI and independent manual QA. These are process references, not inspected passing results.

### RTK: `rtk-ai-rtk/README.md`

1. **Purpose/consumer?** `What RTK Does`: CLI proxy compresses shell output consumed by AI coding agents through filtering, grouping, truncation, and deduplication.
2. **Getting started?** `brew install rtk`; check `rtk --version` and `rtk gain`; select an integration with `rtk init`, restart the agent. Cargo installation warns about the unrelated crates.io namesake.
3. **Operations/config?** `Configuration`: TOML `hooks.exclude_commands`, `tee.enabled`, `tee.mode`; `rtk gain` analytics and `rtk proxy` raw passthrough. Config location differs on macOS. Telemetry controls include `RTK_TELEMETRY_DISABLED=1`.
4. **Limits/prerequisites/effects?** Bash hooks bypass built-in Read/Grep/Glob; Codex uses instruction files, not the same interception mechanism. Some filters need `rg`. Init changes integration files; tee persists raw failure output. Telemetry requires opt-in. Savings concern output, not total bills; token counts approximate bytes/4.
5. **Evidence?** Before/after examples, configuration snippets, upstream `docs/TELEMETRY.md`, `INSTALL.md`, architecture/security links. No independently verified performance results. Verification example says 0.28.2 while Windows text references 0.37.2; the README alone does not resolve this mismatch.

### Axios: `axios-axios/README.md`

1. **Purpose/consumer?** Promise-based HTTP client for JavaScript consumers in browsers and Node.js (`Features`).
2. **Getting started?** `Installing` and `Example`: `npm install axios`, `import axios from 'axios'`, then `axios.get(...)` or `axios.post(...)` with response/error handling.
3. **Operations/config?** `Request config`, `Config defaults`, `Interceptors`: configure `baseURL`, headers, params, timeout, adapters, proxies, cancellation, and response validation. Request config overrides instance and library defaults; request bodies are not inherited.
4. **Limits/prerequisites/effects?** Requests transmit data; global authorization defaults can reach multiple domains. Timeout defaults to zero; body/content limits are unlimited unless configured. README warns `baseURL` is not a security boundary. ES6 Promises are required; HTTP/2 and progress support have adapter/runtime limits.
5. **Evidence?** Detailed examples, response/error schemas, upstream `test/specs/interceptors.spec.js`, `THREATMODEL.md`, CI/browser-matrix links. Exact minimum supported Node version and live test outcomes are not established here.

### n8n: `n8n-io-n8n/README.md`

1. **Purpose/consumer?** Platform for building AI agents and workflows with a visual canvas and code; self-hosted or cloud, with integrations and templates.
2. **Getting started?** `Quick Start`: `npx n8n` requires Node.js. Docker example creates `n8n_data`, publishes port 5678, mounts `/home/node/.n8n`; editor is at localhost:5678.
3. **Operations/config?** Basic Docker persistence and access are shown. Production configuration, credentials, backups, scaling, and upgrade procedures are missing inline; documentation is linked.
4. **Limits/prerequisites/effects?** Node.js or Docker is needed; minimum versions are missing. Docker publishes a port and persists data. Sustainable Use and Enterprise licenses are identified; detailed restrictions and feature entitlements are not included.
5. **Evidence?** Quick-start snippets, capability list, screenshot, documentation/integration/workflow links, and upstream `CONTRIBUTING.md`. No embedded test results or demonstrated production-security guarantees.

## Retained principal YAML surfaces

Common to all five: `metadata.status: draft`; `constraints` require review and prohibit harvester execution. `scope.excludes` rejects unsupported runtime claims, endorsement, and automatic registry acceptance. Empty `requires.capabilities` and `effects.sideEffects` do **not** establish dependency-free or effect-free software. `provenance.sourceConfidence.behavior: low`; repository/revision/target and nonexecuting harvest policy are recorded. `evidence[id=harvest_snapshot]` points to `harvest.json`, not inspected here. Its `supports` lists `compatibility`, but these specs have no corresponding top-level field.

### Codex

`openai-codex/retained-files/openai_codex.codex/specs/codex_cli.spec.yaml`

1. **Purpose/consumer?** `intent.summary` identifies the local coding agent; capability classification is `intent.package.javascript_library`.
2. **Getting started?** `interfaces.inbound[id=package.codex]` names `@openai/codex`; installation, CLI invocation, and authentication are missing.
3. **Operations/config?** No commands, runtime settings, or operational procedures declared.
4. **Limits/prerequisites/effects?** Target is `codex-cli`, not the entire repository; common harvest limits apply. Actual runtime prerequisites/effects are unspecified.
5. **Evidence?** Common `harvest_snapshot` supports intent, capability, and library interface; no behavioral test evidence.

### Bitcoin

`bitcoin-bitcoin/retained-files/bitcoin_bitcoin.core/specs/bitcoin.spec.yaml`

1. **Purpose/consumer?** Generic public repository metadata description; node validation/wallet purpose and intended end user are missing.
2. **Getting started?** No installation or invocation; both interface lists are empty.
3. **Operations/config?** No node, build, test, or configuration procedures.
4. **Limits/prerequisites/effects?** Repository target `.`; common harvest limits only. Network/storage requirements and software effects are missing.
5. **Evidence?** Common harvest/provenance references; no node behavior or test results.

### RTK

`rtk-ai-rtk/retained-files/rtk_ai_rtk.core/specs/rtk.spec.yaml`

1. **Purpose/consumer?** `intent.summary` says language-neutral API-contract documentation/schema evidence, not command-output compression. Consumer is not explicit.
2. **Getting started?** No installation, invocation, or interface declarations.
3. **Operations/config?** No hook, analytics, telemetry, or configuration instructions.
4. **Limits/prerequisites/effects?** Repository target `.` and common harvest limits; actual CLI prerequisites/effects unspecified.
5. **Evidence?** Besides harvest evidence, `semantic_intent_static_evidence` contains lexical clusters referencing upstream `README.md` and `docs/TELEMETRY.md`. These embedded YAML classifications are not runtime verification or facts imported from `semantic.json`.

### Axios

`axios-axios/retained-files/axios_axios.axios/specs/axios.spec.yaml`

1. **Purpose/consumer?** `intent.summary` identifies a Promise HTTP client for browsers/Node.js.
2. **Getting started?** `interfaces.inbound[id=package.axios]` names the library; install/import/request examples are missing.
3. **Operations/config?** No methods, defaults, timeout, cancellation, or error contract.
4. **Limits/prerequisites/effects?** Repository target `.`; runtime versions, network effects, and security limits missing.
5. **Evidence?** Common static harvest reference supports package boundary/interface, not HTTP behavior.

### n8n agents

`n8n-io-n8n/retained-files/n8n_io_n8n.agents/specs/agents.spec.yaml`

1. **Purpose/consumer?** `intent.summary`: AI agent SDK for n8n's code-first execution engine; narrower than the platform README.
2. **Getting started?** `interfaces.inbound[id=package.agents]` names `@n8n/agents`; usable SDK examples are missing.
3. **Operations/config?** No SDK functions, configuration, or deployment workflow.
4. **Limits/prerequisites/effects?** Target `packages/@n8n/agents`; runtime requirements and effects unspecified. Cannot generalize to all n8n packages.
5. **Evidence?** Common static harvest reference and folder-scoped provenance; no SDK behavior tests.

## Separate semantic.json summary

Each repository's `semantic.json` is **proposal-only**, not retained YAML, acceptance, or verified behavior. Evidence paths/hashes are recorded bindings, not independently checked source facts. Reported execution boundaries show no materialization/publication/registry mutation.

- **Codex:** `proposal.claims` adds CLI entrypoint/local-agent specificity. `qualityStatus: eligible_for_calibration` does not mean accepted.
- **Bitcoin:** proposes CMake/vcpkg manifest discovery, not node operation; namespace repair proposed. `qualityStatus: review_required`; diagnostics include `purpose_outcome_anchor_missing`.
- **RTK:** `semanticPass.proposal` proposes compression, CLI/hooks, and intent reuse. **`qualityReport.status: rejected`**, `capability_namespace_violation`, `portableProposal: null`. Top-level `status: completed` means processing completed, not acceptance. These claims must not repair retained YAML answers.
- **Axios:** proposes concrete HTTP request/response and module-consumption capabilities; calibration-eligible only.
- **n8n:** proposes tool/catalog/sandbox/vector-store export capabilities for the SDK; calibration-eligible only, not proof of sandbox enforcement or full-platform behavior.
