# Reviewer-Controlled Semantic Materialization

Use `materialize-semantic-candidate` to apply only explicitly accepted or edited
P55 semantic claims to a new preview candidate revision.

The command revalidates the complete proposal and reviewer-edit digests, copies
only package YAML, preserves the source candidate, records before/after
provenance, and runs SpecHarvester plus read-only SpecPM validation. Purpose,
capability, interface, non-goal, and bound intent proposals map to existing
SpecPM fields. Experimental intents remain non-canonical.

The result is candidate review evidence only. It remains `preview_only`, is not
registry truth, and does not mutate accepted packages, SpecPM, or the public
index.
