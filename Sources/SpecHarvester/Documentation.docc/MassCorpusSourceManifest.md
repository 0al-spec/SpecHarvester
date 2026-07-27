# Mass Corpus Source Manifest

``P53-T3`` records the immutable 100-source input boundary for the Phase 53
campaign. The source manifest and companion selection metadata are separate
from the P52 reference corpus and divide sources into four waves of 25.

Each source has a canonical public GitHub HTTPS origin, a full pinned revision,
an expected operator-provided checkout path, and public discovery evidence for
popularity, language, license metadata, provenance, and size policy. The
selection is not checkout readiness evidence.

P53-T4 verifies local checkout presence, cleanliness, revision, size, and
license/provenance evidence before static parsing can begin. This task does not
clone or fetch repositories, invoke Codex Spark or LM Studio, execute package
managers or harvested code, accept packages or relations, or publish registry
metadata.
