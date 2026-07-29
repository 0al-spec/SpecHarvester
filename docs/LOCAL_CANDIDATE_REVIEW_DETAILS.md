# Local Candidate Review Details

P54-T5 builds a static, digest-bound detail set for the P53-T14 portable
handoff. It is evidence for local maintainer review only and does not change
SpecPM, a registry, or candidate package state.

```bash
spec-harvester build-local-candidate-review-details \
  --archive SPECS/EVIDENCE/P53-T14/P53-T14_Portable_Handoff.tar.gz \
  --expected-sha256 db2593d7b17fd3f0da348b3fce72ea86b510d7c562b82b78047b926608709e63 \
  --catalog SPECS/EVIDENCE/P54-T3/P54-T3_Candidate_Review_Catalog.json \
  --output review-workspace/details.json
```

Each record is bound to the exact packet digest already present in the catalog.
The set includes verified provenance, package topology, file inventory,
generated `specpm.yaml` and specs, diagnostics and triage data, plus a separate
proposal-only static-versus-Codex Spark comparison. Oversized generated files
are represented by a visible omission marker rather than being silently
truncated.

The local browser validates the source bundle digest, every detail/comparison
record, and the complete candidate identity set before copying it to the
browser bundle. Candidate-provided text is displayed only through text nodes
under the browser's restrictive local CSP.
