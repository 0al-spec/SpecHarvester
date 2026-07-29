# Local Review Decision Service

Use `serve-local-review-decisions` to start the P54-T6 loopback-only decision
storage boundary. P54-T7 adds the four bounded reviewer actions, validated
reason codes, current progress, and portable decision exchange.

The service validates every decision against the Workbench schema and catalog
packet binding, requires exact Origin and CSRF checks for writes, uses atomic
current-state replacement, serializes transactions across workspace processes,
and preserves digest-addressed history. The schema is packaged as an importable
wheel resource, and restarting the service reloads the same validated state.

The local browser records `accept_for_intake`, `request_revision`, `defer`, or
`do_not_promote` through `POST /v0/actions`. `GET /v0/summary` reconciles
reviewed and unreviewed candidates. `GET /v0/export` and `POST /v0/import` move
digest-bound decision history between clean local workspaces while preserving
`registryMutationCount: 0`. The CSRF token is entered at runtime and is not
persisted in the generated browser or export.

Stored decisions remain local review evidence only. They do not accept packages,
run SpecPM, or mutate registry truth.
