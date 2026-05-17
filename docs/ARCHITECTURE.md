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
`specs/*.spec.yaml`. It can also consume a precomputed
`PublicInterfaceIndex` JSON artifact and copy it into the candidate output as
`public-interface-index.json`.

The deterministic draft is intentionally conservative. It records observed
package metadata, inferred capability IDs, inferred `intent.*` IDs, provenance,
review constraints, and analyzer-backed inbound interface summaries when a
valid public interface index is provided. It does not claim upstream
endorsement.

Current command:

```bash
spec-harvester draft <harvest-dir-or-json> \
  --interface-index <public-interface-index.json> \
  --out <candidate-dir>
```

If no explicit index path is provided, the drafter only auto-detects
`public-interface-index.json` or `public_interface_index.json` beside
`harvest.json`. It does not run analyzers or inspect raw repository source
during drafting.

### AI Draft Generator

Future component. It may refine deterministic candidates using a bounded model
adapter. Model output must be treated as untrusted candidate metadata. It must
be validated and reviewed before acceptance.

### SpecPM Validation Gate

Every generated candidate must pass:

```bash
specpm validate <candidate-dir> --json
```

### Review Gate

Generated packages should not be accepted into a public registry without a
review gate. Reviewers should check scope, evidence, provenance, package IDs,
intent IDs, upstream relationship, and licensing statements.

### Promotion Gate

Copies a reviewed candidate into an accepted source root and optionally appends
a local `path` entry to an accepted package manifest. Promotion does not publish
to a remote registry by itself.

Current command:

```bash
spec-harvester promote <candidate-dir> --accepted-root <accepted-root>
```

## Non-Goals

SpecHarvester does not replace SpecPM.

SpecHarvester does not define the remote registry API.

SpecHarvester does not make generated specs canonical.

SpecHarvester does not imply upstream maintainer endorsement.
