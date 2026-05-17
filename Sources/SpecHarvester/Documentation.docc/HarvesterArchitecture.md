# Architecture

SpecHarvester is a producer pipeline for candidate SpecPM packages.

## Pipeline Shape

```text
repository source list
        |
        v
safe evidence collector
        |
        v
evidence snapshot
        |
        v
deterministic candidate drafter
        |
        v
AI-assisted refinement, future
        |
        v
SpecPM validation
        |
        v
candidate review
        |
        v
controlled promotion
        |
        v
accepted registry source
```

## Components

### Safe Evidence Collector

Reads allowlisted static files from a public repository checkout and writes an
evidence snapshot. It does not execute package content.

Current command:

```bash
spec-harvester collect-local <repo> --out <candidate-dir>
```

### Deterministic Public Interface Analyzers

Extract compact `PublicInterfaceIndex` artifacts from local source bytes
without executing package code. Python uses the standard-library `ast` module,
and JavaScript/TypeScript uses package manifest entrypoints plus static export
scanning.

Analyzers can use an optional per-file cache keyed by analyzer id, analyzer
version, and file SHA-256 digest. The cache is derived untrusted metadata and
is ignored when metadata or path/evidence validation fails.

### Deterministic Candidate Drafter

Consumes evidence snapshots and drafts `specpm.yaml` plus
`specs/*.spec.yaml`. It can also consume a precomputed
`PublicInterfaceIndex` artifact and copy it into the candidate as
`public-interface-index.json`.

The draft is intentionally conservative. It records observed package metadata,
inferred capability IDs, inferred `intent.*` IDs, provenance, review
constraints, and analyzer-backed inbound interface summaries when a valid index
is provided. It does not claim upstream endorsement.

The drafter validates compact analyzer output; it does not run analyzers or
inspect raw repository source during candidate drafting.

### AI Draft Generator

Future component. Any model output must be treated as untrusted candidate
metadata, validated, and reviewed before acceptance.

### SpecPM Validation Gate

Every generated candidate must pass:

```bash
specpm validate <candidate-dir> --json
```

### Promotion Gate

Promotion copies a reviewed candidate into an accepted source root and can
append a local path entry to an accepted package manifest. It is not direct
publication.

## Non-Goals

SpecHarvester does not replace SpecPM, define the remote registry API, or make
generated specs canonical by itself.

## References

- `docs/ARCHITECTURE.md`
- <doc:TrustBoundary>
- <doc:Roadmap>
