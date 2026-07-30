# Targeted Semantic Quality Calibration

P55-T9 compared Codex 5.3 Spark and LM Studio on `rtk-ai/rtk`,
`openai/codex`, `BurntSushi/ripgrep`, and `thedotmack/claude-mem`.

Spark completed two of four proposals; only Codex had an accurate
repository-specific purpose, while RTK missed token reduction and two outputs
were schema-invalid. LM Studio completed zero of four because schema fragments
appeared in proposal value positions.

Neither provider met the frozen purpose, evidence, schema, and reviewer-burden
gates. P55-T10 remains blocked pending a bounded output-conformance follow-up
and an exact targeted rerun. No thresholds, candidates, intents, registry
records, or public index data were changed.
