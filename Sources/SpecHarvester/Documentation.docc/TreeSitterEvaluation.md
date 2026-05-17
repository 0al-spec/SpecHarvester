# Tree-sitter Evaluation

Status: Proposed decision

SpecHarvester should use Tree-sitter as an optional shared syntax-index backend
for future analyzers, not as an immediate replacement for the current Python
`ast` analyzer or JavaScript/TypeScript manifest/export analyzer.

## Decision

Tree-sitter should complement current analyzers.

It is a good candidate for a future syntax layer because it provides concrete
syntax trees, query captures, error-node visibility, and broad language
coverage. It should not become the default public interface extraction layer
until parser packaging, ABI compatibility, query versioning, and analyzer cache
policy are explicit.

## Trust Boundary

Allowed:

- Read pinned local source bytes.
- Parse bytes with a pinned Tree-sitter parser.
- Run pinned query text.
- Record captures, byte ranges, file digests, versions, and diagnostics.

Forbidden:

- Execute harvested repository code.
- Install harvested dependencies.
- Run package managers, package scripts, tests, build tools, or language
  servers from harvested repositories.
- Load parser grammars from harvested repositories.
- Treat syntax captures as runtime truth.

## Recommended Shape

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

The normalized syntax index should contain stable captures, source evidence,
parser/query metadata, byte ranges, row/column spans, and parser diagnostics.
It should not store raw full trees in candidate artifacts by default.

## Current Analyzer Relationship

Keep `python-ast-public-api` as the default Python analyzer because it uses the
standard library and already provides language-aware signatures without
external parser packaging.

Keep `js-ts-manifest-export-analyzer` as the default JavaScript/TypeScript
entrypoint analyzer because manifest interpretation is outside Tree-sitter's
scope. Tree-sitter can later improve static export extraction after parser
packaging is settled.

## Recommendation

Do not add a Tree-sitter runtime dependency in P1-T4.

Use P1-T5 to integrate current public interface evidence into deterministic
drafting. Add a later optional pilot for one Tree-sitter-backed `SyntaxIndex`
provider with pinned parser packages, query hashes, diagnostics for `ERROR` and
`MISSING` nodes, and no execution/network/package-script access.

The full GitHub-facing decision record is
`docs/TREE_SITTER_EVALUATION.md`.
