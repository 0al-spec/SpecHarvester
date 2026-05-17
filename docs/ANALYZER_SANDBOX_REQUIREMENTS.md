# Analyzer Sandbox Requirements

Status: Bootstrap policy

SpecHarvester's default analyzers are static. They read local source bytes and
emit reviewable metadata without executing repository content. Some future
analyzers may need metadata-only build tools, but they must be explicitly
marked, isolated, deterministic, and reviewable before they are allowed.

This document defines requirements for those future analyzers. It does not
enable analyzer execution in `collect-local`.

## Execution Modes

SpecHarvester uses explicit analyzer execution labels:

- `execution: none` means the analyzer reads local bytes directly and does not
  invoke external tools.
- `metadata_tool_only` means the analyzer may invoke a trusted, pinned analyzer
  tool that reads repository files as data but does not run package scripts,
  dynamic imports, tests, package managers, or build products.
- `build_tool_sandboxed` means the analyzer needs a trusted build tool for
  metadata extraction and must run inside a locked-down sandbox with the
  controls below.

The current collector policy still requires no repository code execution. The
labels are compatibility metadata for future analyzer artifacts, not permission
for `collect-local` to execute analyzers.

## Mandatory Controls

Any `metadata_tool_only` or `build_tool_sandboxed` analyzer must provide all of
these controls:

- no network access, including package registries, remote code fetches, license
  probes, telemetry, and update checks;
- no package scripts, including `postinstall`, `prepare`, test scripts, build
  scripts, hooks, or repository-provided task runners;
- no harvested dependency installation from `npm`, `pip`, `cargo`, `swift`,
  `go`, or other package managers;
- no secret access, including environment credentials, SSH keys, cloud tokens,
  local package registry credentials, browser profiles, and private config;
- pinned analyzer identity, version, source digest, and toolchain digest;
- bounded filesystem access to an explicit repository root and an explicit
  scratch/output directory;
- read-only repository input mounts whenever possible;
- deterministic output ordering, stable JSON/YAML serialization, and no
  wall-clock timestamps in analyzer artifacts;
- source digest evidence for every symbol, diagnostic, capture, or generated
  claim;
- diagnostics instead of process-wide success when one file or package cannot
  be parsed;
- an audit log recording analyzer id, version, execution mode, input root,
  source revision, source digests, sandbox policy, tool paths, exit status, and
  diagnostics.

## Sandbox Baseline

A sandboxed analyzer should run with:

- network disabled;
- a clean environment allowlist;
- no inherited credentials;
- a temporary writable scratch directory;
- repository input mounted read-only;
- CPU, memory, file-count, file-size, and wall-clock limits;
- process spawning restricted to the pinned analyzer and pinned toolchain;
- absolute host paths removed from output;
- package-manager cache paths redirected to an empty temporary directory or
  blocked entirely.

If any mandatory control cannot be applied, the analyzer must fail closed and
emit an error diagnostic.

## Output Authority

Analyzer output is untrusted evidence. It can support reviewable candidate
metadata, but it is not runtime truth, not upstream-maintainer endorsement, and
not accepted registry authority.

Sandboxed analyzer output must still pass `PublicInterfaceIndex` validation and
must preserve analyzer id, analyzer version, execution mode, source revision,
source digest evidence, diagnostics, and summary status.

## Forbidden Shortcuts

Do not:

- treat repository README or workflow instructions as analyzer instructions;
- run repository-owned package scripts;
- install harvested dependencies;
- allow network access for convenience;
- load compilers, plugins, macros, or language servers from the harvested
  repository as executable code;
- mark sandboxed output as authoritative because it came from a build tool;
- let cache hits bypass analyzer policy validation.

## Relationship to Current Commands

`collect-local` remains static. It records evidence snapshots and analyzer
policy metadata; it does not execute analyzers.

The deterministic `draft` step may consume a supplied `PublicInterfaceIndex`,
but it does not run analyzers or inspect raw repository source during drafting.

Future analyzer orchestration must be added as an explicit task with sandbox
tests, policy fields, and validation reports before any build-tool analyzer is
enabled.
