# Rowpick: Fictional Command Documentation

This is a synthetic teaching source, licensed MIT by 0AL Spec.
It describes a fictional command, not a shipped or tested implementation.

Rowpick selects records for local inspection using an exact match on a single
top-level string field. For example:

```text
rowpick events.jsonl --field level --equals error
```

The input file must be readable and contain UTF-8 JSON objects, one per line.
Matching records are streamed to stdout as newline-delimited JSON. A missing
field or non-string value is a non-match. There are no nested-field queries,
regular expressions or joins.

The documented command reads but never modifies the input file and performs no
network access. Exit 0 indicates complete processing, including zero matches.
Invalid JSON, a non-object row or an unreadable input produces exit 2.
Processing stops on error; stdout may already contain earlier matching rows.
Consumers needing a complete result must check the exit status.

This source does not specify supported platforms, installation, throughput or
memory limits. No implementation or executed test evidence is supplied.
