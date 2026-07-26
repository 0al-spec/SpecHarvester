from __future__ import annotations

from pathlib import Path

LICENSE_FILE_BASENAMES = {"LICENSE", "COPYING"}
CANONICAL_DUAL_LICENSE_FILENAMES = {"LICENSE-APACHE", "LICENSE-MIT"}
LICENSE_FILE_TEXT_EXTENSIONS = {"", ".txt", ".md", ".markdown", ".rst"}


def is_license_filename(path: Path) -> bool:
    name = path.name
    if name.upper() in CANONICAL_DUAL_LICENSE_FILENAMES:
        return True
    suffix = path.suffix.lower()
    if suffix not in LICENSE_FILE_TEXT_EXTENSIONS:
        return False
    stem = path.stem if suffix else name
    return stem.upper() in LICENSE_FILE_BASENAMES
