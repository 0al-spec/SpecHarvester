from __future__ import annotations

import json
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.batch_collection import BatchCollectOptions, collect_batch_snapshots
from spec_harvester.drafter import DraftOptions, draft_spec_package
from spec_harvester.governance_reports import build_duplicate_claim_report
from spec_harvester.license_provenance_reports import build_license_provenance_risk_report
from spec_harvester.namespace_reports import build_namespace_upstream_report
from spec_harvester.smoke_triage import build_smoke_triage_summary

EXPECTED_POPULAR_WEB_INTENTS = {
    "intent.web.framework_surface",
    "intent.web.http_routing",
    "intent.web.middleware_pipeline",
    "intent.web.request_response_context",
    "intent.api.contract_surface",
    "intent.developer.tooling_surface",
    "intent.workflow.automation_pipeline",
    "intent.documentation.knowledge_base",
}


@dataclass(frozen=True)
class PopularSmokeFixture:
    repository_id: str
    package_id: str
    package_name: str
    repository: str
    files: dict[str, str]


def test_popular_repository_smoke_promotes_flask_and_gin_contracts(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    checkouts = tmp_path / "checkouts"
    candidates = tmp_path / "candidates"
    reports = tmp_path / "reports"
    inputs.mkdir()
    checkouts.mkdir()
    reports.mkdir()
    fixtures = popular_smoke_fixtures()

    for fixture in fixtures:
        write_fixture(checkouts / fixture.repository_id, fixture.files)
    write_source_manifest(inputs / "repositories.yml", checkouts, fixtures)

    batch_report_path = reports / "popular-batch-validation.json"
    result = collect_batch_snapshots(
        BatchCollectOptions(
            inputs=inputs,
            out=candidates,
            report=batch_report_path,
            emit_interface_indexes=True,
            analyzer_cache_dir=tmp_path / "analyzer-cache",
        )
    )

    assert result["status"] == "ok"
    assert result["collectedCount"] == 3
    assert result["skippedCount"] == 0

    batch_report = read_json(batch_report_path)
    assert batch_report["status"] == "ok"
    assert batch_report["summary"]["errorCount"] == 0
    assert batch_report["summary"]["warningCount"] == 0

    collected = {item["id"]: item for item in result["collected"]}
    assert_popular_collection_record(
        collected["flask"],
        expected_plan_id="spec_harvester.python_public_api",
        expected_language="python",
        expected_ecosystem="pypi",
        expected_license_path="LICENSE.txt",
    )
    assert_popular_collection_record(
        collected["gin"],
        expected_plan_id="spec_harvester.go_public_api",
        expected_language="go",
        expected_ecosystem="go",
        expected_license_path="LICENSE",
    )
    assert_manifest_only_go_module(collected["go-module-manifest-only"])

    draft_results = [
        draft_spec_package(
            DraftOptions(
                snapshot=candidates / fixture.repository_id,
                out=candidates / fixture.repository_id,
                package_id=fixture.package_id,
                name=fixture.package_name,
            )
        )
        for fixture in fixtures
        if fixture.repository_id in {"flask", "gin"}
    ]
    for draft in draft_results:
        assert_popular_draft_contract(draft)

    governance_claims = write_json(
        reports / "popular-governance-claims.json",
        build_duplicate_claim_report(candidates_root=candidates),
    )
    namespace_upstream = write_json(
        reports / "popular-namespace-upstream.json",
        build_namespace_upstream_report(candidates_root=candidates),
    )
    license_provenance = write_json(
        reports / "popular-license-provenance.json",
        build_license_provenance_risk_report(candidates_root=candidates),
    )

    duplicate_report = read_json(governance_claims)
    assert duplicate_report["summary"]["records"] == 2
    assert duplicate_report["summary"]["duplicateIntentCount"] > 0
    assert duplicate_report["summary"]["issueCount"] == 0

    namespace_report = read_json(namespace_upstream)
    assert namespace_report["summary"]["records"] == 2
    assert namespace_report["summary"]["missingUpstreamCount"] == 0
    assert namespace_report["summary"]["upstreamMismatchCount"] == 0
    assert namespace_report["summary"]["issueCount"] == 0

    license_report = read_json(license_provenance)
    assert license_report["summary"]["records"] == 2
    assert license_report["summary"]["riskCounts"]["high"] == 0
    assert license_report["summary"]["issuesByCode"] == {}

    triage = build_smoke_triage_summary(
        batch_validation=batch_report_path,
        governance_claims=governance_claims,
        namespace_upstream=namespace_upstream,
        license_provenance=license_provenance,
    )
    assert triage["kind"] == "SpecHarvesterLocalSmokeTriageSummary"
    assert triage["summary"]["batchErrorCount"] == 0
    assert triage["summary"]["batchWarningCount"] == 0
    assert triage["summary"]["namespaceIssueCount"] == 0
    assert triage["summary"]["licenseIssueCount"] == 0
    assert triage["reports"]["batchValidation"]["path"] == str(batch_report_path)


def assert_popular_collection_record(
    record: dict[str, Any],
    *,
    expected_plan_id: str,
    expected_language: str,
    expected_ecosystem: str,
    expected_license_path: str,
) -> None:
    snapshot = read_json(Path(record["output"]))
    profile = snapshot["projectProfile"]
    assert {item["id"] for item in profile["languages"]} == {expected_language}
    assert {item["id"] for item in profile["ecosystems"]} == {expected_ecosystem}
    assert {item["id"] for item in profile["analyzerPlan"]} == {expected_plan_id}
    assert {item["id"]: item["status"] for item in profile["analyzerPlan"]} == {
        expected_plan_id: "recommended"
    }
    assert snapshot["summary"]["licenseFileCount"] == 1
    assert any(
        item["kind"] == "license" and item["path"] == expected_license_path
        for item in snapshot["files"]
    )

    interface_record = record["interfaceIndex"]
    assert interface_record["status"] == "complete"
    assert interface_record["plannedAnalyzerIds"] == [expected_plan_id]
    assert interface_record["executedAnalyzerIds"] == [expected_plan_id]
    assert interface_record["diagnostics"] == []
    assert Path(interface_record["output"]).exists()

    index = read_json(Path(interface_record["output"]))
    assert index["kind"] == "SpecHarvesterPublicInterfaceIndex"
    assert index["summary"]["status"] == "complete"
    assert index["summary"]["packageCount"] == 1
    assert index["summary"]["symbolCount"] > 0
    assert len(index["analyzers"]) == 1
    assert all(analyzer["execution"] == "none" for analyzer in index["analyzers"])
    assert all(analyzer["networkAccess"] == "none" for analyzer in index["analyzers"])
    assert all(analyzer["packageScripts"] == "not_run" for analyzer in index["analyzers"])


def assert_manifest_only_go_module(record: dict[str, Any]) -> None:
    snapshot = read_json(Path(record["output"]))
    profile = snapshot["projectProfile"]
    assert {item["id"] for item in profile["languages"]} == {"go"}
    assert {item["id"] for item in profile["ecosystems"]} == {"go"}
    assert {item["id"]: item["status"] for item in profile["analyzerPlan"]} == {
        "spec_harvester.go_public_api": "manifest_only"
    }
    assert record["interfaceIndex"]["status"] == "skipped"
    assert record["interfaceIndex"]["executedAnalyzerIds"] == []
    assert "output" not in record["interfaceIndex"]


def assert_popular_draft_contract(draft: dict[str, Any]) -> None:
    manifest_text = Path(draft["manifest"]).read_text(encoding="utf-8")
    spec_text = Path(draft["spec"]).read_text(encoding="utf-8")
    interface_index = Path(draft["interfaceIndex"])

    assert interface_index.exists()
    assert "preview_only: true" in manifest_text
    for intent in EXPECTED_POPULAR_WEB_INTENTS:
        assert intent in manifest_text
        assert intent in spec_text

    assert "intent.package.public_repository_metadata" not in manifest_text
    assert "kind: public_interface_index" in spec_text
    assert "artifactKind: SpecHarvesterPublicInterfaceIndex" in spec_text
    assert "id: semantic_intent_static_evidence" in spec_text
    assert "kind: unknown" not in spec_text
    assert "provides.capabilities.intentIds" not in spec_text
    assert "unknown_evidence_kind" not in spec_text
    assert "evidence_support_target_unknown" not in spec_text


def popular_smoke_fixtures() -> list[PopularSmokeFixture]:
    return [
        PopularSmokeFixture(
            repository_id="flask",
            package_id="flask.core",
            package_name="Flask",
            repository="https://github.com/pallets/flask",
            files={
                "README.md": popular_web_readme("Flask", "Blueprint"),
                "LICENSE.txt": (
                    "MIT License\nCopyright 2026 Example\nPermission is hereby granted.\n"
                ),
                "pyproject.toml": "[project]\nname = 'flask'\nversion = '3.0.0'\n",
                "src/flask/__init__.py": textwrap.dedent(
                    """
                    from .app import Flask
                    from .blueprints import Blueprint
                    from .ctx import RequestContext, session
                    from .json import jsonify

                    __all__ = ["Blueprint", "Flask", "RequestContext", "jsonify", "session"]
                    """
                ),
                "src/flask/app.py": textwrap.dedent(
                    """
                    class Flask:
                        def route(self, rule):
                            pass

                        def add_url_rule(self, rule, endpoint=None, view_func=None):
                            pass

                        def before_request(self, function):
                            pass

                        def after_request(self, function):
                            pass
                    """
                ),
                "src/flask/blueprints.py": textwrap.dedent(
                    """
                    class Blueprint:
                        def route(self, rule):
                            pass

                        def app_template_filter(self, name=None):
                            pass
                    """
                ),
                "src/flask/ctx.py": textwrap.dedent(
                    """
                    session = {}

                    class RequestContext:
                        def push(self):
                            pass

                        def pop(self):
                            pass
                    """
                ),
                "src/flask/json.py": textwrap.dedent(
                    """
                    def jsonify(*args, **kwargs):
                        return args or kwargs

                    def render_template(template_name, **context):
                        return template_name
                    """
                ),
            },
        ),
        PopularSmokeFixture(
            repository_id="gin",
            package_id="gin.core",
            package_name="Gin",
            repository="https://github.com/gin-gonic/gin",
            files={
                "README.md": popular_web_readme("Gin", "RouterGroup"),
                "LICENSE": "MIT License\nCopyright 2026 Example\nPermission is hereby granted.\n",
                "go.mod": "module github.com/gin-gonic/gin\n\ngo 1.24\n",
                "gin.go": textwrap.dedent(
                    """
                    package gin

                    type HandlerFunc func(*Context)
                    type HandlersChain []HandlerFunc
                    type Engine struct{}
                    type RouteInfo struct{}
                    type IRoutes interface {
                        Use(...HandlerFunc) IRoutes
                    }

                    func New() *Engine { return &Engine{} }
                    func Default() *Engine { return &Engine{} }
                    func (engine *Engine) ServeHTTP() {}
                    func (engine *Engine) Use(middleware ...HandlerFunc) IRoutes { return engine }
                    """
                ),
                "routergroup.go": textwrap.dedent(
                    """
                    package gin

                    type Context struct{}
                    type RouterGroup struct{}

                    func (group *RouterGroup) Handle(
                        method string,
                        path string,
                        handlers ...HandlerFunc,
                    ) IRoutes {
                        return group
                    }

                    func (group *RouterGroup) GET(path string, handlers ...HandlerFunc) IRoutes {
                        return group
                    }

                    func (context *Context) JSON(code int, obj any) {}
                    func (context *Context) BindJSON(obj any) error { return nil }
                    """
                ),
            },
        ),
        PopularSmokeFixture(
            repository_id="go-module-manifest-only",
            package_id="go_manifest.core",
            package_name="Go Manifest Only",
            repository="https://github.com/example/go-module-manifest-only",
            files={
                "README.md": "# Go Module Manifest Only\n",
                "LICENSE": "MIT License\nCopyright 2026 Example\nPermission is hereby granted.\n",
                "go.mod": "module github.com/example/go-module-manifest-only\n\ngo 1.24\n",
            },
        ),
    ]


def popular_web_readme(name: str, extra_term: str) -> str:
    return textwrap.dedent(
        f"""
        # {name}

        ## Web Framework

        {name} is a web framework with route, routes, routing, router, middleware,
        handlers, request context, application context, {extra_term}, JSON,
        templates, session, cookie, and response pipeline concepts.

        ## HTTP Routing

        The API contract exposes endpoints, request and response schemas, route
        handlers, URL rules, and router groups.

        ## Middleware Pipeline

        Middleware, before request hooks, after request hooks, handler chains,
        and response pipeline behavior are represented as public API concepts.

        ## Request Response Context

        Request context, application context, session, cookies, JSON, bind JSON,
        jsonify, render template, and templates are reviewable concepts.

        ## Developer Tooling

        CLI commands, configuration, SDK, plugin, and developer tooling docs are
        mentioned for intent extraction.

        ## Workflow Automation

        Workflow automation pipeline validation runs as commands and review tasks.

        ## Documentation Guide Reference

        Documentation, guide, reference, tutorial, and manual pages explain the API.
        """
    )


def write_fixture(root: Path, files: dict[str, str]) -> None:
    root.mkdir(parents=True)
    for relative_path, content in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.lstrip(), encoding="utf-8")


def write_source_manifest(
    path: Path,
    checkouts_root: Path,
    fixtures: list[PopularSmokeFixture],
) -> None:
    lines = ["repositories:"]
    for index, fixture in enumerate(fixtures, start=1):
        checkout = checkouts_root / fixture.repository_id
        lines.extend(
            [
                f"  - id: {fixture.repository_id}",
                f"    repository: {fixture.repository}",
                f"    revision: {index:040x}",
                f"    checkout: {json.dumps(str(checkout))}",
                f"    packageId: {fixture.package_id}",
                "    labels: [synthetic, popular-smoke]",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
