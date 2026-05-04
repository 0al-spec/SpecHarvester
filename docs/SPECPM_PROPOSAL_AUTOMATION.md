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
- promote the candidate into the SpecPM checkout;
- run `specpm public-index generate`;
- print the SpecPM diff.

It will not push a branch or create a PR.

## Manual PR Creation

Run the workflow manually with:

```text
create_pr=true
```

The workflow will additionally:

- create a branch in `0al-spec/SpecPM`;
- commit the promoted accepted source diff;
- push the branch using `SPECPM_PROPOSAL_TOKEN`;
- open a PR against SpecPM `main`.

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
