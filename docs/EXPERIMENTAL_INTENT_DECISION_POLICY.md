# Experimental-Intent Decision Policy

P55-T10A adds one provider-neutral decision policy between observed intent
metadata and an AI-authored semantic proposal. It addresses the P55-T10
baseline in which all 48 generic observed intent references were reused and no
experimental intent was proposed.

## Decision

The semantic author compares the documented user outcome with observed intents:

1. Reuse an observed intent when it already expresses that outcome.
2. A generic package or repository intent requires an explicit,
   evidence-grounded `nearby_intent_difference` rationale before reuse.
3. When no observed intent is sufficient, propose at most one visibly
   non-canonical `intent.experimental.*` value.
4. Do not propose novelty merely because a generic intent is present.

An experimental proposal binds its user need to a `purpose` claim, cites at
least one observed nearby intent, cites one or more `non_goal` claims, and
includes nearby-intent differentiation. Its identifier contains two to six
package-neutral user-outcome terms plus the first eight hexadecimal characters
of the source bundle digest, for example:

```text
intent.experimental.reduce_ai_context.a1b2c3d4
```

The suffix makes repeated author passes deterministic and separates otherwise
identical proposed labels from different evidence bundles. Package, vendor,
and repository names are not valid semantic terms in the identifier.

## Validation

The policy is stored as a canonical JSON fixture with a SHA-256 digest and is
included in the shared Codex 5.3 Spark and LM Studio provider request. The pass
fails closed for stale policy data, more than one experimental intent, malformed
or non-bound identifiers, unknown nearby intents, invalid claim kinds, generic
reuse without explicit comparison, and simultaneous generic reuse plus novelty.

Quality diagnostics separately mark synonym or overlap risk as false novelty.
That signal is a calibration failure for P55-T10B; it does not redefine the
P55-T5 numerical thresholds.

## Authority

Both reuse and experimental decisions remain proposal-only evidence. The policy
cannot accept or edit a proposal, canonicalize an intent, materialize a
candidate, mutate SpecPM or registry truth, or publish an artifact. Those
decisions remain explicit maintainer and SpecPM governance actions.
