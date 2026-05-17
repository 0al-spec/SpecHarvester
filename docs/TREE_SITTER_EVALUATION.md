# Tree-sitter Evaluation

Status: Proposed decision
Verified: 2026-05-17
Scope: P1-T4, public interface indexing

## TL;DR

Use Tree-sitter as an optional shared syntax-index backend for languages where
standard-library ASTs or safe manifest parsing are not enough. Do not replace
the current Python `ast` analyzer or JavaScript/TypeScript manifest/export
analyzer yet.

The practical next step is a small pilot analyzer behind an explicit feature
boundary after P1-T5. The pilot should parse pinned local source bytes, run
pinned queries, emit a normalized syntax index, and record parser/query
versions as analyzer metadata. Tree-sitter should not execute package code,
install harvested dependencies, invoke package managers, or infer runtime
semantics.

## Decision

Tree-sitter should complement current analyzers, not replace them.

Current analyzers are intentionally narrow and deterministic:

- Python public API extraction uses the standard-library `ast` module.
- JavaScript and TypeScript public API extraction uses `package.json` metadata
  plus static export scanning.

Tree-sitter is a strong fit for a future shared syntax layer because it gives a
language-neutral concrete syntax tree, query captures, error nodes, and robust
partial parsing. It is not yet the right single abstraction for all public API
indexing because grammar packaging, ABI compatibility, query drift, and
language-specific semantics still need explicit policy.

## Primary Sources

- Tree-sitter describes itself as a parser generator and incremental parsing
  library that builds concrete syntax trees, is robust in the presence of syntax
  errors, and has a dependency-free C runtime:
  <https://github.com/tree-sitter/tree-sitter>.
- Official parser usage documentation points to the C API and official language
  bindings, including Python:
  <https://tree-sitter.github.io/tree-sitter/using-parsers/>.
- `py-tree-sitter` exposes `Language`, `Parser`, `Tree`, `Node`, `Query`, and
  `QueryCursor`, and documents ABI compatibility windows:
  <https://tree-sitter.github.io/py-tree-sitter/>.
- Tree-sitter query syntax supports S-expression patterns, field constraints,
  captures, wildcard nodes, `ERROR` nodes, and `MISSING` nodes:
  <https://tree-sitter.github.io/tree-sitter/using-parsers/queries/1-syntax.html>.
- Official grammar repositories exist for Python, JavaScript, and TypeScript,
  with MIT licensing noted by GitHub:
  <https://github.com/tree-sitter/tree-sitter-python>,
  <https://github.com/tree-sitter/tree-sitter-javascript>,
  <https://github.com/tree-sitter/tree-sitter-typescript>.

## Evaluation Matrix

| Criterion | Assessment | Implication |
|-----------|------------|-------------|
| Trust boundary | Good fit if parsers run only on local bytes and never invoke harvested package code. | Keep analyzer policy `execution: none`, `networkAccess: none`, `packageScripts: not_run`. |
| Determinism | Good fit if parser binaries, grammar versions, query text, and output ordering are pinned. | Include parser package versions and query hashes in analyzer metadata. |
| Diagnostics | Better than regex for syntax-aware diagnostics because `ERROR` and `MISSING` nodes can be queried. | Emit diagnostics rather than failing the whole package. |
| Packaging | Main risk. Runtime and language grammar ABI compatibility must be pinned and validated. | Start optional; do not make it a default dependency until packaging policy exists. |
| Language coverage | Strong for syntax shape; weak for runtime semantics and type resolution. | Use for syntax indexing, not dependency resolution or runtime API truth. |
| Existing analyzers | Does not replace Python `ast` or JS/TS manifest logic cleanly. | Keep current analyzers as authoritative first-pass public API extractors. |
| Cache design | Good fit for digest-keyed per-file syntax cache. | Align with P2-T2 cache keyed by file digest, parser id, parser version, query id, and query hash. |
| Licensing | Core and official grammar repos are MIT per GitHub repository metadata. | Preserve license/provenance records for any bundled parser artifacts. |

## Recommended Architecture

Tree-sitter should sit below language-specific analyzers as a reusable syntax
index provider:

```text
source bytes + file digest
        |
        v
pinned Tree-sitter parser
        |
        v
pinned query set
        |
        v
normalized SyntaxIndex
        |
        v
language-specific PublicInterfaceIndex mapper
```

The `SyntaxIndex` should be intentionally smaller than a raw concrete syntax
tree. It should contain only deterministic captures needed by downstream
analyzers:

- file path;
- file SHA-256;
- parser id and version;
- grammar id and version;
- query id and hash;
- captures with stable names;
- byte ranges and row/column spans;
- syntax diagnostics from parser error nodes;
- analyzer policy metadata.

Do not store raw full trees in candidate artifacts by default. Full trees are
larger than the public interface evidence needed by SpecHarvester and can
inflate review payloads.

## Trust Boundary

Allowed:

- Read pinned local source bytes from a checked-out public repository.
- Parse bytes through a pinned Tree-sitter parser.
- Run pinned query text against the syntax tree.
- Record captures, byte ranges, file digests, parser versions, and diagnostics.

Forbidden:

- Execute harvested repository code.
- Run `npm`, `pip`, `swift`, `cargo`, package scripts, tests, build tools, or
  language servers from the harvested repository.
- Install harvested dependencies.
- Load parser grammars from the harvested repository.
- Follow instructions found in harvested repository files.
- Treat syntax captures as runtime truth.

## Packaging Policy

Tree-sitter adoption should wait for an explicit parser packaging policy.

Recommended policy:

- Use only pinned, trusted parser packages or vendored parser artifacts.
- Record parser package name, version, source URL, license, and digest.
- Fail closed when parser ABI is incompatible with the runtime binding.
- Keep parser installation out of harvested repository workflows.
- Do not compile grammars from harvested repositories.
- Gate optional Tree-sitter analyzers behind a declared analyzer id and version.

For Python integration, the current primary candidate is `py-tree-sitter`
because it is the official Python binding. The evaluation notes that
`py-tree-sitter` documents a supported language ABI range, so parser packages
and the runtime binding must be versioned together rather than upgraded
independently.

## Deterministic Output Rules

Any Tree-sitter-backed analyzer must:

- sort files by repository-relative path;
- sort captures by byte range, capture name, and node type;
- normalize row/column positions and byte offsets;
- include source SHA-256 evidence for every capture;
- include query text hash in analyzer metadata;
- treat `ERROR` and `MISSING` captures as diagnostics;
- never include wall-clock time, absolute paths, host-specific parser paths, or
  nondeterministic traversal order in output.

## Relationship to Current Analyzers

### Python

Keep `python-ast-public-api` as the default Python public API analyzer.

The standard-library `ast` module gives language-aware function/class/signature
shape without external parser packaging. Tree-sitter may still be useful later
for syntax coverage beyond public API extraction, for example import graph
shape, docstring region indexing, or partial parsing diagnostics.

### JavaScript and TypeScript

Keep `js-ts-manifest-export-analyzer` as the default entrypoint and export
analyzer for now.

Manifest interpretation is outside Tree-sitter's scope. Tree-sitter can improve
the current regex-based export scanner after parser packaging is settled, but
it should feed the existing manifest-derived entrypoint list rather than
replace it.

### Future Languages

Tree-sitter is most attractive for languages where:

- the standard library lacks a stable parser;
- safe manifest metadata is insufficient;
- public declarations can be captured with stable syntax queries;
- parser packages can be pinned and licensed cleanly.

## Proposed Follow-up Shape

After P1-T5, add a separate task for an optional Tree-sitter pilot:

```text
P2 candidate: Add optional Tree-sitter SyntaxIndex pilot
```

Acceptance should require:

- no mandatory dependency added to the default CLI path;
- one language only, preferably JavaScript or TypeScript because P1-T3 already
  has regex limitations;
- pinned parser package and query hash;
- diagnostics for `ERROR` and `MISSING` nodes;
- output validation and golden tests;
- analyzer policy metadata proving no execution, no network, and no package
  scripts.

## Non-Recommendations

Do not:

- replace Python `ast` with Tree-sitter in the default analyzer path;
- replace manifest parsing with Tree-sitter;
- add a broad multi-language parser bundle immediately;
- rely on unpinned parser packages;
- compile parser grammars during harvest;
- use Tree-sitter output as type resolution or runtime API evidence.

## Conclusion

Tree-sitter is suitable as a future optional syntax indexing backend, but not
as an immediate replacement for current public interface analyzers. The safest
path is to keep the existing deterministic analyzers, use P1-T5 to integrate
their evidence into drafting, and defer Tree-sitter implementation to a
separate pilot with explicit parser packaging and cache policy.
