# Trusted Classifier Evaluation

SpecHarvester may use established classifiers and metadata tools in future
analyzer phases, but `collect-local` does not execute them. The
`classifierPolicy` record in `harvest.json` documents the allowed integration
boundary: default mode is disabled, execution is none, no network is allowed,
no package scripts are run, and there is no harvested dependency installation.

External classifier output is advisory untrusted metadata. It may enrich review
evidence, but it does not override manifest-first `ProjectProfile` evidence.

## Policy Contract

The default `classifierPolicy` requires:

- `inputAuthority: untrusted_repository_content`
- `outputAuthority: advisory_untrusted_metadata`
- `defaultMode: disabled`
- `allowedExecutions: ["none"]`
- `networkAccess: none`
- `packageScripts: not_run`
- pinned tool version for any future optional adapter
- classifier id, classifier version, source revision, output digest, and source
  digest evidence
- source digest evidence for every accepted classifier observation
- `manifestEvidencePrecedence: manifest_first`

The adapter contract accepts observations such as language, vendored file,
generated file, package, license, symbol, and syntax node metadata. Those
observations remain evidence for human review, not package authority.

`harvest.json` stores only a compact registry summary so classifier governance
does not inflate routine prompt context. The full reviewed registry remains in
`spec_harvester.classifier_registry`.

## Registry Decisions

| Tool | Status | Use | License note | Decision |
| --- | --- | --- | --- | --- |
| GitHub Linguist | `approved_optional` | language classification, vendored/generated filtering | MIT core repository; bundled grammars need upstream license awareness | Good reference-compatible source, but not required by default. |
| go-enry | `approved_optional` | Linguist-compatible classification and vendored/generated filtering | Apache-2.0 | Preferred future adapter candidate because it can be pinned as a Go module or CLI without Ruby setup. |
| Syft | `approved_optional` | package cataloging and SBOM-like dependency evidence | Apache-2.0 | Useful for local directory package inventory when pinned and sandboxed. |
| ScanCode Toolkit | `deferred` | license, copyright, package, and provenance evidence | `NOASSERTION`; repository includes Apache-2.0 and CC-BY-4.0 materials, datasets and bundled materials need secondary review | Deferred until runtime cost and license-data provenance are reviewed. |
| Universal Ctags | `deferred` | broad symbol extraction | GPL-2.0 CLI boundary needs review | Deferred until JSON Lines output, parser variance, and distribution constraints are resolved. |
| Tree-sitter | `deferred` | syntax indexing and AST extraction | MIT core; each grammar needs license review | Deferred here because AST ingestion belongs to later language-neutral analyzer work. |

## Execution Boundary

Future optional adapters must:

- run only against the already-collected local checkout;
- avoid package managers, dependency installers, build systems, and tests from
  the harvested repository;
- disable or avoid networked targets;
- record the exact tool identity, pinned version, source revision, input file
  digests, and output digest;
- emit deterministic, sorted, schema-versioned output;
- fail closed to manifest-first evidence when the tool is unavailable.

This means a missing classifier cannot make a harvest fail. It only removes an
optional advisory enrichment path.

## Source References

- GitHub Linguist: <https://github.com/github-linguist/linguist>
- go-enry: <https://github.com/go-enry/go-enry>
- Syft: <https://github.com/anchore/syft>
- ScanCode Toolkit: <https://github.com/aboutcode-org/scancode-toolkit>
- Universal Ctags: <https://github.com/universal-ctags/ctags>
- Tree-sitter: <https://github.com/tree-sitter/tree-sitter>

## References

- `docs/TRUSTED_CLASSIFIER_EVALUATION.md`
- <doc:TrustBoundary>
- <doc:AnalyzerSandboxRequirements>
- <doc:TreeSitterEvaluation>
