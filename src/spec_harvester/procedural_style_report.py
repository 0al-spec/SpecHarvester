"""Deterministic procedural-style metrics for local Python source review."""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.architecture_lint import (
    SourceFile,
    scan_source_files,
    skipped_source_file_to_dict,
)

PROCEDURAL_STYLE_REPORT_KIND = "SpecHarvesterProceduralStyleReport"
PROCEDURAL_STYLE_SCHEMA_VERSION = 1
DEFAULT_PATHS = (Path("src/spec_harvester"),)
DEFAULT_LARGEST_FUNCTIONS_LIMIT = 10
DEFAULT_HOTSPOT_MIN_TOP_LEVEL_COUNT = 15
DEFAULT_HOTSPOT_MIN_TOP_LEVEL_SPAN = 300

TRUST_BOUNDARY_NOTES = [
    "Procedural style metrics read local Python source files only.",
    "No repository code execution, dependency installation, network access, or imports occur.",
    "The report is advisory by default and does not mutate source files.",
]


@dataclass(frozen=True)
class FunctionMetric:
    path: str
    name: str
    line: int
    span: int


def build_procedural_style_report(
    paths: list[Path] | None = None,
    *,
    hotspot_min_top_level_count: int = DEFAULT_HOTSPOT_MIN_TOP_LEVEL_COUNT,
    hotspot_min_top_level_span: int = DEFAULT_HOTSPOT_MIN_TOP_LEVEL_SPAN,
    largest_functions_limit: int = DEFAULT_LARGEST_FUNCTIONS_LIMIT,
) -> dict[str, Any]:
    if hotspot_min_top_level_count < 1:
        raise ValueError("--hotspot-min-top-level-count must be at least 1.")
    if hotspot_min_top_level_span < 1:
        raise ValueError("--hotspot-min-top-level-span must be at least 1.")
    if largest_functions_limit < 1:
        raise ValueError("--largest-functions-limit must be at least 1.")

    roots = paths or list(DEFAULT_PATHS)
    scan = scan_source_files(roots)
    file_metrics = [_file_metric(source) for source in scan.files]
    file_metrics.sort(key=lambda item: item["path"])

    largest_functions = _largest_top_level_functions(
        scan.files,
        limit=largest_functions_limit,
    )
    hotspots = _hotspots(
        file_metrics,
        min_top_level_count=hotspot_min_top_level_count,
        min_top_level_span=hotspot_min_top_level_span,
    )
    hotspots.sort(
        key=lambda item: (
            -item["topLevelFunctionSpan"],
            -item["topLevelFunctionCount"],
            item["path"],
        )
    )

    summary = {
        "pathCount": len(roots),
        "fileCount": len(scan.paths),
        "analyzedFileCount": len(scan.files),
        "skippedFileCount": len(scan.skipped_files),
        "topLevelFunctionCount": sum(item["topLevelFunctionCount"] for item in file_metrics),
        "topLevelFunctionSpan": sum(item["topLevelFunctionSpan"] for item in file_metrics),
        "methodCount": sum(item["methodCount"] for item in file_metrics),
        "methodSpan": sum(item["methodSpan"] for item in file_metrics),
        "classCount": sum(item["classCount"] for item in file_metrics),
        "behaviorRichClassCount": sum(item["behaviorRichClassCount"] for item in file_metrics),
        "dtoOnlyClassCount": sum(item["dtoOnlyClassCount"] for item in file_metrics),
        "exceptionLikeClassCount": sum(item["exceptionLikeClassCount"] for item in file_metrics),
        "hotspotCount": len(hotspots),
        "largestTopLevelFunctionCount": len(largest_functions),
        "hotspotPolicy": {
            "minTopLevelFunctionCount": hotspot_min_top_level_count,
            "minTopLevelFunctionSpan": hotspot_min_top_level_span,
        },
    }
    denominator = summary["topLevelFunctionSpan"] + summary["methodSpan"]
    summary["topLevelSpanShare"] = _ratio(summary["topLevelFunctionSpan"], denominator)
    summary["methodSpanShare"] = _ratio(summary["methodSpan"], denominator)

    return {
        "schemaVersion": PROCEDURAL_STYLE_SCHEMA_VERSION,
        "kind": PROCEDURAL_STYLE_REPORT_KIND,
        "status": "attention" if hotspots or scan.skipped_files else "ok",
        "summary": summary,
        "skippedFiles": [skipped_source_file_to_dict(skipped) for skipped in scan.skipped_files],
        "fileMetrics": file_metrics,
        "hotspots": hotspots,
        "largestTopLevelFunctions": [metric.__dict__ for metric in largest_functions],
        "trustBoundary": TRUST_BOUNDARY_NOTES,
    }


def write_procedural_style_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _file_metric(source: SourceFile) -> dict[str, Any]:
    top_level_functions = _top_level_functions(source.tree)
    classes = [node for node in source.tree.body if isinstance(node, ast.ClassDef)]
    class_summaries = [_class_summary(node) for node in classes]
    top_level_span = sum(_span(node) for node in top_level_functions)
    method_count = sum(item["methodCount"] for item in class_summaries)
    method_span = sum(item["methodSpan"] for item in class_summaries)

    denominator = top_level_span + method_span
    return {
        "path": source.path.as_posix(),
        "topLevelFunctionCount": len(top_level_functions),
        "topLevelFunctionSpan": top_level_span,
        "methodCount": method_count,
        "methodSpan": method_span,
        "classCount": len(classes),
        "behaviorRichClassCount": sum(1 for item in class_summaries if item["isBehaviorRich"]),
        "dtoOnlyClassCount": sum(1 for item in class_summaries if item["isDtoOnly"]),
        "exceptionLikeClassCount": sum(1 for item in class_summaries if item["isExceptionLike"]),
        "topLevelSpanShare": _ratio(top_level_span, denominator),
        "methodSpanShare": _ratio(method_span, denominator),
    }


def _class_summary(node: ast.ClassDef) -> dict[str, Any]:
    methods = [
        item for item in node.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    non_dunder_methods = [item for item in methods if not _is_dunder(item.name)]
    dataclass_like = any(
        _decorator_name(item).endswith("dataclass") for item in node.decorator_list
    )
    exception_like = _is_exception_like(node)
    return {
        "methodCount": len(methods),
        "methodSpan": sum(_span(item) for item in methods),
        "isBehaviorRich": len(non_dunder_methods) >= 2 and not exception_like,
        "isDtoOnly": dataclass_like and len(non_dunder_methods) == 0 and not exception_like,
        "isExceptionLike": exception_like,
    }


def _top_level_functions(tree: ast.AST) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    assert isinstance(tree, ast.Module)
    return [item for item in tree.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))]


def _largest_top_level_functions(files: list[SourceFile], *, limit: int) -> list[FunctionMetric]:
    metrics: list[FunctionMetric] = []
    for source in files:
        for node in _top_level_functions(source.tree):
            metrics.append(
                FunctionMetric(
                    path=source.path.as_posix(),
                    name=node.name,
                    line=node.lineno,
                    span=_span(node),
                )
            )
    metrics.sort(key=lambda item: (-item.span, item.path, item.line, item.name))
    return metrics[:limit]


def _hotspots(
    file_metrics: list[dict[str, Any]],
    *,
    min_top_level_count: int,
    min_top_level_span: int,
) -> list[dict[str, Any]]:
    results = []
    for item in file_metrics:
        if (
            item["topLevelFunctionCount"] >= min_top_level_count
            or item["topLevelFunctionSpan"] >= min_top_level_span
        ):
            results.append(item)
    return results


def _is_exception_like(node: ast.ClassDef) -> bool:
    if node.name.endswith(("Error", "Exception")):
        return True
    base_names = {_decorator_name(base) for base in node.bases}
    return any(name.endswith(("Error", "Exception", "BaseException")) for name in base_names)


def _decorator_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _decorator_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    if isinstance(node, ast.Call):
        return _decorator_name(node.func)
    return ""


def _is_dunder(name: str) -> bool:
    return name.startswith("__") and name.endswith("__")


def _span(node: ast.AST) -> int:
    return max(1, getattr(node, "end_lineno", 0) - getattr(node, "lineno", 1) + 1)


def _ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)
