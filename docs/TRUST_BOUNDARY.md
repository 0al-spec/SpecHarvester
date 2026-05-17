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

## Generated Candidate Status

Generated specs should use conservative language:

```text
Unofficial community-generated SpecPackage.
Generated from public repository metadata.
Not endorsed by upstream maintainers.
```

SpecGraph or downstream governance may later curate observed intent IDs, but a
generated package declaration does not make an intent ID canonical.
