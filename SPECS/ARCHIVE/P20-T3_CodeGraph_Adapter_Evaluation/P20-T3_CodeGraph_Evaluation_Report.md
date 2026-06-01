# P20-T3 CodeGraph Adapter Evaluation Report

**Date:** 2026-05-31
**Verdict:** PASS — suitable for a future explicit optional adapter, not for
default collector integration.

## Sources Reviewed

- GitHub repository: <https://github.com/colbymchenry/codegraph>
- Shallow clone commit: `b026e64b413bb4dca1bc7326d7de0837afe0a899`
- npm package metadata: `@colbymchenry/codegraph@0.9.7`
- npm platform package metadata: `@colbymchenry/codegraph-darwin-arm64@0.9.7`
- Local package tarball: `codegraph-0.9.7.tgz`
- Source files inspected:
  - `src/db/schema.sql`
  - `src/types.ts`
  - `src/bin/codegraph.ts`
  - `npm-shim.js`
  - `LICENSE`

## Package and License Signals

| Signal | Value |
|---|---|
| Main package | `@colbymchenry/codegraph` |
| Version checked | `0.9.7` |
| License | MIT |
| Main npm integrity | `sha512-sBZnnKGkUdmM3BOkvfFq6wdK2OC/sA7nLMh28voan82xFzRp8irEVCakywfOXfDE4bkVModWvucz85f3+YMO6w==` |
| Main npm shasum | `72131a74720bebf719e13ebcbf37f0554cc6cac0` |
| Platform package | `@colbymchenry/codegraph-darwin-arm64@0.9.7` |
| Platform npm integrity | `sha512-bQSQSBAeC2HRC4A0wH/T1sOxvLgtNlc7pIjz6vV03ccg0T7zhD0WfyO+HTQRdD1RzAdAILhIB1TJpCQsREoHrg==` |
| Platform npm shasum | `303af1dd3152a6024615ea4ae8c09007239273af` |
| Modified timestamp from npm | `2026-05-28T20:30:26.391Z` |

MIT is compatible with optional local integration, but SpecHarvester should
record the analyzer license in provenance because output would be produced by a
third-party binary.

## Installation Surface

`@colbymchenry/codegraph` is a small npm shim package. The real executable is a
per-platform optional dependency or a GitHub Releases fallback download.
The shim can download missing platform bundles into `~/.codegraph` unless
`CODEGRAPH_NO_DOWNLOAD=1` is set.

Implications for SpecHarvester:

- Do not auto-install `codegraph`.
- Do not invoke the interactive installer.
- Do not allow implicit fallback downloads inside normal harvest/draft flows.
- Require an already-installed executable path or explicit opt-in environment.
- Prefer `CODEGRAPH_NO_DOWNLOAD=1` during compatibility checks and ordinary
  CI. If an optional live smoke intentionally exercises npm shim fallback
  behavior, first verify that the pinned shim version supports
  `CODEGRAPH_INSTALL_DIR`; otherwise treat the cache path as not redirectable
  and use only `CODEGRAPH_NO_DOWNLOAD=1` or a pinned `CODEGRAPH_DOWNLOAD_BASE`.
- Record executable path, analyzer version, package integrity when available,
  and executable digest when running a live adapter.

## Capability Fit

README and source code show a local SQLite knowledge graph with:

- nodes for files, modules, classes, structs, interfaces, traits, protocols,
  functions, methods, properties, fields, variables, constants, enums, type
  aliases, namespaces, imports, exports, routes, and components.
- edges for contains, calls, imports, exports, extends, implements, references,
  type relationships, returns, instantiates, overrides, and decorators.
- file records with content hashes, detected language, size, indexed timestamp,
  node count, and extraction errors.
- JSON CLI output for `status`, `query`, `files`, `callers`, `callees`,
  `impact`, and `affected`.
- broad language coverage including Swift, Objective-C, JS/TS, Python, Go,
  Rust, Java/Kotlin, PHP, Ruby, C/C++, C#, Dart, Lua/Luau, Svelte, Vue, and
  others.

This matches the Phase 20 need: scoped folder/file specs need source-unit graph
evidence across languages and frameworks without pretending that every unit is
a package-manager package.

## Schema Stability

The SQLite schema has an explicit `schema_versions` table and `project_metadata`
table, but the public compatibility contract is not a SpecHarvester-owned
standard. The observed schema is useful but should be treated as adapter-local
input, not as stable registry evidence.

Recommended normalized evidence shape:

```yaml
kind: source_graph_index
schema_version: spec-harvester-codegraph-v1
trust:
  analyzer: codegraph
  analyzer_version: "0.9.7"
  analyzer_license: MIT
  trust_level: untrusted_optional_tool
  executed_repository_code: false
  allowed_network: false
source:
  target_kind: repository|folder|file
  target_path: ...
  source_digests:
    - path: ...
      sha256: ...
summary:
  file_count: 0
  node_count: 0
  edge_count: 0
  languages: []
nodes:
  - id: ...
    kind: function|class|method|...
    name: ...
    qualified_name: ...
    file_path: ...
    language: ...
    range:
      start_line: 1
      end_line: 1
    visibility: public|private|protected|internal|null
    signature: ...
edges:
  - source: ...
    target: ...
    kind: calls|imports|contains|...
    provenance: tree-sitter|heuristic|null
diagnostics: []
```

The adapter should normalize from CLI JSON or SQLite into this SpecHarvester
shape, then let drafting consume the normalized evidence. Drafting must not read
`.codegraph/codegraph.db` directly.

## Interface Compatibility Guard

The important CI check is interface compatibility, not whether CodeGraph can
successfully run over an arbitrary third-party project on every CI run.

Recommended compatibility checks:

- Pin the expected CodeGraph package version and package integrity in a local
  SpecHarvester fixture.
- Verify that the configured executable, when explicitly available, reports the
  pinned version.
- Verify that the CLI surface still exposes the JSON-producing commands needed
  by the adapter: `status --json`, `query --json`, `files --json`,
  `callers --json`, `callees --json`, `impact --json`, and `affected --json`.
- Keep small captured JSON fixtures for the normalized records SpecHarvester
  consumes, then validate those fixtures against a SpecHarvester-owned schema.
- Keep live indexing of real repositories out of ordinary CI. If needed, run it
  manually or in an explicit `workflow_dispatch` job with a pre-provisioned,
  pinned `codegraph` executable.

This makes CI answer the compatibility question: "does our adapter still match
the pinned CodeGraph interface?" It does not try to prove that every supported
language or every upstream project indexes correctly on CI.

## Trust Policy

`codegraph` claims local-only indexing and uses tree-sitter plus SQLite, but it
is still a third-party executable. Treat it differently from trusted in-process
Python AST analyzers.

Policy:

- Analyzer classification: `third_party_local_binary`.
- Evidence trust: untrusted/assistive evidence, never authoritative by itself.
- Repository code execution: prohibited.
- Network access: prohibited during adapter execution.
- Installation: out of band, explicit opt-in only.
- Input scope: only the selected source target and inherited repository root
  metadata.
- Output scope: normalized graph summary plus bounded nodes/edges, with size
  limits.
- Provenance: include analyzer version, executable digest, command arguments,
  source target metadata, source file digests, and adapter version.

## Performance and Smoke Notes

The platform bundle is approximately `45.5 MB`. A direct download was started to
inspect the executable and interrupted after about 35 seconds at roughly 15%,
because full binary installation is not required for this evaluation PR and the
adapter must not depend on auto-download behavior.

Commands that were safe and useful:

```bash
npm view @colbymchenry/codegraph version license dist.tarball bin --json
npm view @colbymchenry/codegraph dependencies optionalDependencies peerDependencies --json
npm view @colbymchenry/codegraph dist.integrity dist.shasum time.modified repository homepage --json
npm view @colbymchenry/codegraph-darwin-arm64@0.9.7 version license dist.tarball dist.integrity dist.shasum --json
curl -L --retry 3 --retry-delay 2 --fail https://registry.npmjs.org/@colbymchenry/codegraph/-/codegraph-0.9.7.tgz -o /tmp/codegraph-0.9.7.tgz
git clone --depth 1 https://github.com/colbymchenry/codegraph.git /tmp/codegraph-repo
```

The first `npx --yes @colbymchenry/codegraph --help` and `npm pack` attempts hit
transient `ECONNRESET` from the npm registry. Retrying metadata queries and the
small package tarball succeeded. This reinforces that future tests must not make
ordinary CI depend on live npm/GitHub downloads.

## Recommendation

Proceed with `codegraph` only as a follow-up optional adapter:

- Good fit for multi-language source-unit graph evidence.
- Good fit for token/time reduction goals when a local index already exists.
- Not suitable as a default dependency or automatic installer.
- Not suitable as a trusted evidence source without normalization and explicit
  provenance.
- Best first integration is a read-only CLI probe that consumes existing
  `codegraph ... --json` output or an existing `.codegraph/codegraph.db`,
  normalizes into SpecHarvester evidence, and fails closed when unavailable.

## Follow-Up Tasks Added

- `P20-T6` — Implement an explicit opt-in CodeGraph adapter boundary that never
  installs or downloads tools, records analyzer/executable provenance, and
  normalizes JSON/SQLite graph evidence into SpecHarvester-owned
  `source_graph_index` evidence.
- `P20-T7` — Add a pinned CodeGraph interface compatibility guard that verifies
  the expected package version, binary availability contract, CLI JSON flags,
  and normalized schema mapping without indexing third-party projects in
  ordinary CI.
