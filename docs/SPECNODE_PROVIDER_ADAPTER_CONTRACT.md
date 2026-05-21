# SpecNode Provider Adapter Contract

Status: Phase 11 contract

This document defines the OpenAI-compatible provider adapter boundary for
future SpecNode-assisted candidate refinement.

The adapter boundary is local-provider infrastructure. It is not deterministic
evidence collection, not `refine-preview` planning, and not accepted registry
truth. SpecHarvester prepares deterministic artifacts. SpecNode owns provider
discovery, health checks, model listing, model execution policy, provenance, and
usage receipt generation.

## Contract Names

- `SpecNodeOpenAICompatibleProviderAdapter`: provider adapter contract for
  OpenAI-compatible local model servers.
- `SpecNodeProviderDiscoveryResult`: discovery output for configured and
  detected provider endpoints.
- `SpecNodeProviderHealth`: health-check result for one endpoint.
- `SpecNodeModelListing`: normalized model list returned by a provider.
- `SpecNodeGenerationPolicy`: timeout, retry, temperature, output-token, and
  prompt-budget policy for one model execution.
- `SpecNodeProviderUsageReceipt`: provider execution receipt embedded in the
  broader `usageReceipt` returned to SpecHarvester.

## Relationship to Existing Contracts

This contract fits after the deterministic preview plan:

```text
SpecHarvesterSpecNodeArtifactBundle
  -> SpecHarvesterRefinePreviewPlan
  -> SpecNodeRefinementJob
  -> SpecNodeOpenAICompatibleProviderAdapter
  -> candidatePatchProposal + usageReceipt, future
```

`SpecHarvesterSpecNodeArtifactBundle` and `SpecNodeRefinementJob` are defined
in [`SPECNODE_INTEGRATION_CONTRACT.md`](SPECNODE_INTEGRATION_CONTRACT.md).
`SpecHarvesterRefinePreviewPlan` is defined in
[`SPECNODE_REFINE_PREVIEW_CONTRACT.md`](SPECNODE_REFINE_PREVIEW_CONTRACT.md).

SpecHarvester does not contact providers. It may request provider metadata
through a typed SpecNode job or show a provider status supplied by SpecNode, but
provider discovery and model execution belong to SpecNode.

## Provider Adapter Shape

```json
{
  "schemaVersion": 1,
  "kind": "SpecNodeOpenAICompatibleProviderAdapter",
  "providerKind": "openai_compatible",
  "providerName": "lm_studio",
  "baseUrl": "http://127.0.0.1:1234",
  "endpointAllowlist": [
    "/v1/models",
    "/v1/chat/completions"
  ],
  "defaultHeaders": {
    "Content-Type": "application/json"
  },
  "authPolicy": {
    "mode": "none_or_local_token",
    "secretSource": "specnode_runtime_only",
    "redactHeaders": ["Authorization"]
  },
  "networkPolicy": {
    "scope": "localhost_only",
    "allowRemoteEndpoints": false,
    "modelNetworkAccess": "provider_only",
    "toolNetworkAccess": "none"
  },
  "generationPolicy": {
    "temperature": 0.2,
    "maxOutputTokens": 2048,
    "promptBudget": {
      "maxPromptTokens": 8192,
      "maxPromptBytes": 60000
    },
    "timeoutPolicy": {
      "connectTimeoutSeconds": 5,
      "readTimeoutSeconds": 120,
      "totalTimeoutSeconds": 180
    },
    "retryPolicy": {
      "maxAttempts": 2,
      "retryOnStatus": [408, 429, 500, 502, 503, 504],
      "backoff": "bounded_exponential",
      "maxBackoffSeconds": 5
    }
  },
  "authorityPolicy": {
    "modelFilesystemAccess": "none",
    "modelShellAccess": "none",
    "rawSourceAccess": "none",
    "secretAccess": "none",
    "allowedTools": [],
    "candidateMutation": "proposal_only"
  }
}
```

The exact schema can be implemented later. P11-T3 fixes the required meanings,
field names, and trust boundaries.

## LM Studio Discovery

LM Studio is the first local provider target because it exposes an
OpenAI-compatible API on a standard local port.

Default discovery candidates:

- `http://127.0.0.1:1234`
- `http://localhost:1234`

Discovery rules:

- SpecNode must prefer explicit operator configuration over auto-discovery.
- Auto-discovery is advisory and local only.
- The default mode is `localhost_only`.
- Remote base URLs require explicit operator opt-in and must not be inferred
  from repository content, harvested files, package metadata, or model output.
- Discovery must not read secrets from the harvested repository.
- Discovery must not execute repository code, package managers, tests, build
  tools, or shell commands.

## Endpoint Allowlist

The adapter may use only these OpenAI-compatible endpoints for this job class:

- `/v1/models`
- `/v1/chat/completions`

Endpoint joining rule: `baseUrl` is the provider origin without the OpenAI API
version path, and allowlisted endpoints are absolute API paths beginning with
`/v1/`. Implementations must join them by trimming exactly one slash between
`baseUrl` and the endpoint. For example,
`http://127.0.0.1:1234` + `/v1/models` becomes
`http://127.0.0.1:1234/v1/models`; `baseUrl` values ending in `/v1` must be
rejected or normalized before use.

Forbidden endpoints and behaviors:

- arbitrary URL fetches;
- provider-specific file upload APIs;
- tool or function calling endpoints for repository access;
- browser, search, crawling, or retrieval endpoints;
- model-requested endpoint expansion;
- streaming logs that expose raw prompts, secrets, or unredacted artifacts.

`modelNetworkAccess: provider_only` allows SpecNode to contact the configured
provider endpoint. It does not allow the model to browse repositories, fetch
dependencies, call external APIs, or request new network destinations.

## Health Checks

`SpecNodeProviderHealth` records whether an endpoint is reachable and compatible
enough for a refinement job.

```json
{
  "kind": "SpecNodeProviderHealth",
  "providerKind": "openai_compatible",
  "baseUrl": "http://127.0.0.1:1234",
  "checkedAt": "2026-05-21T00:00:00Z",
  "status": "healthy",
  "httpStatus": 200,
  "modelsEndpoint": "/v1/models",
  "chatCompletionsEndpoint": "/v1/chat/completions",
  "latencyMs": 42,
  "diagnostics": []
}
```

Health check statuses:

- `healthy`
- `unreachable`
- `unauthorized`
- `incompatible`
- `timeout`
- `error`

Health checks are runtime availability metadata, not deterministic package
evidence. They must not be written into candidate BoundarySpec evidence.

## Model Listing

`SpecNodeModelListing` normalizes `/v1/models` output without trusting model
names as capability claims.

```json
{
  "kind": "SpecNodeModelListing",
  "providerKind": "openai_compatible",
  "providerName": "lm_studio",
  "baseUrl": "http://127.0.0.1:1234",
  "retrievedAt": "2026-05-21T00:00:00Z",
  "models": [
    {
      "id": "local-model-id",
      "ownedBy": "local",
      "contextWindowTokens": null,
      "supportsChatCompletions": true
    }
  ]
}
```

Model listing rules:

- model IDs are runtime selection metadata only;
- model IDs must be recorded exactly in `usageReceipt` when used;
- SpecNode must not infer package capabilities from model names;
- SpecNode must reject jobs that name a model absent from the selected provider
  listing unless the operator explicitly allows stale listing behavior.

## Generation Policy

`SpecNodeGenerationPolicy` binds provider execution to predictable budgets.

Required fields:

- `temperature`
- `maxOutputTokens`
- `promptBudget.maxPromptTokens`
- `promptBudget.maxPromptBytes`
- `timeoutPolicy.connectTimeoutSeconds`
- `timeoutPolicy.readTimeoutSeconds`
- `timeoutPolicy.totalTimeoutSeconds`
- `retryPolicy.maxAttempts`
- `retryPolicy.retryOnStatus`
- `retryPolicy.backoff`

Policy rules:

- `temperature` should default to a low value such as `0.2` for reviewable
  refinement.
- `maxOutputTokens` must be lower than or equal to the job token budget.
- `promptBudget` must not exceed the `SpecHarvesterRefinePreviewPlan`
  `promptBudget`.
- Retries must replay the same compact deterministic input and must not add raw
  repository source, extra tools, or new endpoints.
- Timeouts and retries must be recorded in the provider usage receipt.

## Request Boundary

The provider request body may include only:

- model ID selected by SpecNode policy;
- bounded messages derived from `compactModelInput`;
- explicit output schema instructions for future `candidatePatchProposal`;
- `temperature`;
- `max_tokens` or OpenAI-compatible equivalent;
- no tool calls.

The request body must not include raw repository source, raw documentation
bodies, dependency directories, provider logs, local credentials, environment
dumps, SSH keys, access tokens, arbitrary prompts, or model-generated
instructions from previous runs.

## Usage Receipt

`SpecNodeProviderUsageReceipt` is embedded in the future `usageReceipt` output.
It records runtime provenance without making the model output authoritative.

Required receipt fields:

- `providerKind`
- `providerName`
- `baseUrl`
- `endpoint`
- `modelId`
- `requestId`
- `startedAt`
- `completedAt`
- `durationMs`
- `status`
- `attempts`
- `timeoutPolicy`
- `retryPolicy`
- `temperature`
- `maxOutputTokens`
- `promptBudget`
- `inputTokens`
- `outputTokens`
- `totalTokens`
- `finishReason`
- `responseSha256`
- `redactionPolicy`

The receipt must redact authorization headers and must not persist raw prompts,
raw model responses, secrets, or provider logs unless a later contract defines a
bounded redacted evidence artifact.

## Authority Policy

The provider adapter cannot expand model authority.

Required authority fields:

- `modelFilesystemAccess: none`
- `modelShellAccess: none`
- `rawSourceAccess: none`
- `secretAccess: none`
- `allowedTools: []`
- `candidateMutation: proposal_only`
- `modelNetworkAccess: provider_only`
- `toolNetworkAccess: none`

SpecHarvester does not contact providers. SpecNode may contact the configured
provider endpoint. The model may not call tools, run commands, inspect the
filesystem, request secrets, perform network fetches, install dependencies,
browse repositories, or write candidate files.

## Rejection Conditions

SpecNode must reject provider execution when:

- the provider base URL is not explicit or locally discovered under policy;
- the base URL is outside `localhost_only` mode without operator opt-in;
- the requested endpoint is not in `endpointAllowlist`;
- `/v1/models` fails and no explicit model override policy allows proceeding;
- the requested model ID is absent from the listing;
- health status is `unreachable`, `unauthorized`, `incompatible`, `timeout`, or
  `error`;
- `temperature`, `maxOutputTokens`, timeout, retry, or prompt-budget fields are
  missing;
- `promptBudget` exceeds the preview plan budget;
- request content includes excluded raw source, documentation bodies, secrets,
  provider logs, dependency directories, or arbitrary prompts;
- policy grants shell, filesystem, tools, raw-source, secret, or network
  expansion authority.

## Non-Goals

P11-T3 does not implement an HTTP client, call LM Studio, execute models, define
the final `candidatePatchProposal` schema, or add real provider smoke coverage.
Those are later implementation tasks.
P11-T4 defines the schema-validated patch proposal output boundary in
[`SPECNODE_PATCH_PROPOSAL_CONTRACT.md`](SPECNODE_PATCH_PROPOSAL_CONTRACT.md).

## Review Rule

A provider adapter configuration is safe for future SpecNode refinement only
when it is explicit, local by default, endpoint-allowlisted, budgeted,
receipted, and unable to expand model authority beyond `provider_only` network
access.
