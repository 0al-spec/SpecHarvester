# P6-T1 Discover Nested Swift Package Manifests during Static Harvest

## Scope

- Extend static collector discovery for nested `Package.swift` files.
- Preserve the local-only trust boundary: no SwiftPM execution, no package
  scripts, no dependency installation, and no network access.
- Keep generated batch validation confidence tied to collected static evidence.
- Add focused tests for nested Swift package discovery and batch confidence.

## Branch

- `feature/P6-T1-discover-nested-swift-package-manifests`

## Smoke Evidence

- Before this task, the smoke run downgraded `cupertino` to medium confidence
  because `Packages/Package.swift` was not recognized as package-manifest
  evidence.
- After this task, `cupertino` collects `Packages/Package.swift`,
  `packageManifestCount` becomes `1`, and batch confidence becomes `high`.

## Result

- `collector.candidate_files()` now includes bounded nested Swift manifest
  discovery.
- Nested Swift discovery ignores root `Package.swift` duplicates and common
  generated/vendor directories such as `.build`, `.git`, `.swiftpm`,
  `DerivedData`, `build`, and `node_modules`.
- Batch validation reports now see nested Swift manifests as package evidence
  through the existing `package_manifest` classification.
