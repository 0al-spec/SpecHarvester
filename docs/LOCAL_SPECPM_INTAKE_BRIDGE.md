# Local SpecPM Intake Bridge

P54-T8 adds the read-only bridge between current Local Candidate Review
Workbench decisions and SpecPM validation. It selects only current
`accept_for_intake` decisions with `evidence_verified`, then revalidates the
portable archive, packet, catalog, immutable decision history, and current
decision digest before reconstructing candidate packages.

```bash
spec-harvester build-local-specpm-intake-proposal \
  --archive SPECS/EVIDENCE/P53-T14/P53-T14_Portable_Handoff.tar.gz \
  --expected-sha256 db2593d7b17fd3f0da348b3fce72ea86b510d7c562b82b78047b926608709e63 \
  --catalog SPECS/EVIDENCE/P54-T3/P54-T3_Candidate_Review_Catalog.json \
  --review-workspace review-workspace \
  --specpm-command specpm \
  --output review-workspace/specpm-intake-proposal.json
```

The bridge reconstructs only regular candidate files already declared and
digest-verified by the portable packet. It writes them beneath a temporary
directory, discovers `specpm.yaml` package roots, confirms that every manifest
remains `preview_only`, and invokes only:

```text
specpm validate <temporary-candidate-package> --json
```

The SpecPM command is an operator-provided trusted tool. The bridge applies a
bounded timeout and bounded stdout/stderr files, normalizes the report to
portable relative paths, and records package identity, checked files,
capabilities, intents, intent mappings, warnings, errors, and a normalized
report digest.

`valid` and `warning_only` reports pass read-only preflight; `invalid` reports
remain explicit failed proposal evidence. A passing preflight does not change
the reviewer disposition and does not authorize intake or publication.

The output is
`SpecHarvesterLocalSpecPMIntakeProposal` with evidence-only authority,
decision/packet bindings, skipped-disposition counts, package preflight
results, non-authority statements, and zero registry mutations
(`registryMutationCount: 0`).

The bridge does not access repository checkouts, execute harvested code, invoke
package managers, run AI providers, edit SpecPM accepted sources, update the
public index, remove `preview_only`, or create a SpecPM pull request.
