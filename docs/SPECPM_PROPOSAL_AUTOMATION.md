# SpecPM Proposal Automation

Status: Trusted workflow design

SpecHarvester can open proposal PRs in the SpecPM repository after a candidate
has been generated, validated, and promoted into a SpecPM accepted source diff.

This automation is intentionally a proposal mechanism. It does not publish
directly to the public registry.

```text
SpecHarvester candidate
        |
        v
SpecHarvester validation and promotion
        |
        v
trusted proposal workflow
        |
        v
PR in 0al-spec/SpecPM
        |
        v
SpecPM CI and maintainer review
        |
        v
merge to SpecPM main
        |
        v
GitHub Pages /v0 publication
```

## Workflow

The workflow is:

```text
.github/workflows/propose-to-specpm.yml
```

It can run in two trusted modes:

- manual `workflow_dispatch`;
- `workflow_run` after `CI` succeeds on `main`, only when explicitly enabled
  with a repository variable.

It must not run with write credentials on ordinary `pull_request` events.

For review safety, manifest-path decisions can be prepared from the reviewed
candidate using `prepare-accepted-entry` before running proposal automation.

## Preflight Validation

The trusted proposal run performs explicit preflight checks before cross-repository
proposal writes:

- candidate directory existence;
- candidate validation with `python -m specpm.cli validate <candidate_dir> --json`;
- producer bundle preflight with
  `python -m spec_harvester preflight-candidate-bundle <candidate_dir>`;
- static viewer rendering with
  `python -m spec_harvester render-spec-site --candidate <candidate_dir>`;
- metadata identity check:
  - `specpm.yaml` `metadata.id` must match `package_id`;
  - `specpm.yaml` `metadata.version` must match `package_version`;
- symlink rejection for candidate `specpm.yaml` input paths.

The workflow uploads the producer preflight report and static viewer as a
workflow artifact. When it opens a SpecPM pull request, the PR body links the
evidence required by the SpecPM producer bundle intake checklist:

- accepted source bundle path in the SpecPM diff;
- `specpm.yaml`;
- `producer-receipt.json`;
- `validation-report.json`;
- `diagnostics.json`;
- producer preflight report artifact;
- static viewer artifact;
- accepted-source diff in the pull request.

These links are review evidence only. They do not make the candidate accepted,
published, signed, installed, or trusted.

The stable producer evidence roles and expected inputs for a future optional
SpecPM CI preflight gate are documented in
[`SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md`](SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md).
That gate may consume proposal evidence, but it must not replace maintainer
review or turn producer-side preflight into registry acceptance.

Proposal bodies should also include a machine-readable
`registryAcceptanceDecision` reference with `status: external_required`. The
external decision record boundary is documented in
[`SPECPM_REGISTRY_ACCEPTANCE_DECISION.md`](SPECPM_REGISTRY_ACCEPTANCE_DECISION.md).
The reference tells SpecPM consumers where acceptance authority lives without
claiming approval from generated producer output.

## Package-Set Handoff Dry Run

Package-set proposal automation is intentionally narrower than single-package
proposal automation in P26-T2. Use `proposal_kind: package_set` to generate and
upload package-set handoff evidence from a trusted workflow run:

```text
proposal_kind: package_set
package_set_bundle_dir: .smoke/xyflow-package-set/package-set
package_set_viewer_dir: "" # optional; default smoke run uses .smoke/xyflow-package-set/viewer
create_pr=false
```

When `package_set_bundle_dir` keeps the default
`.smoke/xyflow-package-set/package-set` and the directory is absent on the
fresh GitHub runner, the trusted workflow generates it with
`xyflow-package-set-smoke` before building the handoff artifact. Custom
`package_set_bundle_dir` values must point at committed or downloaded
artifacts.

The workflow runs the package-set handoff command:

```bash
python3 -m spec_harvester package-set-handoff-proposal \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --viewer .smoke/xyflow-package-set/viewer \
  --output .smoke/xyflow-package-set/handoff/proposal.json \
  --proposal-body .smoke/xyflow-package-set/handoff/proposal.md
```

That artifact records `SpecHarvesterPackageSetHandoffProposal`,
`spec-harvester.package-set-handoff-proposal/v0`, member package evidence
links, package relation proposals, `bundle-set-preflight` status, static viewer
links, and `registryAcceptanceDecision.status: external_required`. It is still
review evidence only; it does not accept packages or relations. See
[`PACKAGE_SET_HANDOFF_PROPOSAL.md`](PACKAGE_SET_HANDOFF_PROPOSAL.md).

Package-set proposal intake expectations are recorded in
[`PACKAGE_SET_PROPOSAL_INTAKE_CHECKLIST.md`](PACKAGE_SET_PROPOSAL_INTAKE_CHECKLIST.md).
They define the required evidence roles before maintainers accept package
members or relations.

Package-set mode uploads a `specpm-package-set-proposal-evidence-*` workflow
artifact containing:

- `package-set-handoff-proposal.json`
- `package-set-handoff-proposal.md`

It does not promote files into the SpecPM checkout, does not use
`SPECPM_PROPOSAL_TOKEN`, and does not create a SpecPM PR. This keeps generated
package-set handoff evidence available to maintainers without granting
cross-repository write credentials to untrusted pull request events or treating
producer output as registry acceptance.

After promotion, the workflow runs `specpm public-index generate` and validates the
resulting SpecPM diff scope. Allowed changed paths are:

- `public-index/generated/<packageId>/<packageVersion>/*`
- `public-index/accepted-packages.yml`

Any other changed path causes immediate failure.

## Required Secret

To create a PR in SpecPM, configure:

```text
SPECPM_PROPOSAL_TOKEN
```

The token should be a GitHub App installation token or a fine-scoped token with
write access to `0al-spec/SpecPM`.

Recommended scope:

```text
Contents: read/write on 0al-spec/SpecPM
Pull requests: read/write on 0al-spec/SpecPM
Metadata: read
```

Do not use a broad personal token if a GitHub App token is available.

## Optional Variables

Automatic proposal after green CI on `main` is disabled by default.

To enable it, set:

```text
SPECHARVESTER_AUTO_PROPOSE_TO_SPECPM=true
```

Optional defaults for workflow-run mode:

```text
SPECHARVESTER_CANDIDATE_DIR=candidates/github.com/xyflow/xyflow
SPECHARVESTER_PACKAGE_ID=xyflow.core
SPECHARVESTER_PACKAGE_VERSION=0.1.0
```

Manual `workflow_dispatch` inputs override these values.

## Manual Dry Run

Run the workflow manually with:

```text
create_pr=false
```

The workflow will:

- check out SpecHarvester;
- check out SpecPM;
- install both packages;
- validate the candidate with SpecPM;
- run producer bundle preflight and upload the preflight report as workflow
  evidence;
- render the static viewer and upload it as workflow evidence;
- promote the candidate into the SpecPM checkout;
- run `specpm public-index generate`;
- print the SpecPM diff.

It will not push a branch or create a PR.

Troubleshooting notes:

- Identity mismatch: verify `candidates/<pkg>/specpm.yaml` metadata against workflow
  inputs before running proposal.
- No changes: candidate promotion is deterministic; review upstream expected effects
  and re-run after `prepare-accepted-entry` if manifest path was absent.
- Scope failure: the changed files were outside `public-index/generated/<id>/<ver>`
  and `public-index/accepted-packages.yml`.
- Symlink validation failure: copy candidate content to a normal path and avoid
  symlinked manifest inputs.

## Manual PR Creation

Run the workflow manually with:

```text
create_pr=true
```

The workflow will additionally:

- create a branch in `0al-spec/SpecPM`;
- commit the promoted accepted source diff;
- push the branch using `SPECPM_PROPOSAL_TOKEN`;
- open a PR against SpecPM `main` with producer bundle evidence links in the
  body.

## Security Boundary

The split is deliberate:

```text
CI validates.
Proposal workflow writes only from trusted context.
SpecPM maintainers accept.
```

The proposal workflow does not run with cross-repository write credentials for
untrusted pull requests.

If SpecHarvester is compromised or generates a bad candidate, the result is
still only a SpecPM PR. The package becomes registry input only after SpecPM
review and merge.

## Accepted Package Update Lifecycle

The accepted package lifecycle keeps SpecPM path versions immutable. Proposal
automation should therefore submit updates as new accepted version paths rather
than replacing prior version paths.

A stable update record should include:

- `sourceRevision`: pinned upstream revision used for candidate generation;
- `evidenceDigests`: digests for `harvest.json` and other promoted evidence artifacts;
- `oldPackageVersion` / `newPackageVersion`;
- `changedClaims`: a list of materially changed intent/capability/scope claims;
- `validationStatus`: candidate validation and governance smoke outcomes;
- `reviewerNotes`: rationale and risk notes for this update.

When the update is only metadata correction:

- preserve `sourceRevision` if applicable;
- still create a new accepted package version path;
- document why this is metadata-only to avoid confusing upstream content changes
  with editorial errata.

## Maintainer Review

SpecPM maintainers should still review:

- package ID and namespace;
- capability IDs;
- observed `intent.*` IDs;
- source provenance;
- license metadata;
- scope and evidence quality;
- public-index impact.

Automation proposes. SpecPM accepts.
