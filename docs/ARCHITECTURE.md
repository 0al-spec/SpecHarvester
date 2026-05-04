# SpecHarvester Architecture

Status: Bootstrap

SpecHarvester is a producer pipeline for candidate SpecPM packages.

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
AI draft generator
        |
        v
SpecPM validation
        |
        v
candidate review
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

### AI Draft Generator

Future component. It should consume evidence snapshots and draft
`specpm.yaml` plus `specs/*.spec.yaml`.

The model output must be treated as untrusted candidate metadata. It must be
validated and reviewed before acceptance.

### SpecPM Validation Gate

Every generated candidate must pass:

```bash
specpm validate <candidate-dir> --json
```

### Review Gate

Generated packages should not be accepted into a public registry without a
review gate. Reviewers should check scope, evidence, provenance, package IDs,
intent IDs, upstream relationship, and licensing statements.

## Non-Goals

SpecHarvester does not replace SpecPM.

SpecHarvester does not define the remote registry API.

SpecHarvester does not make generated specs canonical.

SpecHarvester does not imply upstream maintainer endorsement.
