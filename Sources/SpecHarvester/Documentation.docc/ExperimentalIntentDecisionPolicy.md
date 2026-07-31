# Experimental-Intent Decision Policy

P55-T10A binds one evidence-grounded reuse-versus-novelty policy into both
semantic-author providers.

An observed intent is reused when it already expresses the documented user
outcome. Generic package or repository intents require explicit comparison.
When no observed intent is sufficient, the provider may propose at most one
package-neutral `intent.experimental.*` value with a purpose claim, observed
nearby intents, non-goals, differentiation evidence, and a source-digest suffix.

The digest-bound policy fails closed for malformed decisions and treats synonym
or overlap risk as false novelty during calibration. It does not change the
frozen P55 quality thresholds or grant acceptance, canonicalization,
materialization, registry, or publication authority.
