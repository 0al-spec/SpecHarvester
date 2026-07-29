# Local Review Decision Service

Use `serve-local-review-decisions` to start the P54-T6 loopback-only decision
storage boundary.

The service validates every decision against the Workbench schema and catalog
packet binding, requires exact Origin and CSRF checks for writes, uses atomic
current-state replacement, serializes transactions across workspace processes,
and preserves digest-addressed history. The schema is packaged as an importable
wheel resource, and restarting the service reloads the same validated state.

Stored decisions remain local review evidence only. They do not accept packages,
run SpecPM, or mutate registry truth.
