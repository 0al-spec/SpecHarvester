# SpecNode Provider Adapter Contract

This page mirrors the GitHub provider adapter contract for future
SpecNode-assisted candidate refinement.

The adapter boundary is local-provider infrastructure. SpecHarvester prepares
deterministic artifacts; SpecNode owns provider discovery, health checks, model
listing, model execution policy, provenance, and usage receipt generation.
SpecHarvester does not contact providers.

## Contract Names

- `SpecNodeOpenAICompatibleProviderAdapter`: OpenAI-compatible local provider
  adapter contract.
- `SpecNodeProviderDiscoveryResult`: configured or discovered endpoint result.
- `SpecNodeProviderHealth`: endpoint health-check result.
- `SpecNodeModelListing`: normalized `/v1/models` output.
- `SpecNodeGenerationPolicy`: timeout, retry, temperature, output-token, and
  prompt-budget policy.
- `SpecNodeProviderUsageReceipt`: provider execution receipt embedded in
  `usageReceipt`.

## Adapter Shape

```json
{
  "schemaVersion": 1,
  "kind": "SpecNodeOpenAICompatibleProviderAdapter",
  "providerKind": "openai_compatible",
  "providerName": "lm_studio",
  "baseUrl": "http://127.0.0.1:1234",
  "endpointAllowlist": ["/v1/models", "/v1/chat/completions"],
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

## LM Studio Discovery

Default LM Studio discovery candidates are `http://127.0.0.1:1234` and
`http://localhost:1234`.

Rules:

- explicit operator configuration wins over auto-discovery;
- auto-discovery is advisory and local only;
- default mode is `localhost_only`;
- remote base URLs require explicit operator opt-in;
- discovery must not execute repository code or shell commands;
- discovery must not read secrets from harvested repositories.

## Endpoint Allowlist

The adapter may use only `/v1/models` and `/v1/chat/completions`.

Endpoint joining rule: `baseUrl` is the provider origin without the OpenAI API
version path, and allowlisted endpoints are absolute API paths beginning with
`/v1/`. Implementations must join them by trimming exactly one slash between
`baseUrl` and the endpoint. For example,
`http://127.0.0.1:1234` + `/v1/models` becomes
`http://127.0.0.1:1234/v1/models`; `baseUrl` values ending in `/v1` must be
rejected or normalized before use.

`modelNetworkAccess: provider_only` allows SpecNode to contact the configured
provider endpoint. It does not allow the model to browse repositories, fetch
dependencies, call external APIs, or request new network destinations.

## Health and Model Listing

`SpecNodeProviderHealth` records endpoint status such as `healthy`,
`unreachable`, `unauthorized`, `incompatible`, `timeout`, or `error`.

`SpecNodeModelListing` normalizes `/v1/models` output. Model IDs are runtime
selection metadata only, must be recorded in `usageReceipt`, and must not be
treated as package capability claims.

## Generation Policy

`SpecNodeGenerationPolicy` must include `temperature`, `maxOutputTokens`,
`promptBudget`, `timeoutPolicy`, and `retryPolicy`.

Retries must replay the same compact deterministic input and must not add raw
repository source, tools, or endpoints. The `promptBudget` must not exceed the
`SpecHarvesterRefinePreviewPlan` budget.

Provider requests and receipts must not include raw repository source, raw
documentation bodies, secrets, dependency directories, or provider logs.

## Usage Receipt

`SpecNodeProviderUsageReceipt` records `providerKind`, `providerName`,
`baseUrl`, `endpoint`, `modelId`, `requestId`, `startedAt`, `completedAt`,
`durationMs`, `status`, `attempts`, `timeoutPolicy`, `retryPolicy`,
`temperature`, `maxOutputTokens`, `promptBudget`, `inputTokens`,
`outputTokens`, `totalTokens`, `finishReason`, `responseSha256`, and
`redactionPolicy`.

The receipt must redact authorization headers and must not persist raw prompts,
raw model responses, secrets, or provider logs unless a later contract defines a
bounded redacted evidence artifact.

## Authority Policy

The provider adapter cannot expand model authority:

- `modelFilesystemAccess: none`
- `modelShellAccess: none`
- `rawSourceAccess: none`
- `secretAccess: none`
- `allowedTools: []`
- `candidateMutation: proposal_only`
- `modelNetworkAccess: provider_only`
- `toolNetworkAccess: none`

SpecNode may contact the configured provider endpoint. The model may not call
tools, run commands, inspect the filesystem, request secrets, perform network
fetches, install dependencies, browse repositories, or write candidate files.

## Rejection Conditions

Reject provider execution when the base URL is not explicit or locally
discovered under policy, the endpoint is outside `endpointAllowlist`,
`/v1/models` fails without an override policy, the requested model is absent,
health is not usable, policy fields are missing, `promptBudget` exceeds the
preview plan budget, request content includes excluded raw content, or policy
grants shell, filesystem, tool, raw-source, secret, or network-expansion
authority.

Schema-validated patch proposal output is defined separately in
<doc:SpecNodePatchProposalContract>.

Local in-process SpecNode-compatible provider smoke coverage is defined in
<doc:SpecNodeProviderSmokeCoverage>. That smoke coverage does not call LM
Studio or make SpecHarvester own provider execution.

## References

- `docs/SPECNODE_PROVIDER_ADAPTER_CONTRACT.md`
- <doc:SpecNodeIntegrationContract>
- <doc:SpecNodeRefinePreviewContract>
- <doc:SpecNodePatchProposalContract>
- <doc:SpecNodeProviderSmokeCoverage>
- <doc:Workflow>
- <doc:TrustBoundary>
