# Analyzer Sandbox Requirements

SpecHarvester's default analyzers use `execution: none`: they read local source
bytes and emit reviewable metadata without executing repository content.

Future analyzers may declare `metadata_tool_only` or `build_tool_sandboxed`,
but only if they satisfy the sandbox controls below. These labels are analyzer
artifact metadata, not permission for `collect-local` to run analyzers.

## Required Controls

Every metadata-tool or build-tool analyzer must declare and enforce:

- no network access;
- no package scripts;
- no harvested dependency installation;
- no secret access;
- pinned analyzer identity, version, source digest, and toolchain digest;
- bounded filesystem access to an explicit repository root and scratch
  directory;
- deterministic output ordering and serialization;
- source digest evidence for every symbol, diagnostic, capture, or claim;
- diagnostics when one file or package cannot be parsed;
- an audit log with analyzer id, version, execution mode, source revision,
  sandbox policy, tool paths, exit status, and diagnostics.

## Sandbox Baseline

A `build_tool_sandboxed` analyzer should run with network disabled, a clean
environment allowlist, read-only repository input mounts, temporary writable
scratch space, CPU/memory/file/wall-clock limits, restricted process spawning,
and no host-specific absolute paths in output.

If any mandatory control cannot be applied, the analyzer must fail closed and
emit an error diagnostic.

## Output Authority

Analyzer output is untrusted evidence. It can support reviewable candidate
metadata, but it is not runtime truth, upstream-maintainer endorsement, or
accepted registry authority.

Sandboxed analyzer output must still pass `PublicInterfaceIndex` validation and
preserve analyzer id, analyzer version, execution mode, source revision, source
digest evidence, diagnostics, and summary status.

## Current Commands

`collect-local` remains static and does not run analyzers. The deterministic
`draft` step may consume a supplied `PublicInterfaceIndex`, but it does not run
analyzers or inspect raw repository source during drafting.

Future analyzer orchestration must be added by an explicit task with sandbox
tests, policy fields, and validation reports before any build-tool analyzer is
enabled.

## References

- `docs/ANALYZER_SANDBOX_REQUIREMENTS.md`
- <doc:TrustBoundary>
- <doc:HarvesterArchitecture>
