# P10-T2 Validation Report

Status: Passed
Updated: 2026-05-19
Task: `P10-T2` Manifest-First Ecosystem Detectors

## Scope

Implemented manifest-first detector coverage for the initial `ProjectProfile`
ecosystem matrix:

- JavaScript package managers: npm, pnpm, Yarn, Bun.
- Swift/SPM.
- Python packaging: PyPI, pip, setuptools.
- Java/Kotlin: Maven and Gradle.
- Go modules.
- PHP Composer.
- C/C++ package/build manifests: CMake, Meson, Autotools, make, Conan, vcpkg.
- Objective-C/iOS: Xcode project/workspace metadata and CocoaPods.
- Ruby: Bundler and RubyGems.
- Rust Cargo.

## Validation

- `ruff check src tests`
  - Result: Passed.
- `ruff format --check src tests`
  - Result: Passed.
- `PYTHONPATH=src python -m pytest tests/test_collector.py -q`
  - Result: Passed, 63 tests.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - Result: Passed, 182 tests.
  - Coverage: 90.71%.
- `swift package dump-package >/dev/null`
  - Result: Passed.
- `swift build --target SpecHarvesterDocs`
  - Result: Passed.

## Notes

- Detector output remains path/manifest based and deterministic.
- No harvested package scripts, build tools, dependency installers, analyzers,
  or network probes were executed.
- Analyzer plan entries remain advisory; only existing Python and JS/TS public
  API analyzers are recommended for execution by later workflow steps.
