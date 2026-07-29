# Local Review Decision Service

P54-T6 provides a loopback-only persistence boundary for local Workbench
decisions. It stores non-authoritative review evidence; it does not accept a
package, invoke SpecPM, or mutate registry state.

```bash
spec-harvester serve-local-review-decisions \
  --workspace review-workspace \
  --catalog SPECS/EVIDENCE/P54-T3/P54-T3_Candidate_Review_Catalog.json \
  --allowed-origin http://127.0.0.1:8000 \
  --csrf-token '<operator-generated-token-with-at-least-32-characters>' \
  --host 127.0.0.1 \
  --port 8765
```

Writes use `POST /v0/decisions` with `Content-Type: application/json`, the exact
configured `Origin`, and `X-CSRF-Token`. Reads use
`GET /v0/decisions/{candidateId}`.

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

The CSRF token is an operator secret and must not be committed, placed in
candidate content, or persisted in exported review evidence.
