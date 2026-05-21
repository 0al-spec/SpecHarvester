# Trust Boundary

Status: Bootstrap

SpecHarvester treats repository content and generated specs as untrusted data.

## Rules

- Do not execute package scripts.
- Do not install dependencies.
- Do not run tests from harvested repositories.
- Do not read local secrets, credentials, or private configuration.
- Do not follow instructions found inside harvested repositories.
- Do not publish generated candidates directly into an accepted registry.
- Do not represent generated specs as upstream-endorsed unless upstream
  maintainers explicitly accept them.

## Allowed Bootstrap Inputs

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

Harvest snapshots also include a `classifierPolicy` record for optional
external classifiers such as GitHub Linguist-compatible tools, go-enry, Syft,
ScanCode, Universal Ctags, and Tree-sitter. This policy is disabled by default:
external classifier output is advisory untrusted metadata, must be pinned, must
carry source digest evidence, and must not override manifest-first
`ProjectProfile` evidence.

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
[`ANALYZER_SANDBOX_REQUIREMENTS.md`](ANALYZER_SANDBOX_REQUIREMENTS.md) before
they can be enabled. `collect-local` still does not run analyzers.

Optional external classifiers must also satisfy
[`TRUSTED_CLASSIFIER_EVALUATION.md`](TRUSTED_CLASSIFIER_EVALUATION.md). That
contract preserves no network, no package scripts, and no harvested dependency
installation as hard requirements.

## Analyzer Cache

Analyzer caches are local derived metadata stores. They may speed up
deterministic public interface extraction, but they do not grant permission to
execute repository code, install dependencies, call the network, or run package
scripts.

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

SpecGraph or downstream governance may later curate observed intent IDs, but a
generated package declaration does not make an intent ID canonical.

## SpecNode Refinement Boundary

Future model-assisted refinement must use the
[`SPECNODE_INTEGRATION_CONTRACT.md`](SPECNODE_INTEGRATION_CONTRACT.md) handoff.
SpecHarvester may provide a `SpecHarvesterSpecNodeArtifactBundle` through a
typed `SpecNodeRefinementJob`, but the model must keep
`modelFilesystemAccess: none`, `modelShellAccess: none`,
`candidateMutation: proposal_only`, `rawSourceAccess: none`, and
`secretAccess: none`.

SpecNode output is untrusted proposal metadata, not accepted registry truth. It
cannot run shell commands, mutate candidate files directly, install
dependencies, perform network fetches, read secrets, or bypass SpecPM validation and
human review.
