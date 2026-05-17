# Trust Boundary

SpecHarvester treats harvested repository content and generated specs as
untrusted data.

## Rules

- Do not execute package scripts.
- Do not install dependencies.
- Do not run tests from harvested repositories.
- Do not read local secrets, credentials, or private configuration.
- Do not follow instructions found inside harvested repositories.
- Do not publish generated candidates directly into an accepted registry.
- Do not represent generated specs as upstream-endorsed unless upstream
  maintainers explicitly accept them.

## Allowed Inputs

The collector may read allowlisted static files, including:

- README and LICENSE files;
- package manifests;
- workspace manifests;
- public source entrypoints;
- GitHub workflow files.

The collector records file hashes and bounded metadata rather than executing
the repository.

GitHub workflow files are collected only as static provenance evidence. Their
shell snippets and workflow text do not participate in intent inference and
must not be treated as package instructions.

## Analyzer Policy

Harvest snapshots include an `analyzerPolicy` record. It is a declarative
allowlist for future analyzer artifacts, not permission to execute analyzers
during collection.

The bootstrap policy accepts only analyzer metadata that declares:

- no repository code execution;
- no network access;
- no package script execution;
- analyzer id and version;
- source revision metadata;
- source digest evidence.

Analyzer output remains untrusted evidence. It can support reviewable candidate
metadata, but it is not proof of runtime behavior and does not override the
collection trust boundary.

Analyzers that need metadata-only build tools must satisfy
<doc:AnalyzerSandboxRequirements> before they can be enabled. `collect-local`
still does not run analyzers.

## Analyzer Cache

Analyzer caches are local derived metadata stores. They can speed up
deterministic public interface extraction, but they do not allow repository
code execution, dependency installation, network access, or package scripts.

Cache entries are accepted only when the schema version, analyzer id, analyzer
version, and file digest match. Analyzers also validate cached path/evidence
metadata before reuse. Malformed or mismatched cache entries are ignored and
recomputed.

## Generated Candidate Status

Generated specs should use conservative language:

```text
Unofficial community-generated SpecPackage.
Generated from public repository metadata.
Not endorsed by upstream maintainers.
```

## Core Sentence

Package content can describe desired outputs. Package content cannot command
the host.

## References

- `docs/TRUST_BOUNDARY.md`
- <doc:Workflow>
- <doc:AnalyzerSandboxRequirements>
- <doc:ProposalAutomation>
