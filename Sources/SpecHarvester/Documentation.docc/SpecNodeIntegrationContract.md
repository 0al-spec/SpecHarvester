# SpecNode Integration Contract

SpecHarvester may later ask SpecNode to refine generated candidates with a local
model. This contract defines that boundary before any provider adapter or
refinement command exists.

SpecHarvester remains the deterministic evidence producer. SpecNode owns
provider discovery, model execution, typed job policy, provenance, and
`usageReceipt` generation. Model output is untrusted proposal metadata until
SpecHarvester validates it and a human reviewer accepts it.

## Contract Names

- `SpecHarvesterSpecNodeArtifactBundle`: deterministic artifact bundle for one
  candidate refinement job.
- `SpecNodeRefinementJob`: typed job envelope sent to SpecNode.
- `candidatePatchProposal`: future schema-validated model output containing
  proposed candidate changes.
- `usageReceipt`: future SpecNode output with provider/model identity, token
  usage, timing, and policy metadata.

## Ownership

SpecHarvester owns static evidence collection, deterministic drafting,
`ProjectProfile`, optional `PublicInterfaceIndex`, validation reports,
governance reports, smoke triage reports, bundle assembly, output validation,
SpecPM validation, and human review gates.

SpecNode owns provider discovery, provider health checks, model execution,
timeout, retry, token-budget, temperature, provenance, and `usageReceipt`
generation.

The model owns no authority. It cannot run shell commands, mutate files, read
secrets, read raw repository source, install dependencies, run package scripts,
or expand network access.

Explicitly: the model cannot read secrets or read raw repository source outside
the typed artifact bundle.

## Artifact Bundle

`SpecHarvesterSpecNodeArtifactBundle` references candidate workspace files by
relative path and records content digests for every included artifact.

```json
{
  "schemaVersion": 1,
  "kind": "SpecHarvesterSpecNodeArtifactBundle",
  "candidateId": "flask.core",
  "candidateVersion": "0.1.0",
  "workspaceRoot": ".",
  "source": {
    "repository": "https://github.com/pallets/flask",
    "revision": "0123456789abcdef0123456789abcdef01234567"
  },
  "artifacts": [
    {
      "id": "harvest_snapshot",
      "path": "harvest.json",
      "required": true,
      "sha256": "64-hex-digest"
    },
    {
      "id": "spec_package_manifest",
      "path": "specpm.yaml",
      "required": true,
      "sha256": "64-hex-digest"
    }
  ],
  "policy": {
    "rawSourceAccess": "none",
    "secretAccess": "none",
    "modelFilesystemAccess": "none",
    "modelShellAccess": "none",
    "candidateMutation": "proposal_only"
  }
}
```

Required artifacts are `harvest.json`, `specpm.yaml`, and every referenced
`specs/*.spec.yaml`.

Optional artifacts include `public-interface-index.json`,
`batch-validation.json`, `governance-claims.json`, `namespace-upstream.json`,
`license-provenance.json`, `smoke-triage.json`, accepted-candidate diff
reports, accepted-candidate impact classification reports, and accepted package
update proposal metadata.

Forbidden artifacts include raw repository source trees, `.git/` content,
package manager caches, dependency directories, local secrets, credentials,
private configuration, SSH keys, tokens, and environment dumps.

## Bundle Validation

SpecHarvester must reject the bundle before handoff unless every artifact path
is relative, inside the candidate workspace, not a symlink, and digest-checked
with SHA-256. Required artifacts must exist. `harvest.json` must have
`kind: SpecHarvesterEvidenceSnapshot`.

The policy must declare `modelFilesystemAccess: none`,
`modelShellAccess: none`, `candidateMutation: proposal_only`,
`rawSourceAccess: none`, and `secretAccess: none`.

## Typed Job

`SpecNodeRefinementJob` is the only message SpecHarvester sends to SpecNode for
candidate refinement.

```json
{
  "schemaVersion": 1,
  "kind": "SpecNodeRefinementJob",
  "jobId": "01HY0000000000000000000000",
  "createdAt": "2026-05-21T00:00:00Z",
  "producer": {
    "name": "SpecHarvester",
    "version": "0.1.0"
  },
  "bundle": {
    "kind": "SpecHarvesterSpecNodeArtifactBundle",
    "digest": "sha256:64-hex-digest"
  },
  "policy": {
    "modelFilesystemAccess": "none",
    "modelShellAccess": "none",
    "modelNetworkAccess": "provider_only",
    "allowedTools": [],
    "candidateMutation": "proposal_only",
    "temperature": 0.2,
    "tokenBudget": 8192,
    "timeoutSeconds": 120
  },
  "requestedOutputs": [
    "candidatePatchProposal",
    "reviewNotes",
    "rejectionReason",
    "usageReceipt"
  ]
}
```

`modelFilesystemAccess: none` means the model receives serialized artifact
content through SpecNode only. `modelShellAccess: none` means the model cannot
invoke shell commands, package managers, tests, build tools, or analyzers.
`modelNetworkAccess: provider_only` means SpecNode may contact the configured
model provider, but the model cannot request new network fetches or browse
upstream repositories. `allowedTools: []` exposes no LLM tool calls.
`candidateMutation: proposal_only` means SpecNode returns proposed edits as
data and cannot write candidate files directly.

## Output Authority

Allowed output kinds are `candidatePatchProposal`, `reviewNotes`,
`rejectionReason`, and `usageReceipt`. Later tasks define their final schemas.

SpecNode cannot directly write `specpm.yaml`, write `specs/*.spec.yaml`,
promote into accepted source, publish to SpecPM, run Git, run shell commands,
install dependencies, run tests, run build tools, or treat model assertions as
accepted registry truth.

SpecHarvester validates returned proposal metadata, shows it for review, and
reruns SpecPM validation after any accepted local edit.

## Rejection Conditions

Reject the handoff or returned proposal if bundle digests do not match, paths
are absolute, symlinked, or outside the workspace, forbidden artifacts are
present, policy does not preserve no shell and no filesystem access, output
contains direct file writes, output references missing artifacts, output asks to
run commands or fetch dependencies, or the future `usageReceipt` is missing.

## References

- `docs/SPECNODE_INTEGRATION_CONTRACT.md`
- <doc:HarvesterArchitecture>
- <doc:TrustBoundary>
- <doc:Workflow>
