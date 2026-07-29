# Local Review Decision Service

Use `serve-local-review-decisions` to start the P54-T6 loopback-only decision
storage boundary.

The service validates every decision against the Workbench schema and catalog
packet binding, requires exact Origin and CSRF checks for writes, uses atomic
current-state replacement, and preserves digest-addressed history. Restarting
the service reloads the same validated state.

Stored decisions remain local review evidence only. They do not accept packages,
run SpecPM, or mutate registry truth.
