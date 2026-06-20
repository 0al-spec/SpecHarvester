# Bounded Popular-Library Pilot Manifest

Status: P46-T1 pilot manifest.

P46-T1 defines the first post-hardening bounded popular-library pilot manifest.
It does not run the pilot. It prepares the pinned local input that P46-T2 can
run in static-only mode before any AI-enabled pilot run is allowed.

The source manifest is:

```text
inputs/p46-bounded-popular-library-pilot/repositories.yml
```

The durable fixture is:

```text
tests/fixtures/bounded_popular_library_pilot_manifest/p46-t1-bounded-popular-library-pilot-manifest.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.bounded-popular-library-pilot-manifest/v0
kind: SpecHarvesterBoundedPopularLibraryPilotManifest
authority: producer_bounded_pilot_manifest_only
```

## Selected Repositories

The manifest selects exactly six pinned local checkouts:

| Repository | Ecosystem | Package id | Expected shape |
| --- | --- | --- | --- |
| Flask | Python / PyPI | `flask.core` | `python_web_framework_single_package` |
| Gin | Go | `gin.core` | `go_web_framework_single_package` |
| xyflow | JavaScript / TypeScript / npm | `xyflow.workspace` | `javascript_typescript_package_set` |
| Cupertino | SwiftPM | `cupertino.core` | `swift_spm_ui_single_package` |
| NavigationSplitView | SwiftPM | `navigation_split_view.core` | `swift_spm_ui_single_package` |
| docc2context | SwiftPM / CLI | `docc2context.core` | `swift_cli_documentation_single_package` |

This keeps the pilot bounded while covering Python, Go, JavaScript,
TypeScript, and Swift. The set intentionally includes both single-package and
package-set shapes.

## Carry-Forward Warning

Gin carries the P45 warning context:

```text
model_evidence_path_unsupported
```

The warning is non-blocking for pilot start, but P46-T4 and P46-T5 must keep it
visible as a registry-promotion blocker until triaged.

xyflow carries an operator checkout caveat because the local checkout origin is
a fork while the manifest records the canonical upstream repository.

## Stop Conditions

P46-T2 must stop before candidate generation or handoff if any selected source
has:

- missing pinned local checkout;
- source revision mismatch;
- static-only preflight failure;
- missing expected manifest evidence;
- ambiguous package-set topology;
- unreported carry-forward warning.

The static-only gate in P46-T2 must pass before P46-T3 can run the local
OpenAI-compatible provider.

## Boundary

P46-T1 does not run the pilot, run AI, clone or fetch repositories, install
dependencies, invoke package managers, execute harvested code, enable trusted
local adapter execution, accept packages or relations, publish registry
metadata, seed baselines, remove `preview_only`, persist raw prompts, persist
raw provider responses, persist secrets, or persist chain-of-thought.

The manifest does not treat AI output as registry truth and does not treat
adapter output as registry truth.
