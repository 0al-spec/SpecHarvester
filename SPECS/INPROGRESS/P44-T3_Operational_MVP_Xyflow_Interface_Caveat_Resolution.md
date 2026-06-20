# P44-T3 Operational MVP Xyflow Interface Caveat Resolution

## Status

Planned.

## Motivation

P43-T4 and P43-T6 kept two xyflow manual-correction caveats visible:
partial `PublicInterfaceIndex` evidence and operator checkout fork origin. P44-T3
must decide whether those caveats block the P44 rerun or can be accepted with
explicit review boundaries.

## Goal

Record a durable caveat resolution artifact for xyflow that distinguishes
acceptable bounded parser coverage limits from registry-facing acceptance
requirements.

## Deliverables

- Machine-readable `SpecHarvesterOperationalMVPXyflowCaveatResolution` fixture.
- Explicit decision for partial public-interface evidence.
- Explicit decision for SoundBlaster fork-origin evidence.
- GitHub documentation, DocC mirror, navigation links, and docs-contract
  coverage.
- Validation report for this task.

## Acceptance Criteria

- The fixture references P43-T4, P43-T6, and P44-T2 by path, digest, API
  version, kind, and authority.
- The fixture records that partial public-interface evidence is accepted for
  the bounded P44 rerun but remains visible for author review.
- The fixture records that SoundBlaster fork-origin evidence is acceptable as
  operator-provided review input for P44, but not canonical upstream acceptance.
- The fixture does not accept packages, relations, AI output, adapter output, or
  registry truth.

## Non-Goals

- Do not rerun public-interface extraction.
- Do not clone or fetch canonical xyflow upstream.
- Do not modify generated package candidates.
- Do not approve registry publication or broader scraping.
