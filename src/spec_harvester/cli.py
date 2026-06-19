from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from spec_harvester.accepted_candidate_impact import (
    build_accepted_candidate_impact_report,
    write_accepted_candidate_impact_report,
)
from spec_harvester.accepted_diff import (
    build_accepted_candidate_diff_report,
    write_accepted_candidate_diff_report,
)
from spec_harvester.accepted_update_proposal import (
    AcceptedPackageUpdateProposalOptions,
    build_accepted_package_update_proposal,
    build_accepted_package_update_proposal_markdown,
    write_accepted_package_update_proposal,
    write_accepted_package_update_proposal_markdown,
)
from spec_harvester.ai_enrichment_candidate_patch import (
    AIEnrichmentCandidatePatchOptions,
    build_ai_enrichment_candidate_patch,
)
from spec_harvester.author_ready_calibration_matrix import (
    build_author_ready_calibration_matrix,
    write_author_ready_calibration_matrix,
)
from spec_harvester.autonomous_candidate_batch import (
    DEFAULT_AUTONOMOUS_ROLE_PROFILE,
    DEFAULT_LM_STUDIO_BASE_URL,
    DEFAULT_PROVIDER_NAME,
    AutonomousCandidateBatchOptions,
    run_autonomous_candidate_batch,
)
from spec_harvester.baseline_submission_handoff import (
    BaselineSubmissionHandoffOptions,
    build_baseline_submission_handoff,
    write_baseline_submission_handoff,
)
from spec_harvester.batch_collection import BatchCollectOptions, collect_batch_snapshots
from spec_harvester.bundle_set_preflight import (
    BundleSetPreflightOptions,
    run_bundle_set_preflight,
)
from spec_harvester.candidate_bundle_preflight import (
    CandidateBundlePreflightOptions,
    run_candidate_bundle_preflight,
)
from spec_harvester.cli_report_commands import (
    run_architecture_lint,
    run_code_duplication_report,
    run_procedural_style_report,
)
from spec_harvester.code_duplication_report import (
    BACKEND_BUILTIN,
    BACKEND_JSCPD,
    BACKEND_PYLINT,
    DEFAULT_MIN_LINES,
)
from spec_harvester.codegraph_compatibility import (
    CodeGraphCompatibilityOptions,
    build_codegraph_compatibility_report,
    write_codegraph_compatibility_report,
)
from spec_harvester.codegraph_source_graph import (
    DEFAULT_MAX_EDGES as CODEGRAPH_DEFAULT_MAX_EDGES,
)
from spec_harvester.codegraph_source_graph import (
    DEFAULT_MAX_NODES as CODEGRAPH_DEFAULT_MAX_NODES,
)
from spec_harvester.codegraph_source_graph import (
    CodeGraphSourceGraphOptions,
    build_codegraph_source_graph_index,
    write_codegraph_source_graph_index,
)
from spec_harvester.collector import (
    DEFAULT_MAX_FILE_BYTES,
    HarvestOptions,
    collect_local_repository,
)
from spec_harvester.drafter import (
    DEFAULT_AUTHOR,
    DEFAULT_SPEC_VERSION,
    DraftOptions,
    draft_spec_package,
)
from spec_harvester.fresh_candidate_refresh_run import (
    FreshCandidateRefreshRunOptions,
    build_fresh_candidate_refresh_run,
    write_fresh_candidate_refresh_run,
)
from spec_harvester.governance_reports import (
    build_duplicate_claim_report,
    write_governance_report,
)
from spec_harvester.license_provenance_reports import (
    build_license_provenance_risk_report,
    write_license_provenance_report,
)
from spec_harvester.model_json_repair import DEFAULT_JSON_REPAIR_MAX_ATTEMPTS
from spec_harvester.namespace_reports import (
    build_namespace_upstream_report,
    write_namespace_upstream_report,
)
from spec_harvester.package_set_ai_draft_proposal import (
    PackageSetAIDraftProposalOptions,
    build_package_set_ai_draft_proposal,
    write_package_set_ai_draft_proposal,
)
from spec_harvester.package_set_ai_draft_proposal import (
    model_request_record as package_set_ai_draft_request,
)
from spec_harvester.package_set_ai_draft_proposal import (
    write_model_request_record as write_package_set_ai_draft_request,
)
from spec_harvester.package_set_ai_enrichment import (
    PackageSetAIEnrichmentOptions,
    build_package_set_ai_enrichment_proposal,
    model_request_records,
    write_model_request_records,
    write_package_set_ai_enrichment_proposal,
)
from spec_harvester.package_set_drafter import (
    DEFAULT_ROLE_SELECTION_PROFILE,
    PACKAGE_SET_ROLE_PROFILES,
    PackageSetDraftOptions,
    draft_package_set,
)
from spec_harvester.package_set_handoff_proposal import (
    PackageSetHandoffProposalOptions,
    build_package_set_handoff_proposal,
    write_package_set_handoff_proposal,
    write_package_set_handoff_proposal_markdown,
)
from spec_harvester.procedural_style_report import (
    DEFAULT_HOTSPOT_MIN_TOP_LEVEL_COUNT,
    DEFAULT_HOTSPOT_MIN_TOP_LEVEL_SPAN,
)
from spec_harvester.promoter import (
    PrepareAcceptedManifestEntryOptions,
    PromoteOptions,
    prepare_accepted_manifest_entry,
    promote_candidate,
)
from spec_harvester.real_repo_quality_report import (
    build_quality_report,
    write_quality_report,
)
from spec_harvester.repository_profile_detection import (
    RepositoryIdentity,
    RepositoryProfileDetectionOptions,
    build_repository_profile_detection,
    repository_identity_from_source_manifest,
    write_repository_profile_detection,
)
from spec_harvester.selected_candidate_handoff_proposal import (
    SelectedCandidateHandoffProposalOptions,
    build_selected_candidate_handoff_proposal,
    write_selected_candidate_handoff_proposal,
    write_selected_candidate_handoff_proposal_markdown,
)
from spec_harvester.smoke_triage import (
    build_smoke_triage_summary,
    write_smoke_triage_summary,
)
from spec_harvester.source_manifest import read_repository_source_manifests
from spec_harvester.static_spec_renderer import (
    StaticPackageSetRendererOptions,
    StaticSpecRendererOptions,
    render_static_package_set_site,
    render_static_spec_site,
)
from spec_harvester.xyflow_package_set_smoke import (
    XyflowPackageSetSmokeOptions,
    run_xyflow_package_set_smoke,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="spec-harvester")
    subcommands = parser.add_subparsers(dest="command", required=True)

    collect_local = subcommands.add_parser(
        "collect-local",
        help="Collect a safe evidence snapshot from a local repository, folder, or file target.",
    )
    collect_local.add_argument("source", type=Path, help="Local source root or direct file target.")
    collect_local.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output directory where harvest.json will be written.",
    )
    collect_local.add_argument("--repository", help="Public source repository URL.")
    collect_local.add_argument("--revision", help="Pinned source revision or commit SHA.")
    collect_local.add_argument(
        "--target",
        type=Path,
        help="Optional folder or file path relative to source root to harvest as the spec target.",
    )
    collect_local.add_argument(
        "--max-file-bytes",
        type=int,
        default=DEFAULT_MAX_FILE_BYTES,
        help=f"Maximum allowlisted file size to read. Default: {DEFAULT_MAX_FILE_BYTES}.",
    )
    collect_local.set_defaults(func=run_collect_local)

    collect_batch = subcommands.add_parser(
        "collect-batch",
        help="Collect harvest snapshots from repository source manifests.",
    )
    collect_batch.add_argument(
        "inputs",
        type=Path,
        help="Directory containing repository source manifests matching *.yml.",
    )
    collect_batch.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output root where deterministic candidate directories are written.",
    )
    collect_batch.add_argument(
        "--select",
        action="append",
        default=[],
        help="Repository id to collect. Can be passed multiple times.",
    )
    collect_batch.add_argument(
        "--max-file-bytes",
        type=int,
        default=DEFAULT_MAX_FILE_BYTES,
        help=f"Maximum allowlisted file size to read. Default: {DEFAULT_MAX_FILE_BYTES}.",
    )
    collect_batch.add_argument(
        "--report",
        type=Path,
        help="Optional path where a deterministic batch validation JSON report is written.",
    )
    collect_batch.add_argument(
        "--relaxed-private",
        action="store_true",
        help=("Disable strict public registry preflight checks for private-code spec coverage."),
    )
    collect_batch.add_argument(
        "--emit-interface-indexes",
        action="store_true",
        help=(
            "Opt in to running built-in static analyzers recommended by "
            "ProjectProfile.analyzerPlan and write public-interface-index.json."
        ),
    )
    collect_batch.add_argument(
        "--analyzer-cache-dir",
        type=Path,
        help=(
            "Optional root for per-repository static analyzer caches when "
            "--emit-interface-indexes is set."
        ),
    )
    collect_batch.add_argument(
        "--parser-profile",
        dest="parser_profile_id",
        help=(
            "Optional repository parsing profile id for static analyzer path "
            "classification. Example: python.web_framework.v0."
        ),
    )
    collect_batch.add_argument(
        "--emit-workspace-inventory",
        action="store_true",
        help=(
            "Opt in to writing deterministic workspace-inventory.json artifacts for "
            "monorepo/package-set review."
        ),
    )
    collect_batch.set_defaults(func=run_collect_batch)

    autonomous_candidate_batch = subcommands.add_parser(
        "autonomous-candidate-batch",
        help=(
            "Run the local-source autonomous candidate MVP over repository "
            "source manifests and write a batch report."
        ),
    )
    autonomous_candidate_batch.add_argument(
        "inputs",
        type=Path,
        help="Directory containing repository source manifests matching *.yml.",
    )
    autonomous_candidate_batch.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output root for collected evidence, package-set bundles, AI proposals, and report.",
    )
    autonomous_candidate_batch.add_argument(
        "--select",
        action="append",
        default=[],
        help="Repository id to process. Can be passed multiple times.",
    )
    autonomous_candidate_batch.add_argument(
        "--max-file-bytes",
        type=int,
        default=DEFAULT_MAX_FILE_BYTES,
        help=f"Maximum allowlisted file size to read. Default: {DEFAULT_MAX_FILE_BYTES}.",
    )
    autonomous_candidate_batch.add_argument(
        "--relaxed-private",
        action="store_true",
        help="Disable strict public registry preflight checks for private-code experiments.",
    )
    autonomous_candidate_batch.add_argument(
        "--analyzer-cache-dir",
        type=Path,
        help="Optional root for per-repository static analyzer caches.",
    )
    autonomous_candidate_batch.add_argument(
        "--parser-profile",
        dest="parser_profile_id",
        help=(
            "Optional repository parsing profile id for static analyzer path "
            "classification. Example: python.web_framework.v0."
        ),
    )
    autonomous_candidate_batch.add_argument(
        "--repository-profile-selection",
        default="none",
        help=(
            "Repository profile selection mode for producer-side evidence: "
            "none, auto, or an explicit profile id. Default: none."
        ),
    )
    autonomous_candidate_batch.add_argument(
        "--repository-plugin-applicability",
        type=Path,
        help=(
            "Optional SpecHarvesterRepositoryPluginApplicabilityReport JSON to "
            "copy into batch output as sidecar producer evidence."
        ),
    )
    autonomous_candidate_batch.add_argument(
        "--role-profile",
        choices=tuple(PACKAGE_SET_ROLE_PROFILES),
        default=DEFAULT_AUTONOMOUS_ROLE_PROFILE,
        help=(f"Package-set role selection profile. Default: {DEFAULT_AUTONOMOUS_ROLE_PROFILE}."),
    )
    autonomous_candidate_batch.add_argument(
        "--role",
        action="append",
        default=[],
        help="Inventory package role to draft. Can be repeated.",
    )
    autonomous_candidate_batch.add_argument(
        "--skip-ai",
        action="store_true",
        help="Disable local model calls for deterministic offline runs.",
    )
    autonomous_candidate_batch.add_argument(
        "--lm-studio-base-url",
        default=DEFAULT_LM_STUDIO_BASE_URL,
        help=f"Local OpenAI-compatible provider base URL. Default: {DEFAULT_LM_STUDIO_BASE_URL}.",
    )
    autonomous_candidate_batch.add_argument(
        "--lm-studio-model",
        help="Local model id for LM Studio/OpenAI-compatible execution, e.g. openai/gpt-oss-20b.",
    )
    autonomous_candidate_batch.add_argument(
        "--provider-name",
        default=DEFAULT_PROVIDER_NAME,
        help=f"Provider label recorded in proposal artifacts. Default: {DEFAULT_PROVIDER_NAME}.",
    )
    autonomous_candidate_batch.add_argument(
        "--json-repair-max-attempts",
        type=int,
        default=DEFAULT_JSON_REPAIR_MAX_ATTEMPTS,
        help=(
            "Maximum malformed JSON repair prompts per local model call. "
            f"Default: {DEFAULT_JSON_REPAIR_MAX_ATTEMPTS}."
        ),
    )
    autonomous_candidate_batch.add_argument(
        "--apply-ai-enrichment",
        action="store_true",
        help=(
            "Opt in to applying clean AI enrichment proposals into copied "
            "preview candidates with ai-enrichment-candidate-patch.json reports."
        ),
    )
    autonomous_candidate_batch.set_defaults(func=run_autonomous_candidate_batch_cli)

    draft = subcommands.add_parser(
        "draft",
        help="Draft a candidate SpecPackage from a harvest.json snapshot.",
    )
    draft.add_argument("snapshot", type=Path, help="Harvest snapshot file or directory.")
    draft.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output candidate package directory.",
    )
    draft.add_argument(
        "--package-id",
        help="SpecPackage id. Defaults to <repository-name>.core.",
    )
    draft.add_argument("--name", help="Human-readable package name.")
    draft.add_argument(
        "--version",
        default=DEFAULT_SPEC_VERSION,
        help=f"Generated SpecPackage version. Default: {DEFAULT_SPEC_VERSION}.",
    )
    draft.add_argument(
        "--author",
        default=DEFAULT_AUTHOR,
        help=f"Generated SpecPackage author. Default: {DEFAULT_AUTHOR}.",
    )
    draft.add_argument(
        "--interface-index",
        type=Path,
        help=(
            "Optional PublicInterfaceIndex JSON artifact used to enrich "
            "generated interfaces.inbound entries."
        ),
    )
    draft.set_defaults(func=run_draft)

    draft_package_set_parser = subcommands.add_parser(
        "draft-package-set",
        help="Draft preview candidate packages from workspace-inventory.json.",
    )
    draft_package_set_parser.add_argument(
        "inventory",
        type=Path,
        help="Workspace inventory JSON produced by collect-batch --emit-workspace-inventory.",
    )
    draft_package_set_parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output directory where package-set candidate bundles are written.",
    )
    draft_package_set_parser.add_argument(
        "--version",
        default=DEFAULT_SPEC_VERSION,
        help=f"Generated SpecPackage version. Default: {DEFAULT_SPEC_VERSION}.",
    )
    draft_package_set_parser.add_argument(
        "--author",
        default=DEFAULT_AUTHOR,
        help=f"Generated SpecPackage author. Default: {DEFAULT_AUTHOR}.",
    )
    draft_package_set_parser.add_argument(
        "--role-profile",
        choices=tuple(PACKAGE_SET_ROLE_PROFILES),
        default=DEFAULT_ROLE_SELECTION_PROFILE,
        help=(
            "Named package role selection profile. Use generic_monorepo to draft "
            "workspace plus member_package entries. Explicit --role values override "
            "the profile. Default: default."
        ),
    )
    draft_package_set_parser.add_argument(
        "--role",
        action="append",
        default=[],
        help=(
            "Inventory package role to draft. Can be repeated. Defaults to "
            "the selected --role-profile."
        ),
    )
    draft_package_set_parser.set_defaults(func=run_draft_package_set)

    render_spec_site = subcommands.add_parser(
        "render-spec-site",
        help="Render a generated SpecPM candidate package as a static HTML/JS site.",
    )
    render_spec_site.add_argument(
        "--candidate",
        type=Path,
        required=True,
        help="Candidate package directory containing specpm.yaml.",
    )
    render_spec_site.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output directory where the static site will be written.",
    )
    render_spec_site.set_defaults(func=run_render_spec_site)

    render_package_set_site = subcommands.add_parser(
        "render-package-set-site",
        help="Render a generated package-set output directory as a static HTML/JS site.",
    )
    render_package_set_site.add_argument(
        "--bundle-set",
        type=Path,
        required=True,
        help="Package-set output directory containing package-set-draft.json.",
    )
    render_package_set_site.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output directory where the static site will be written.",
    )
    render_package_set_site.set_defaults(func=run_render_package_set_site)

    preflight = subcommands.add_parser(
        "preflight-candidate-bundle",
        help="Verify a generated SpecPM candidate bundle before SpecPM handoff.",
    )
    preflight.add_argument(
        "candidate",
        type=Path,
        help="Candidate package directory containing producer-receipt.json.",
    )
    preflight.set_defaults(func=run_preflight_candidate_bundle)

    bundle_set_preflight = subcommands.add_parser(
        "preflight-bundle-set",
        help="Verify a generated package-set output directory before SpecPM handoff.",
    )
    bundle_set_preflight.add_argument(
        "bundle_set",
        type=Path,
        help="Package-set output directory containing package-set-draft.json.",
    )
    bundle_set_preflight.set_defaults(func=run_preflight_bundle_set)

    package_set_handoff_proposal = subcommands.add_parser(
        "package-set-handoff-proposal",
        help="Build a reviewable SpecPM handoff proposal for a generated package set.",
    )
    package_set_handoff_proposal.add_argument(
        "--bundle-set",
        type=Path,
        required=True,
        help="Package-set output directory containing package-set-draft.json.",
    )
    package_set_handoff_proposal.add_argument(
        "--viewer",
        type=Path,
        help="Optional package-set viewer output directory containing index.html.",
    )
    package_set_handoff_proposal.add_argument(
        "--output",
        type=Path,
        help="Optional path where proposal JSON is written.",
    )
    package_set_handoff_proposal.add_argument(
        "--proposal-body",
        type=Path,
        help="Optional path where Markdown proposal body is written.",
    )
    package_set_handoff_proposal.set_defaults(func=run_package_set_handoff_proposal)

    selected_candidate_handoff_proposal = subcommands.add_parser(
        "selected-candidate-handoff-proposal",
        help="Build a reviewable SpecPM handoff proposal for selected candidate bundles.",
    )
    selected_candidate_handoff_proposal.add_argument(
        "--selected-handoff-dry-run",
        type=Path,
        required=True,
        help="P30 selected handoff dry-run JSON fixture or artifact.",
    )
    selected_candidate_handoff_proposal.add_argument(
        "--candidate-root",
        type=Path,
        help="Optional root containing <package_id>/candidate or <package_id> bundles.",
    )
    selected_candidate_handoff_proposal.add_argument(
        "--preflight-root",
        type=Path,
        help="Optional root containing <package_id>.json producer preflight reports.",
    )
    selected_candidate_handoff_proposal.add_argument(
        "--viewer-root",
        type=Path,
        help="Optional root containing <package_id>/index.html viewer outputs.",
    )
    selected_candidate_handoff_proposal.add_argument(
        "--output",
        type=Path,
        help="Optional path where proposal JSON is written.",
    )
    selected_candidate_handoff_proposal.add_argument(
        "--proposal-body",
        type=Path,
        help="Optional path where Markdown proposal body is written.",
    )
    selected_candidate_handoff_proposal.set_defaults(func=run_selected_candidate_handoff_proposal)

    fresh_candidate_refresh_run = subcommands.add_parser(
        "fresh-candidate-refresh-run",
        help=(
            "Export a generated package-set bundle into a SpecPM "
            "prepare-refresh-decision fresh generated root."
        ),
    )
    fresh_candidate_refresh_run.add_argument(
        "--bundle-set",
        type=Path,
        required=True,
        help="Package-set output directory containing package-set-draft.json.",
    )
    fresh_candidate_refresh_run.add_argument(
        "--fresh-generated-root",
        type=Path,
        required=True,
        help=(
            "Output root where candidates are copied as "
            "<package_id>/<version>/specpm.yaml and specs/*.spec.yaml."
        ),
    )
    fresh_candidate_refresh_run.add_argument(
        "--source-repository",
        help="Optional source repository URL override recorded for SpecPM compare.",
    )
    fresh_candidate_refresh_run.add_argument(
        "--source-revision",
        help=(
            "Optional source revision override. Defaults to "
            "package-set-draft.json source.exactRevision or source.revision."
        ),
    )
    fresh_candidate_refresh_run.add_argument(
        "--run-label",
        default="local-refresh-evaluation",
        help="Human-readable run label recorded for SpecPM compare.",
    )
    fresh_candidate_refresh_run.add_argument(
        "--output",
        type=Path,
        help="Optional path where SpecHarvesterFreshCandidateRefreshRun JSON is written.",
    )
    fresh_candidate_refresh_run.set_defaults(func=run_fresh_candidate_refresh_run)

    baseline_submission_handoff = subcommands.add_parser(
        "baseline-submission-handoff",
        help=(
            "Build first-submission or seeded-baseline handoff evidence when "
            "SpecPM cannot prepare a refresh decision because no generated "
            "baseline exists."
        ),
    )
    baseline_submission_handoff.add_argument(
        "--fresh-candidate-refresh-run",
        type=Path,
        required=True,
        help="Path to SpecHarvesterFreshCandidateRefreshRun JSON.",
    )
    baseline_submission_handoff.add_argument(
        "--specpm-prepare-report",
        type=Path,
        help=(
            "Optional SpecPM prepare-report.json. When provided, it must contain "
            "refresh_decision_prepare_current_contract_files_missing diagnostics."
        ),
    )
    baseline_submission_handoff.add_argument(
        "--output",
        type=Path,
        help="Optional path where SpecHarvesterBaselineSubmissionHandoff JSON is written.",
    )
    baseline_submission_handoff.set_defaults(func=run_baseline_submission_handoff)

    package_set_ai_draft = subcommands.add_parser(
        "package-set-ai-draft-proposal",
        help="Build proposal-only LLM package-set draft selection from workspace inventory.",
    )
    package_set_ai_draft.add_argument(
        "inventory",
        type=Path,
        help="Workspace inventory JSON produced by collect-batch --emit-workspace-inventory.",
    )
    package_set_ai_draft.add_argument(
        "--source-checkout",
        type=Path,
        help="Optional local public repository checkout used for allowlisted root evidence.",
    )
    package_set_ai_draft.add_argument(
        "--provider-base-url",
        help="Optional local OpenAI-compatible provider base URL, e.g. http://127.0.0.1:1234.",
    )
    package_set_ai_draft.add_argument(
        "--provider-name",
        default="lm_studio",
        help="Provider label recorded in the proposal. Default: lm_studio.",
    )
    package_set_ai_draft.add_argument(
        "--model",
        help="OpenAI-compatible model id, e.g. openai/gpt-oss-20b.",
    )
    package_set_ai_draft.add_argument(
        "--model-output",
        type=Path,
        help="Optional external model output JSON to wrap instead of calling a provider.",
    )
    package_set_ai_draft.add_argument(
        "--request-output",
        type=Path,
        help="Optional path where compact package-set model request is written.",
    )
    package_set_ai_draft.add_argument(
        "--output",
        type=Path,
        help="Optional path where AI draft proposal JSON is written.",
    )
    package_set_ai_draft.add_argument(
        "--timeout-seconds",
        type=float,
        default=120.0,
        help="Provider request timeout in seconds. Default: 120.",
    )
    package_set_ai_draft.add_argument(
        "--max-output-tokens",
        type=int,
        default=3000,
        help="Maximum provider output tokens. Default: 3000.",
    )
    package_set_ai_draft.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Provider temperature. Default: 0.",
    )
    package_set_ai_draft.add_argument(
        "--json-repair-max-attempts",
        type=int,
        default=DEFAULT_JSON_REPAIR_MAX_ATTEMPTS,
        help=(
            "Maximum malformed JSON repair prompts for live provider output. "
            f"Default: {DEFAULT_JSON_REPAIR_MAX_ATTEMPTS}."
        ),
    )
    package_set_ai_draft.set_defaults(func=run_package_set_ai_draft_proposal)

    package_set_ai_enrichment = subcommands.add_parser(
        "package-set-ai-enrichment-proposal",
        help="Build proposal-only AI enrichment for a generated package set.",
    )
    package_set_ai_enrichment.add_argument(
        "--bundle-set",
        type=Path,
        required=True,
        help="Package-set output directory containing package-set-draft.json.",
    )
    package_set_ai_enrichment.add_argument(
        "--source-checkout",
        type=Path,
        help="Optional local public repository checkout used for allowlisted evidence files.",
    )
    package_set_ai_enrichment.add_argument(
        "--provider-base-url",
        help="Optional local OpenAI-compatible provider base URL, e.g. http://127.0.0.1:1234.",
    )
    package_set_ai_enrichment.add_argument(
        "--provider-name",
        default="lm_studio",
        help="Provider label recorded in the proposal. Default: lm_studio.",
    )
    package_set_ai_enrichment.add_argument(
        "--model",
        help="OpenAI-compatible model id, e.g. openai/gpt-oss-20b.",
    )
    package_set_ai_enrichment.add_argument(
        "--model-output",
        type=Path,
        help="Optional external model output JSON to wrap instead of calling a provider.",
    )
    package_set_ai_enrichment.add_argument(
        "--request-output",
        type=Path,
        help="Optional path where compact per-package model requests are written.",
    )
    package_set_ai_enrichment.add_argument(
        "--output",
        type=Path,
        help="Optional path where AI enrichment proposal JSON is written.",
    )
    package_set_ai_enrichment.add_argument(
        "--timeout-seconds",
        type=float,
        default=120.0,
        help="Provider request timeout in seconds. Default: 120.",
    )
    package_set_ai_enrichment.add_argument(
        "--max-output-tokens",
        type=int,
        default=2200,
        help="Maximum provider output tokens per package. Default: 2200.",
    )
    package_set_ai_enrichment.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Provider temperature. Default: 0.",
    )
    package_set_ai_enrichment.add_argument(
        "--json-repair-max-attempts",
        type=int,
        default=DEFAULT_JSON_REPAIR_MAX_ATTEMPTS,
        help=(
            "Maximum malformed JSON repair prompts per live provider call. "
            f"Default: {DEFAULT_JSON_REPAIR_MAX_ATTEMPTS}."
        ),
    )
    package_set_ai_enrichment.set_defaults(func=run_package_set_ai_enrichment)

    apply_ai_enrichment = subcommands.add_parser(
        "apply-ai-enrichment-proposal",
        help="Apply a clean AI enrichment proposal to a copied preview candidate.",
    )
    apply_ai_enrichment.add_argument(
        "--proposal",
        type=Path,
        required=True,
        help="package-set-ai-enrichment-proposal.json to apply.",
    )
    apply_ai_enrichment.add_argument(
        "--candidate",
        type=Path,
        required=True,
        help="Generated candidate bundle to copy and enrich.",
    )
    apply_ai_enrichment.add_argument(
        "--package-id",
        help="Package id to apply when the proposal contains multiple packages.",
    )
    apply_ai_enrichment.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output directory for the enriched preview candidate copy.",
    )
    apply_ai_enrichment.add_argument(
        "--report",
        type=Path,
        help="Optional path for the machine-readable patch report.",
    )
    apply_ai_enrichment.set_defaults(func=run_apply_ai_enrichment_proposal)

    promote = subcommands.add_parser(
        "promote",
        help="Validate and copy a candidate package into an accepted source root.",
    )
    promote.add_argument("candidate", type=Path, help="Candidate SpecPackage directory.")
    promote.add_argument(
        "--accepted-root",
        type=Path,
        required=True,
        help="Directory where the promoted package copy will be written.",
    )
    promote.add_argument(
        "--manifest",
        type=Path,
        help="Optional accepted-packages.yml manifest to update with a local path entry.",
    )
    promote.add_argument(
        "--manifest-entry-path",
        help="Path to write into the manifest. Defaults to an inferred local path.",
    )
    promote.add_argument(
        "--package-subdir",
        help="Subdirectory under --accepted-root. Defaults to <package_id>/<version>.",
    )
    promote.add_argument(
        "--specpm-command",
        default="specpm",
        help="SpecPM validation command. Default: specpm.",
    )
    promote.add_argument(
        "--specpm-pythonpath",
        help="PYTHONPATH prefix for a local SpecPM checkout.",
    )
    promote.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip SpecPM validation. Intended only for tests or emergency manual workflows.",
    )
    promote.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing promoted package directory.",
    )
    promote.set_defaults(func=run_promote)

    prepare_manifest_entry = subcommands.add_parser(
        "prepare-accepted-entry",
        help="Prepare a PR-ready accepted-packages.yml entry for a reviewed candidate.",
    )
    prepare_manifest_entry.add_argument(
        "candidate", type=Path, help="Reviewed candidate SpecPackage directory."
    )
    prepare_manifest_entry.add_argument(
        "--manifest",
        required=True,
        type=Path,
        help="Accepted-packages manifest file to update.",
    )
    prepare_manifest_entry.add_argument(
        "--manifest-entry-path",
        help=(
            "Explicit manifest entry path to write. If set, --manifest-entry-prefix "
            "and --package-subdir are ignored."
        ),
    )
    prepare_manifest_entry.add_argument(
        "--manifest-entry-prefix",
        default="public-index/generated",
        help="Path prefix for inferred manifest entry. Default: public-index/generated.",
    )
    prepare_manifest_entry.add_argument(
        "--package-subdir",
        help=(
            "Package subdirectory used with --manifest-entry-prefix "
            "(defaults to <packageId>/<version>)."
        ),
    )
    prepare_manifest_entry.set_defaults(func=run_prepare_accepted_manifest_entry)

    source_manifests = subcommands.add_parser(
        "source-manifests",
        help="Read repository source manifests from an inputs directory and print JSON.",
    )
    source_manifests.add_argument(
        "inputs",
        type=Path,
        help="Directory containing repository source manifests matching *.yml.",
    )
    source_manifests.add_argument(
        "--include-disabled",
        action="store_true",
        help="Include entries with enabled: false in the JSON output.",
    )
    source_manifests.set_defaults(func=run_source_manifests)

    repository_profile_detect = subcommands.add_parser(
        "repository-profile-detect",
        help=(
            "Emit a producer-side repository profile detection artifact from "
            "operator-provided static evidence."
        ),
    )
    repository_profile_detect.add_argument(
        "--source-manifest",
        type=Path,
        help="Optional directory containing repository source manifests matching *.yml.",
    )
    repository_profile_detect.add_argument(
        "--source-id",
        help="Repository id to load from --source-manifest.",
    )
    repository_profile_detect.add_argument("--repository-id", help="Repository id.")
    repository_profile_detect.add_argument("--repository-url", help="Repository URL.")
    repository_profile_detect.add_argument("--ref", help="Repository ref.")
    repository_profile_detect.add_argument("--revision", help="Repository revision.")
    repository_profile_detect.add_argument(
        "--selection",
        default="auto",
        help="Repository profile selection: auto, none, or an explicit profile id.",
    )
    repository_profile_detect.add_argument(
        "--declared-repository-profile",
        help="Optional source-manifest declared repository profile metadata.",
    )
    repository_profile_detect.add_argument(
        "--evidence-path",
        action="append",
        default=[],
        help="Repository-relative static evidence path. Can be repeated.",
    )
    repository_profile_detect.add_argument(
        "--output",
        type=Path,
        help="Optional output path for repository-profile-detection.json.",
    )
    repository_profile_detect.set_defaults(func=run_repository_profile_detect)

    governance = subcommands.add_parser(
        "governance-report",
        help="Build duplicate intent and capability claim report from candidate/accepted metadata.",
    )
    governance.add_argument(
        "--accepted-root",
        type=Path,
        help="Accepted package source root for claim dedupe input.",
    )
    governance.add_argument(
        "--candidates-root",
        type=Path,
        help="Candidate package root for claim dedupe input.",
    )
    governance.add_argument(
        "--output",
        type=Path,
        help="Optional path where governance report JSON is written.",
    )
    governance.set_defaults(func=run_governance_report)

    namespace_upstream = subcommands.add_parser(
        "governance-upstream-report",
        help=(
            "Build namespace and upstream relationship review report from candidate/accepted "
            "metadata."
        ),
    )
    namespace_upstream.add_argument(
        "--accepted-root",
        type=Path,
        help="Accepted package source root for namespace/upstream input.",
    )
    namespace_upstream.add_argument(
        "--candidates-root",
        type=Path,
        help="Candidate package root for namespace/upstream input.",
    )
    namespace_upstream.add_argument(
        "--output",
        type=Path,
        help="Optional path where namespace/upstream report JSON is written.",
    )
    namespace_upstream.set_defaults(func=run_namespace_upstream_report)

    license_risk = subcommands.add_parser(
        "governance-license-provenance-report",
        help=(
            "Build license and upstream provenance risk review report from candidate/accepted "
            "metadata."
        ),
    )
    license_risk.add_argument(
        "--accepted-root",
        type=Path,
        help="Accepted package source root for risk input.",
    )
    license_risk.add_argument(
        "--candidates-root",
        type=Path,
        help="Candidate package root for risk input.",
    )
    license_risk.add_argument(
        "--output",
        type=Path,
        help="Optional path where license and provenance risk report JSON is written.",
    )
    license_risk.set_defaults(func=run_license_provenance_report)

    code_duplication = subcommands.add_parser(
        "code-duplication-report",
        help="Build an advisory duplicate-code report from local source files.",
    )
    code_duplication.add_argument(
        "--path",
        action="append",
        type=Path,
        default=[],
        help=("Source file or directory to scan. May be repeated. Defaults to src/spec_harvester."),
    )
    code_duplication.add_argument(
        "--min-lines",
        type=int,
        default=DEFAULT_MIN_LINES,
        help=(
            f"Minimum normalized line window to treat as a duplicate. Default: {DEFAULT_MIN_LINES}."
        ),
    )
    code_duplication.add_argument(
        "--output",
        type=Path,
        help="Optional path where duplicate-code report JSON is written.",
    )
    code_duplication.add_argument(
        "--backend",
        choices=(BACKEND_BUILTIN, BACKEND_PYLINT, BACKEND_JSCPD),
        default=BACKEND_BUILTIN,
        help=(
            "Duplicate-code detector backend. Use 'pylint' for the established "
            "Python R0801 checker or 'jscpd' for an optional multi-language "
            "detector. Default: builtin."
        ),
    )
    code_duplication.add_argument(
        "--pylint-command",
        default="pylint",
        help="Pylint executable to use when --backend pylint is selected. Default: pylint.",
    )
    code_duplication.add_argument(
        "--jscpd-command",
        default="jscpd",
        help=(
            "jscpd command to use when --backend jscpd is selected. "
            "May include command words such as 'npx --yes jscpd@4.2.4'. Default: jscpd."
        ),
    )
    code_duplication.add_argument(
        "--fail-on-duplicates",
        action="store_true",
        help="Return exit code 1 when duplicate blocks are detected.",
    )
    code_duplication.set_defaults(func=run_code_duplication_report)

    architecture_lint = subcommands.add_parser(
        "architecture-lint",
        help="Build an advisory architecture lint report for local source files.",
    )
    architecture_lint.add_argument(
        "--path",
        action="append",
        type=Path,
        default=[],
        help=("Source file or directory to scan. May be repeated. Defaults to src/spec_harvester."),
    )
    architecture_lint.add_argument(
        "--output",
        type=Path,
        help="Optional path where architecture lint report JSON is written.",
    )
    architecture_lint.add_argument(
        "--fail-on-issues",
        action="store_true",
        help="Return exit code 1 when architecture lint issues are detected.",
    )
    architecture_lint.set_defaults(func=run_architecture_lint)

    procedural_style = subcommands.add_parser(
        "procedural-style-report",
        help="Build an advisory procedural-style metrics report for local Python source files.",
    )
    procedural_style.add_argument(
        "--path",
        action="append",
        type=Path,
        default=[],
        help=("Source file or directory to scan. May be repeated. Defaults to src/spec_harvester."),
    )
    procedural_style.add_argument(
        "--output",
        type=Path,
        help="Optional path where procedural-style report JSON is written.",
    )
    procedural_style.add_argument(
        "--hotspot-min-top-level-count",
        type=int,
        default=DEFAULT_HOTSPOT_MIN_TOP_LEVEL_COUNT,
        help=(
            "Minimum top-level function count for a file to be treated as a hotspot. "
            f"Default: {DEFAULT_HOTSPOT_MIN_TOP_LEVEL_COUNT}."
        ),
    )
    procedural_style.add_argument(
        "--hotspot-min-top-level-span",
        type=int,
        default=DEFAULT_HOTSPOT_MIN_TOP_LEVEL_SPAN,
        help=(
            "Minimum top-level function span for a file to be treated as a hotspot. "
            f"Default: {DEFAULT_HOTSPOT_MIN_TOP_LEVEL_SPAN}."
        ),
    )
    procedural_style.add_argument(
        "--fail-on-hotspots",
        action="store_true",
        help="Return exit code 1 when procedural-style hotspots are detected.",
    )
    procedural_style.set_defaults(func=run_procedural_style_report)

    codegraph_source_graph = subcommands.add_parser(
        "codegraph-source-graph-index",
        help="Normalize existing CodeGraph JSON or SQLite evidence into source_graph_index.",
    )
    codegraph_source_graph.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Existing CodeGraph JSON output or SQLite database. No tool execution occurs.",
    )
    codegraph_source_graph.add_argument(
        "--input-format",
        choices=("json", "sqlite"),
        required=True,
        help="Input artifact format to normalize.",
    )
    codegraph_source_graph.add_argument(
        "--output",
        type=Path,
        help="Optional path where source_graph_index JSON is written.",
    )
    codegraph_source_graph.add_argument(
        "--source-repository",
        help="Optional source repository URL recorded in normalized provenance.",
    )
    codegraph_source_graph.add_argument(
        "--source-revision",
        help="Optional source revision recorded in normalized provenance.",
    )
    codegraph_source_graph.add_argument(
        "--source-target-kind",
        choices=("repository", "folder", "file"),
        default="repository",
        help="Harvest source target kind. Default: repository.",
    )
    codegraph_source_graph.add_argument(
        "--source-target-path",
        default=".",
        help="Harvest source target path. Default: .",
    )
    codegraph_source_graph.add_argument(
        "--analyzer-version",
        help="Optional CodeGraph analyzer version recorded in trust provenance.",
    )
    codegraph_source_graph.add_argument(
        "--executable",
        type=Path,
        help="Optional pre-provisioned CodeGraph executable path to digest, not run.",
    )
    codegraph_source_graph.add_argument(
        "--max-nodes",
        type=int,
        default=CODEGRAPH_DEFAULT_MAX_NODES,
        help=f"Maximum normalized nodes to include. Default: {CODEGRAPH_DEFAULT_MAX_NODES}.",
    )
    codegraph_source_graph.add_argument(
        "--max-edges",
        type=int,
        default=CODEGRAPH_DEFAULT_MAX_EDGES,
        help=f"Maximum normalized edges to include. Default: {CODEGRAPH_DEFAULT_MAX_EDGES}.",
    )
    codegraph_source_graph.set_defaults(func=run_codegraph_source_graph_index)

    codegraph_compatibility = subcommands.add_parser(
        "codegraph-compatibility-report",
        help="Validate pinned CodeGraph fixture compatibility without indexing repositories.",
    )
    codegraph_compatibility.add_argument(
        "--fixture",
        type=Path,
        required=True,
        help="Pinned CodeGraph compatibility fixture JSON.",
    )
    codegraph_compatibility.add_argument(
        "--output",
        type=Path,
        help="Optional path where compatibility report JSON is written.",
    )
    codegraph_compatibility.add_argument(
        "--executable",
        type=Path,
        help="Optional pre-provisioned CodeGraph executable to version-probe.",
    )
    codegraph_compatibility.add_argument(
        "--timeout-seconds",
        type=int,
        default=5,
        help="Timeout for optional executable version probe. Default: 5.",
    )
    codegraph_compatibility.set_defaults(func=run_codegraph_compatibility_report)

    accepted_diff = subcommands.add_parser(
        "accepted-candidate-diff-report",
        help="Build accepted-vs-candidate package metadata diff report.",
    )
    accepted_diff.add_argument(
        "--accepted-root",
        type=Path,
        required=True,
        help="Accepted package source root for diff input.",
    )
    accepted_diff.add_argument(
        "--candidates-root",
        type=Path,
        required=True,
        help="Candidate package root for diff input.",
    )
    accepted_diff.add_argument(
        "--output",
        type=Path,
        help="Optional path where accepted/candidate diff report JSON is written.",
    )
    accepted_diff.set_defaults(func=run_accepted_candidate_diff_report)

    accepted_candidate_impact = subcommands.add_parser(
        "accepted-candidate-impact-classification-report",
        help=("Build bucketed accepted-vs-candidate update impact classification report."),
    )
    accepted_candidate_impact.add_argument(
        "--accepted-root",
        type=Path,
        required=True,
        help="Accepted package source root for impact input.",
    )
    accepted_candidate_impact.add_argument(
        "--candidates-root",
        type=Path,
        required=True,
        help="Candidate package root for impact input.",
    )
    accepted_candidate_impact.add_argument(
        "--output",
        type=Path,
        help="Optional path where accepted/candidate impact report JSON is written.",
    )
    accepted_candidate_impact.set_defaults(func=run_accepted_candidate_impact_report)

    accepted_package_update_proposal = subcommands.add_parser(
        "accepted-package-update-proposal",
        help="Build a PR-ready SpecPM update proposal payload for a reviewed candidate.",
    )
    accepted_package_update_proposal.add_argument(
        "candidate",
        type=Path,
        help="Reviewed candidate directory containing specpm.yaml.",
    )
    accepted_package_update_proposal.add_argument(
        "--accepted-root",
        type=Path,
        required=True,
        help="Accepted package source root used for latest accepted comparison.",
    )
    accepted_package_update_proposal.add_argument(
        "--output",
        type=Path,
        help="Optional path where proposal JSON payload is written.",
    )
    accepted_package_update_proposal.add_argument(
        "--proposal-body",
        type=Path,
        help="Optional path for generated markdown proposal body.",
    )
    accepted_package_update_proposal.add_argument(
        "--skip-validation",
        action="store_true",
        help=(
            "Skip SpecPM validation. Intended only for CI smoke contexts and tests "
            "that need deterministic pre-validation artifacts."
        ),
    )
    accepted_package_update_proposal.add_argument(
        "--update-kind",
        choices=sorted({"upstream_revision", "metadata_errata", "correction"}),
        help="Override update kind when reviewer context is known.",
    )
    accepted_package_update_proposal.add_argument(
        "--allow-correction",
        action="store_true",
        help=(
            "Allow updates that target an already-accepted package version. "
            "Must be paired with --correction-note."
        ),
    )
    accepted_package_update_proposal.add_argument(
        "--correction-note",
        action="append",
        default=[],
        help="Correction rationale note. Repeatable. Required when --allow-correction is set.",
    )
    accepted_package_update_proposal.add_argument(
        "--reviewer-notes",
        action="append",
        default=[],
        help="Optional reviewer note for this proposal (repeatable).",
    )
    accepted_package_update_proposal.add_argument(
        "--specpm-command",
        default="specpm",
        help="SpecPM validation command. Default: specpm.",
    )
    accepted_package_update_proposal.add_argument(
        "--specpm-pythonpath",
        help="Optional PYTHONPATH prefix for local SpecPM checkout.",
    )
    accepted_package_update_proposal.set_defaults(func=run_accepted_package_update_proposal)

    smoke_triage = subcommands.add_parser(
        "smoke-triage-summary",
        help="Build a compact local smoke triage summary from existing report JSON files.",
    )
    smoke_triage.add_argument(
        "--batch-validation",
        type=Path,
        required=True,
        help="Path to batch-validation.json.",
    )
    smoke_triage.add_argument(
        "--governance-claims",
        type=Path,
        required=True,
        help="Path to governance-claims.json.",
    )
    smoke_triage.add_argument(
        "--namespace-upstream",
        type=Path,
        required=True,
        help="Path to namespace-upstream.json.",
    )
    smoke_triage.add_argument(
        "--license-provenance",
        type=Path,
        required=True,
        help="Path to license-provenance.json.",
    )
    smoke_triage.add_argument(
        "--output",
        type=Path,
        help="Optional path where local smoke triage summary JSON is written.",
    )
    smoke_triage.set_defaults(func=run_smoke_triage_summary)

    xyflow_package_set_smoke = subcommands.add_parser(
        "xyflow-package-set-smoke",
        help="Run the local synthetic xyflow package-set smoke scenario.",
    )
    xyflow_package_set_smoke.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Empty output directory where the smoke fixture and artifacts are written.",
    )
    xyflow_package_set_smoke.set_defaults(func=run_xyflow_package_set_smoke_command)

    quality_report = subcommands.add_parser(
        "quality-report",
        help=(
            "Build a structured quality report for a real-repository refinement "
            "validation run from an existing execution report JSON."
        ),
    )
    quality_report.add_argument(
        "--run-report",
        type=Path,
        required=True,
        help="Path to the execution report JSON produced by the P15-T2 runner.",
    )
    quality_report.add_argument(
        "--candidates-root",
        type=Path,
        help=(
            "Override the candidate output root directory used to locate "
            "per-package artifact files. Defaults to the 'out' field in the "
            "run report."
        ),
    )
    quality_report.add_argument(
        "--notes",
        action="append",
        default=[],
        metavar="id=PKG,notes=TEXT",
        help=(
            "Human-review note for one package in the form 'id=<pkg_id>,notes=<text>'. "
            "May be repeated for multiple packages. Alternatively pass a single "
            "@<path> argument to read a JSON file mapping package ids to notes."
        ),
    )
    quality_report.add_argument(
        "--output",
        type=Path,
        help="Optional path where quality report JSON is written.",
    )
    quality_report.set_defaults(func=run_quality_report)

    calibration_matrix = subcommands.add_parser(
        "author-ready-calibration-matrix",
        help=(
            "Build an author-ready calibration matrix from an existing "
            "real-repository quality report."
        ),
    )
    calibration_matrix.add_argument(
        "--quality-report",
        type=Path,
        required=True,
        help="Path to SpecHarvesterRealRepositoryQualityReport JSON.",
    )
    calibration_matrix.add_argument(
        "--author-notes",
        type=Path,
        help=(
            "Optional JSON file mapping package ids to estimated author edits, "
            "edit categories, notes, and generator follow-up reasons."
        ),
    )
    calibration_matrix.add_argument(
        "--output",
        type=Path,
        help="Optional path where calibration matrix JSON is written.",
    )
    calibration_matrix.set_defaults(func=run_author_ready_calibration_matrix)

    return parser


def run_collect_local(args: argparse.Namespace) -> int:
    snapshot = collect_local_repository(
        HarvestOptions(
            source=args.source,
            repository=args.repository,
            revision=args.revision,
            target=args.target,
            max_file_bytes=args.max_file_bytes,
        )
    )
    args.out.mkdir(parents=True, exist_ok=True)
    output_path = args.out / "harvest.json"
    output_path.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "ok",
                "output": str(output_path),
                "target": snapshot["source"]["target"],
                "fileCount": snapshot["summary"]["fileCount"],
                "skippedFileCount": snapshot["summary"]["skippedFileCount"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def run_collect_batch(args: argparse.Namespace) -> int:
    result = collect_batch_snapshots(
        BatchCollectOptions(
            inputs=args.inputs,
            out=args.out,
            selected_ids=tuple(args.select),
            max_file_bytes=args.max_file_bytes,
            report=args.report,
            strict_public=not args.relaxed_private,
            emit_interface_indexes=args.emit_interface_indexes,
            analyzer_cache_dir=args.analyzer_cache_dir,
            emit_workspace_inventory=args.emit_workspace_inventory,
            parser_profile_id=args.parser_profile_id,
        )
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if result.get("status") == "error" else 0


def run_autonomous_candidate_batch_cli(args: argparse.Namespace) -> int:
    try:
        result = run_autonomous_candidate_batch(
            AutonomousCandidateBatchOptions(
                inputs=args.inputs,
                out=args.out,
                selected_ids=tuple(args.select),
                max_file_bytes=args.max_file_bytes,
                strict_public=not args.relaxed_private,
                analyzer_cache_dir=args.analyzer_cache_dir,
                parser_profile_id=args.parser_profile_id,
                role_profile=args.role_profile,
                roles=tuple(args.role),
                skip_ai=args.skip_ai,
                lm_studio_base_url=args.lm_studio_base_url,
                lm_studio_model=args.lm_studio_model,
                provider_name=args.provider_name,
                json_repair_max_attempts=args.json_repair_max_attempts,
                apply_ai_enrichment=args.apply_ai_enrichment,
                repository_profile_selection=args.repository_profile_selection,
                repository_plugin_applicability=args.repository_plugin_applicability,
            )
        )
    except ValueError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "passed" else 1


def run_draft(args: argparse.Namespace) -> int:
    result = draft_spec_package(
        DraftOptions(
            snapshot=args.snapshot,
            out=args.out,
            package_id=args.package_id,
            name=args.name,
            version=args.version,
            author=args.author,
            interface_index=args.interface_index,
        )
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_draft_package_set(args: argparse.Namespace) -> int:
    result = draft_package_set(
        PackageSetDraftOptions(
            inventory=args.inventory,
            out=args.out,
            version=args.version,
            author=args.author,
            roles=tuple(args.role),
            role_profile=args.role_profile,
        )
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_render_spec_site(args: argparse.Namespace) -> int:
    result = render_static_spec_site(
        StaticSpecRendererOptions(candidate=args.candidate, output=args.output)
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "ok" else 1


def run_render_package_set_site(args: argparse.Namespace) -> int:
    result = render_static_package_set_site(
        StaticPackageSetRendererOptions(bundle_set=args.bundle_set, output=args.output)
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "ok" else 1


def run_preflight_candidate_bundle(args: argparse.Namespace) -> int:
    result = run_candidate_bundle_preflight(
        CandidateBundlePreflightOptions(candidate=args.candidate)
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "passed" else 1


def run_preflight_bundle_set(args: argparse.Namespace) -> int:
    result = run_bundle_set_preflight(BundleSetPreflightOptions(bundle_set=args.bundle_set))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "passed" else 1


def run_package_set_handoff_proposal(args: argparse.Namespace) -> int:
    result = build_package_set_handoff_proposal(
        PackageSetHandoffProposalOptions(bundle_set=args.bundle_set, viewer=args.viewer)
    )
    if args.output is not None:
        write_package_set_handoff_proposal(args.output, result)
    if args.proposal_body is not None:
        write_package_set_handoff_proposal_markdown(args.proposal_body, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_selected_candidate_handoff_proposal(args: argparse.Namespace) -> int:
    result = build_selected_candidate_handoff_proposal(
        SelectedCandidateHandoffProposalOptions(
            selected_handoff_dry_run=args.selected_handoff_dry_run,
            candidate_root=args.candidate_root,
            preflight_root=args.preflight_root,
            viewer_root=args.viewer_root,
        )
    )
    if args.output is not None:
        write_selected_candidate_handoff_proposal(args.output, result)
    if args.proposal_body is not None:
        write_selected_candidate_handoff_proposal_markdown(args.proposal_body, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_fresh_candidate_refresh_run(args: argparse.Namespace) -> int:
    result = build_fresh_candidate_refresh_run(
        FreshCandidateRefreshRunOptions(
            bundle_set=args.bundle_set,
            fresh_generated_root=args.fresh_generated_root,
            source_repository=args.source_repository,
            source_revision=args.source_revision,
            run_label=args.run_label,
        )
    )
    if args.output is not None:
        write_fresh_candidate_refresh_run(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_baseline_submission_handoff(args: argparse.Namespace) -> int:
    try:
        result = build_baseline_submission_handoff(
            BaselineSubmissionHandoffOptions(
                fresh_candidate_refresh_run=args.fresh_candidate_refresh_run,
                specpm_prepare_report=args.specpm_prepare_report,
            )
        )
    except ValueError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, indent=2))
        return 2
    if args.output is not None:
        write_baseline_submission_handoff(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_package_set_ai_draft_proposal(args: argparse.Namespace) -> int:
    options = PackageSetAIDraftProposalOptions(
        inventory=args.inventory,
        source_checkout=args.source_checkout,
        provider_base_url=args.provider_base_url,
        provider_name=args.provider_name,
        model=args.model,
        model_output=args.model_output,
        timeout_seconds=args.timeout_seconds,
        max_output_tokens=args.max_output_tokens,
        temperature=args.temperature,
        json_repair_max_attempts=args.json_repair_max_attempts,
    )
    if args.request_output is not None:
        write_package_set_ai_draft_request(
            args.request_output,
            package_set_ai_draft_request(options),
        )
    if args.output is None and args.provider_base_url is None and args.model_output is None:
        result = {
            "status": "request_prepared",
            "requestOutput": str(args.request_output) if args.request_output else None,
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    result = build_package_set_ai_draft_proposal(options)
    if args.output is not None:
        write_package_set_ai_draft_proposal(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] in {"completed", "warning"} else 1


def run_package_set_ai_enrichment(args: argparse.Namespace) -> int:
    options = PackageSetAIEnrichmentOptions(
        bundle_set=args.bundle_set,
        source_checkout=args.source_checkout,
        provider_base_url=args.provider_base_url,
        provider_name=args.provider_name,
        model=args.model,
        model_output=args.model_output,
        timeout_seconds=args.timeout_seconds,
        max_output_tokens=args.max_output_tokens,
        temperature=args.temperature,
        json_repair_max_attempts=args.json_repair_max_attempts,
    )
    if args.request_output is not None:
        write_model_request_records(args.request_output, model_request_records(options))
    if args.output is None and args.provider_base_url is None and args.model_output is None:
        result = {
            "status": "request_prepared",
            "requestOutput": str(args.request_output) if args.request_output else None,
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    result = build_package_set_ai_enrichment_proposal(options)
    if args.output is not None:
        write_package_set_ai_enrichment_proposal(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] in {"completed", "warning"} else 1


def run_apply_ai_enrichment_proposal(args: argparse.Namespace) -> int:
    try:
        result = build_ai_enrichment_candidate_patch(
            AIEnrichmentCandidatePatchOptions(
                proposal=args.proposal,
                candidate=args.candidate,
                output=args.output,
                package_id=args.package_id,
                report=args.report,
            )
        )
    except ValueError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_codegraph_source_graph_index(args: argparse.Namespace) -> int:
    try:
        result = build_codegraph_source_graph_index(
            CodeGraphSourceGraphOptions(
                input=args.input,
                input_format=args.input_format,
                source_repository=args.source_repository,
                source_revision=args.source_revision,
                source_target_kind=args.source_target_kind,
                source_target_path=args.source_target_path,
                analyzer_version=args.analyzer_version,
                executable=args.executable,
                max_nodes=args.max_nodes,
                max_edges=args.max_edges,
            )
        )
    except ValueError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, indent=2))
        return 2
    if args.output is not None:
        write_codegraph_source_graph_index(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_codegraph_compatibility_report(args: argparse.Namespace) -> int:
    try:
        result = build_codegraph_compatibility_report(
            CodeGraphCompatibilityOptions(
                fixture=args.fixture,
                executable=args.executable,
                timeout_seconds=args.timeout_seconds,
            )
        )
    except ValueError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, indent=2))
        return 2
    if args.output is not None:
        write_codegraph_compatibility_report(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "passed" else 1


def run_promote(args: argparse.Namespace) -> int:
    result = promote_candidate(
        PromoteOptions(
            candidate=args.candidate,
            accepted_root=args.accepted_root,
            manifest=args.manifest,
            manifest_entry_path=args.manifest_entry_path,
            package_subdir=args.package_subdir,
            specpm_command=args.specpm_command,
            specpm_pythonpath=args.specpm_pythonpath,
            skip_validation=args.skip_validation,
            force=args.force,
        )
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_source_manifests(args: argparse.Namespace) -> int:
    repositories = read_repository_source_manifests(
        args.inputs,
        include_disabled=args.include_disabled,
    )
    print(
        json.dumps(
            {
                "status": "ok",
                "input": str(args.inputs),
                "repositoryCount": len(repositories),
                "repositories": repositories,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def run_repository_profile_detect(args: argparse.Namespace) -> int:
    repository = repository_identity_from_args(args)
    payload = build_repository_profile_detection(
        RepositoryProfileDetectionOptions(
            repository=repository,
            selection=args.selection,
            evidence_paths=tuple(args.evidence_path),
        )
    )
    if args.output is not None:
        write_repository_profile_detection(args.output, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def repository_identity_from_args(args: argparse.Namespace) -> RepositoryIdentity:
    if args.source_manifest is not None:
        return repository_identity_from_source_manifest(
            args.source_manifest,
            source_id=args.source_id,
            declared_repository_profile=args.declared_repository_profile,
        )

    if not args.repository_id:
        raise ValueError("--repository-id is required without --source-manifest")
    if not args.repository_url:
        raise ValueError("--repository-url is required without --source-manifest")
    if (args.ref is None) == (args.revision is None):
        raise ValueError("Exactly one of --ref or --revision is required without --source-manifest")
    return RepositoryIdentity(
        repository_id=args.repository_id,
        repository_url=args.repository_url,
        ref=args.ref,
        revision=args.revision,
        source_manifest_path=None,
        source_manifest_entry_id=args.repository_id,
        declared_repository_profile=args.declared_repository_profile,
    )


def run_governance_report(args: argparse.Namespace) -> int:
    if args.accepted_root is None and args.candidates_root is None:
        raise ValueError("At least one of --accepted-root or --candidates-root must be set.")

    result = build_duplicate_claim_report(
        accepted_root=args.accepted_root,
        candidates_root=args.candidates_root,
    )
    if args.output is not None:
        write_governance_report(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_namespace_upstream_report(args: argparse.Namespace) -> int:
    if args.accepted_root is None and args.candidates_root is None:
        raise ValueError("At least one of --accepted-root or --candidates-root must be set.")

    result = build_namespace_upstream_report(
        accepted_root=args.accepted_root,
        candidates_root=args.candidates_root,
    )
    if args.output is not None:
        write_namespace_upstream_report(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_license_provenance_report(args: argparse.Namespace) -> int:
    if args.accepted_root is None and args.candidates_root is None:
        raise ValueError("At least one of --accepted-root or --candidates-root must be set.")

    result = build_license_provenance_risk_report(
        accepted_root=args.accepted_root,
        candidates_root=args.candidates_root,
    )
    if args.output is not None:
        write_license_provenance_report(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_accepted_candidate_diff_report(args: argparse.Namespace) -> int:
    result = build_accepted_candidate_diff_report(
        accepted_root=args.accepted_root,
        candidates_root=args.candidates_root,
    )
    if args.output is not None:
        write_accepted_candidate_diff_report(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_accepted_candidate_impact_report(args: argparse.Namespace) -> int:
    result = build_accepted_candidate_impact_report(
        accepted_root=args.accepted_root,
        candidates_root=args.candidates_root,
    )
    if args.output is not None:
        write_accepted_candidate_impact_report(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_accepted_package_update_proposal(args: argparse.Namespace) -> int:
    result = build_accepted_package_update_proposal(
        AcceptedPackageUpdateProposalOptions(
            candidate=args.candidate,
            accepted_root=args.accepted_root,
            specpm_command=args.specpm_command,
            specpm_pythonpath=args.specpm_pythonpath,
            skip_validation=args.skip_validation,
            update_kind=args.update_kind,
            allow_correction=args.allow_correction,
            correction_notes=tuple(args.correction_note),
            reviewer_notes=tuple(args.reviewer_notes),
        )
    )
    if args.output is not None:
        write_accepted_package_update_proposal(args.output, result)
    if args.proposal_body is not None:
        body = build_accepted_package_update_proposal_markdown(result)
        write_accepted_package_update_proposal_markdown(args.proposal_body, body)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_smoke_triage_summary(args: argparse.Namespace) -> int:
    result = build_smoke_triage_summary(
        batch_validation=args.batch_validation,
        governance_claims=args.governance_claims,
        namespace_upstream=args.namespace_upstream,
        license_provenance=args.license_provenance,
    )
    if args.output is not None:
        write_smoke_triage_summary(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_xyflow_package_set_smoke_command(args: argparse.Namespace) -> int:
    result = run_xyflow_package_set_smoke(XyflowPackageSetSmokeOptions(output=args.output))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "passed" else 1


def run_quality_report(args: argparse.Namespace) -> int:
    try:
        run_report_text = args.run_report.read_text(encoding="utf-8")
        run_report = json.loads(run_report_text)
    except OSError as exc:
        print(
            json.dumps(
                {"status": "error", "message": f"Cannot read run report: {exc}"},
                indent=2,
            )
        )
        return 2
    except json.JSONDecodeError as exc:
        print(
            json.dumps(
                {"status": "error", "message": f"Invalid run report JSON: {exc.msg}"},
                indent=2,
            )
        )
        return 2
    if not isinstance(run_report, dict):
        print(
            json.dumps(
                {"status": "error", "message": "Run report must be a JSON object"},
                indent=2,
            )
        )
        return 2

    try:
        human_notes = _parse_quality_report_notes(args.notes)
    except ValueError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, indent=2))
        return 2
    result = build_quality_report(
        run_report,
        candidates_root=args.candidates_root,
        run_report_path=args.run_report,
        human_notes=human_notes,
    )
    if args.output is not None:
        write_quality_report(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def run_author_ready_calibration_matrix(args: argparse.Namespace) -> int:
    try:
        quality_report = _read_json_object(args.quality_report, "quality report")
    except ValueError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, indent=2))
        return 2

    try:
        author_notes = (
            _read_json_object(args.author_notes, "author notes")
            if args.author_notes is not None
            else {}
        )
    except ValueError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, indent=2))
        return 2

    result = build_author_ready_calibration_matrix(
        quality_report,
        author_notes=author_notes,
        quality_report_path=args.quality_report,
    )
    if args.output is not None:
        write_author_ready_calibration_matrix(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def _read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Cannot read {label}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid {label} JSON: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{label.capitalize()} must be a JSON object")
    return data


def _parse_quality_report_notes(raw_notes: list[str]) -> dict[str, str]:
    """Parse ``--notes`` arguments into a mapping of package id → notes text.

    Accepts either:
    - ``id=<pkg_id>,notes=<text>`` pairs (one per ``--notes`` flag), or
    - a single ``@<path>`` argument pointing to a JSON file mapping ids to notes.
    """
    if not raw_notes:
        return {}

    # Single @file shorthand
    if len(raw_notes) == 1 and raw_notes[0].startswith("@"):
        notes_path = Path(raw_notes[0][1:])
        try:
            data = json.loads(notes_path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise ValueError(f"Cannot read notes file: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid notes JSON: {exc.msg}") from exc
        if isinstance(data, dict):
            return {str(k): str(v) for k, v in data.items()}
        raise ValueError("Notes file must be a JSON object mapping package ids to notes")

    notes: dict[str, str] = {}
    for entry in raw_notes:
        # Split on the first occurrence of ",notes=" so that commas inside
        # the notes text are preserved correctly.
        sep = ",notes="
        sep_idx = entry.find(sep)
        if sep_idx != -1:
            head = entry[:sep_idx]
            text = entry[sep_idx + len(sep) :]
        else:
            head = entry
            text = ""
        pkg_id = ""
        for part in head.split(","):
            if part.startswith("id="):
                pkg_id = part[3:]
        if pkg_id:
            notes[pkg_id] = text
    return notes


def run_prepare_accepted_manifest_entry(args: argparse.Namespace) -> int:
    result = prepare_accepted_manifest_entry(
        PrepareAcceptedManifestEntryOptions(
            candidate=args.candidate,
            manifest=args.manifest,
            manifest_entry_path=args.manifest_entry_path,
            manifest_entry_prefix=args.manifest_entry_prefix,
            package_subdir=args.package_subdir,
        )
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
