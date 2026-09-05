# P56-T3 Bounded Authoring Runner

## Implementation Checkpoint

P56-T3 is **in progress**. `investigative_authoring_io.py` implements the
caller-side evidence budget and candidate sink. It is not a standalone agent,
worker sandbox, completed execution lock, or permission to start P56-T4.

The existing Codex semantic adapter starts `codex exec --sandbox read-only`
from the inherited environment. Its transport does not mediate source reads,
count unique returned byte ranges, or demonstrate evaluator/sibling denial.
Wrapping output JSON cannot establish those missing properties. The frozen
T1 protocol requires that any necessary current-arm protocol change precede
both scored generation arms.

## Implemented I/O Contract

`AuthoringEvidence` receives a caller-owned source root and relative-path to
SHA-256 allowlist. It returns only requested UTF-8 source slices after checking
the complete file digest. Directory traversal is descriptor-relative, refuses
symlinks and nonregular files, and does not import or execute target code.
The root and its ancestors are trusted caller configuration, not model input.

Byte ranges are zero-based, half-open. Requests must be nonempty and no longer
than 24 KiB. Partial UTF-8 characters are excluded and both requested and actual
returned ranges are recorded. EOF shortening is explicit. The union of actual
returned ranges is charged per file, with 24 KiB per file, 96 KiB aggregate,
and 100 requests per repository/arm. Repeated reads still consume requests.
A budget violation is sticky: reuse the same object across repairs and retries.

Generated/projected evidence is charged through `generated(item, text)` using
the exact caller-serialized UTF-8 bytes. Stable item IDs cannot change content;
different IDs count separately even when their text matches. The caller must
route every generated evidence item through this method. Instructions and
schema are separate from evidence. This primitive alone cannot prevent a
provider from obtaining unmetered evidence through another tool.

The read ledger contains sequence, operation, source path/hash, requested and
returned ranges, returned bytes, monotonic start/end, and status/code. It keeps
no content, prompts, model responses or reasoning. Denied unlisted or unsafe
paths are not copied into portable receipts. Monotonic timestamps are meaningful
within one process only; they are not wall-clock provenance.

`CandidateOutput` writes a complete mapping of relative paths to UTF-8 contents
into a new directory, at most 256 KiB by default. It refuses traversal, conflicting
file/directory names, and existing output. It is a data sink, not SpecPM validation
or publication approval. Caller ownership and exclusive access to the output
parent are required; it is not a filesystem sandbox against other local writers.
An I/O failure may leave a partial directory, which must remain a failed attempt
rather than be silently overwritten. Schema validity, preview-only boundaries,
and semantic correctness still require their respective gates.

## Remaining Admission Obligations

Before P56-T3 can be marked complete:

1. Connect an isolated provider runtime to the metered tool broker. Exclude
   parent history, personal config/skills, evaluator data, sibling outputs,
   arbitrary network tools and source execution. Model transport credentials
   stay outside portable evidence.
2. Run positive controls and negative access probes in that same runtime.
   A missing mount, mock provider, prompt instruction or untested receipt is
   not sufficient evidence of the complete boundary.
3. Enforce the model-call, attempt, repair, retry and total-time budgets at the
   subprocess/request boundary; collect actual usage when available.
4. Integrate trusted SpecPM validation and selected-boundary receipts.
5. Demonstrate unchanged bounded arm A, or version its necessary protocol
   change explicitly. Lock both arms' inputs, implementation hashes, runtime
   versions and probe results before scored generation.

No live provider was used for this checkpoint. The separate Luna-medium Logrus
smoke does not satisfy these obligations. T1 targets, model, scoring and answer
key remain unchanged.
