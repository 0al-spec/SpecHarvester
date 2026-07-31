# Local Review Decision Service

P54-T6 provides the loopback-only persistence boundary for local Workbench
decisions. P54-T7 adds bounded reviewer actions, progress summaries, and
portable decision exchange. The service stores non-authoritative review
evidence; it does not accept a package, invoke SpecPM, or mutate registry state.

```bash
spec-harvester serve-local-review-decisions \
  --workspace review-workspace \
  --catalog SPECS/EVIDENCE/P54-T3/P54-T3_Candidate_Review_Catalog.json \
  --details review-workspace/details.json \
  --allowed-origin http://127.0.0.1:8000 \
  --csrf-token '<operator-generated-token-with-at-least-32-characters>' \
  --host 127.0.0.1 \
  --port 8765
```

The browser uses `POST /v0/actions` with `Content-Type: application/json`, the
exact configured `Origin`, and `X-CSRF-Token`. The service creates the timestamp
and catalog packet binding. The action must select one valid pair:

| Disposition | Reason code |
| --- | --- |
| `accept_for_intake` | `evidence_verified` |
| `request_revision` | `evidence_revision_required` |
| `defer` | `review_deferred` |
| `do_not_promote` | `promotion_not_suitable` |

`POST /v0/decisions` remains available for complete schema-valid records.
Read-only endpoints expose one current decision, all current decisions, the
reason taxonomy, and corpus progress:

- `GET /v0/decisions/{candidateId}`
- `GET /v0/decisions`
- `GET /v0/reasons`
- `GET /v0/summary`

`GET /v0/export` emits all immutable decision history in deterministic
candidate and lineage order. `POST /v0/import` accepts that JSON only when its
source-bundle digest, packet bindings, reason mappings, and prior-decision
chain match the target workspace. Import writes require the same Origin and
CSRF checks as actions. New decisions are rejected before persistence if they
would make the canonical export exceed the import transport limit, so every
export produced by the service remains importable. The export fixes
`registryMutationCount` at zero.

With `--details`, P55-T7 also permits one semantic reviewer edit inside a
candidate decision. The service revalidates the complete portable semantic
record and requires exact candidate packet, semantic record, proposal, and
source-bundle digests. It computes the reviewer-edit digest itself and accepts
only:

- `accepted` with one or more selected proposal claim IDs;
- `edited` with selected claim IDs and bounded replacement text;
- `rejected` or `deferred` without selected or edited claims.

Unknown claims, stale proposal records, duplicate edits, unsupported fields,
empty reviewer identities, and incoherent decision/edit combinations fail
before persistence. The semantic record is optional for ordinary candidate
decisions, but a semantic action is rejected when no complete record is present
in the configured detail set.

Every submitted record must match the P54-T2 decision schema and the exact
candidate/packet binding in the validated P54-T3 catalog. A first decision must
have `priorDecisionSha256: null`; a replacement must carry the SHA-256 of the
actual current decision. Stale replacements are rejected.

Current records live under `decisions/`; immutable digest-addressed copies live
under `history/`. Writes use a same-filesystem temporary file, durable flush,
atomic replacement, and a workspace file lock that serializes the complete
read/check/write transaction across service processes. The store rejects path traversal, symlink escapes,
unknown candidates, stale packet digests, malformed records, oversized bodies,
non-loopback binding, untrusted origins, and invalid CSRF tokens.

The P54 Workbench JSON Schema is packaged inside the installed wheel, so the
service does not depend on a repository checkout or editable installation.

The browser asks for service URL, reviewer identity, and the CSRF token at
runtime. The token is an operator secret and must not be committed, placed in
candidate content, local storage, generated browser files, or exported review
evidence.
