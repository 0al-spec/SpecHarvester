# T6 Candidate-Only Review

**All notes: AI assistance, maintainer confirmation pending.** Bounded agent-assisted artifact-only review, not human approval. All behavior below is what the **candidate claims**, not independently proven behavior. No builds, tests, network checks, or provenance verification were performed. Main owns integration and original data.

Paths below are relative to each named repository's `new/original/` directory under `comparison-t5-offline-20260906/`. `S` means `specs/main.spec.yaml`; `M` means `specpm.yaml`. Candidate manifests, specs, and selected packaged evidence were inspected, including packaged README excerpts. Upstream standalone README, retained files, semantic references, and original checkouts were not used for these answers. Missing guidance means missing from reviewed material, not necessarily absent upstream. All manifests set `preview_only: true`; all specs have `metadata.status: draft` and empty `implementationBindings`.

Main-agent verification corrected four initial quick-start omissions: the delegated review had over-excluded packaged README excerpts. The corrected answers below include those candidate-owned files, without importing facts from standalone reference surfaces. No commands were executed.

## openai-codex

1. **Purpose/consumer:** Candidate claims a local repository-oriented coding agent for developers and application embedders, through CLI, TypeScript, and Python; desktop, IDE, and cloud surfaces are excluded. [M: `metadata.summary`; S: `intent`, `scope`]
2. **Public interface/getting started:** Packaged overview includes a CLI installer command, `codex` and ChatGPT sign-in; API-key setup links outward. TypeScript uses `Codex.startThread()` then `run()`/`runStreamed()`; Python uses `Codex()` then `thread_start().run(...)`. Detailed `codex exec` contract remains missing here. [S: `interfaces.inbound`; `evidence/product-overview.md`:5-15; `evidence/python-sdk.md`: example]
3. **Operations/config:** Working directory, `skipGitRepoCheck`, inherited or explicit `env`, CLI `config` overrides, and resumption from `~/.codex/sessions` are described. Deployment/retention guidance remains incomplete. [S: `interfaces.outbound`; `evidence/typescript-sdk.md`]
4. **Limits/prerequisites/effects:** Node 18+, authenticated CLI, normally a Git repository; Python minimum unspecified. Process spawning, workspace reads/writes, logging, and network use are claimed. Approval callback presence does not establish secure defaults or sandbox enforcement. [S: `constraints`, `effects`; `evidence/python-sdk.md`: Author notes]
5. **Pinned evidence:** SDK excerpts record revision `16d7daad7c5dc73da8558102a65bb7d7709807e1`, source ranges, and full-source SHA-256 values. Documentation and a partial client excerpt support interface descriptions, not successful or safe execution; hashes were not verified. [`evidence/typescript-sdk.md`, `evidence/python-sdk.md`: Provenance]

## bitcoin-bitcoin

1. **Purpose/consumer:** Candidate claims a fully validating Bitcoin node for operators, optionally exposing wallet, RPC, and GUI functionality. [M: `metadata.summary`; S: `intent`, `provides.capabilities`]
2. **Public interface/getting started:** Unpack binaries; launch `bin/bitcoind` or `bin/bitcoin-qt`; wrapper subcommands expose node/GUI/RPC. Authenticated RPC uses `/` or `/wallet/<walletname>/`. Acquisition, full build dependencies, and a complete first RPC example are missing here. [`evidence/operational-files.md`; S: `interfaces.inbound`]
3. **Operations/config:** Manually create `bitcoin.conf`; changes require restart. Data includes logs, settings, authentication cookie, blockchain state, and optional wallets. Daemon RPC defaults enabled; GUI RPC defaults disabled, configurable with `-server`. [S: `constraints.restart_configuration`, `interfaces.outbound`; `evidence/operational-files.md`, `evidence/rpc.md`]
4. **Limits/prerequisites/effects:** No public-Internet RPC exposure; credentials lack transport encryption. Wallet files must not be shared between instances. Network/state writes and fund-spending RPC effects are claimed; resource sizing and release stability remain unestablished. [S: `constraints`, `effects`, `scope.excludes`]
5. **Pinned evidence:** Revision `a2aab6df97d9f3e1186e8c3fc57ad909cc8aef9b`, source ranges, and full-file digests accompany documentation references. Provenance explicitly disclaims build/runtime/conformance execution; excerpts do not prove validation correctness. [`evidence/source-provenance.md`; S: `evidence`]

## rtk-ai-rtk

1. **Purpose/consumer:** Candidate claims shell-output compression and command rewriting for AI-agent workflows, with passthrough for unsupported commands. [M: `metadata.summary`; S: `intent`, `provides.capabilities`]
2. **Public interface/getting started:** `rtk <supported-command>`, proxy and rewrite are described. Packaged quick start lists assistant-specific init commands including `rtk init -g --codex`, then restart and `git status` test. Binary acquisition remains absent from this excerpt. [S: `interfaces.inbound`; `evidence/readme-excerpt.md`: Quick Start]
3. **Operations/config:** `rtk config --create`, platform TOML locations, tracking retention/database, tee recovery, and telemetry opt-out are documented. Windows configuration location is not supplied in this excerpt. [`evidence/configuration-excerpt.md`]
4. **Limits/prerequisites/effects:** Underlying tools are required; savings are approximate, not billing guarantees. Rewrite is not authorization. Spawned commands, SQLite tracking, raw-output files, and telemetry can have effects. [S: `constraints`, `effects`; `evidence/rewrite-excerpt.rs`: exit table and `evaluate`]
5. **Pinned evidence:** Revision `7da2674073394194754a228d346189a74869e6ba` plus ranges/full-file digests maps CLI, runner, rewrite, configuration, and selected test excerpts. Packaged test claims are not test-run receipts or universal semantic-equivalence proof. [`evidence/source-notes.md`; S: `evidence`]

## axios-axios

1. **Purpose/consumer:** Candidate claims a Promise-based HTTP library for browser/Node JavaScript and TypeScript applications, not a server or CLI. [M: `metadata`; S: `intent`, `scope`]
2. **Public interface/getting started:** Packaged README includes `import axios from 'axios'`, an awaited GET with error handling and an `axios.create()` example. Package metadata identifies module/type entry points; dependency installation is absent from this excerpt. [S: `interfaces`; `evidence/README-excerpt.md`:18-28,90-100; `evidence/package-metadata.md`]
3. **Operations/config:** Instance defaults, per-request configuration, interceptors, timeout, headers, response types, status validation, and cancellation are described. Adapter selection and exhaustive field behavior remain uncertain. [S: `provides.capabilities`, `interfaces`; `evidence/source-notes.md`]
4. **Limits/prerequisites/effects:** Promise support required; timeout and body caps recommended; AbortController preferred. Outbound HTTP and callbacks are claimed; remote mutation consequences are not characterized by the effect list. [S: `constraints`, `effects`]
5. **Pinned evidence:** Revision `509719387e4993392ca40da03a49678269cdfb90`, ranges/full-file digests, types and metadata are referenced. Packaged README examples cover requests, responses, errors and cancellation; documentation and declarations do not prove runtime transport behavior. [`evidence/source-notes.md`, `evidence/README-excerpt.md`; S: `evidence`]

## n8n-io-n8n

1. **Purpose/consumer:** Candidate claims workflow automation for teams plus Instance AI resource inspection/building assistance. [M: `metadata.summary`; S: `intent`, `provides.capabilities`]
2. **Public interface/getting started:** Packaged overview includes `npx n8n`, Docker volume/run commands with port 5678 and editor URL. Workflow tools expose identifiers and inputs. Instance AI HTTP route/payload is not established here. [S: `interfaces.inbound`; `evidence/product-overview.md`:16-31; `evidence/instance-ai-tools.md`]
3. **Operations/config:** Model/provider credentials, MCP/search, sandbox settings, settings-over-environment precedence, database persistence, and shutdown workspace destruction are described. [`evidence/instance-ai-configuration.md`]
4. **Limits/prerequisites/effects:** Builder requires enabled sandbox/provider configuration. Workflow/database writes, network calls, and code execution are claimed. Verification simulation is documentation, not proven isolation; licensing permission requires separate confirmation. [S: `constraints`, `effects`; `evidence/instance-ai-tools.md`]
5. **Pinned evidence:** Revision `082b5d9190f4bc81d93c6a94d6d4692bed4660ca` includes ranges/full-file digests for configuration, tools, sandbox, overview, and license references. Evidence does not establish runtime safety, complete routes, or deployment-specific license permission. [`evidence/source-provenance.md`; S: `evidence`]
