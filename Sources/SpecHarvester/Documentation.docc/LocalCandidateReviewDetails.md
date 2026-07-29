# Local Candidate Review Details

Build digest-bound detail and comparison records from the P53-T14 portable
handoff with `build-local-candidate-review-details`, then supply the result to
``render-local-candidate-review-browser`` with `--details`.

The selected-candidate panel presents provenance, package topology, generated
files, diagnostics, and proposal-only static-versus-Codex Spark evidence as
inert local text. It cannot accept packages, mutate the registry, or run
candidate code.
