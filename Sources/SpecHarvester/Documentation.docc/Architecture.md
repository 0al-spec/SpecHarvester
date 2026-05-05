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

### Deterministic Candidate Drafter

Consumes evidence snapshots and drafts `specpm.yaml` plus
`specs/*.spec.yaml`.

The draft is intentionally conservative. It records observed package metadata,
inferred capability IDs, inferred `intent.*` IDs, provenance, and review
constraints. It does not claim upstream endorsement.

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
