from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from spec_harvester.swift_text import strip_swift_comments

STRING_RE = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')
NAME_RE = re.compile(r"\bname\s*:\s*\"([^\"\\]*(?:\\.[^\"\\]*)*)\"")
PRODUCT_RE = re.compile(r"\bproduct\s*:\s*\.([A-Za-z][A-Za-z0-9_]*)")
PLATFORM_RE = re.compile(
    r"\b(?:platform|destinations|deploymentTargets)\s*:\s*(?:\[[^\]]*\])?\.([A-Za-z][A-Za-z0-9_]*)"
)
DOT_PLATFORM_RE = re.compile(r"\.([A-Za-z][A-Za-z0-9_]*)")


@dataclass(frozen=True)
class TuistManifestCall:
    name: str
    body: str


def parse_tuist_manifest(text: str, *, filename: str) -> dict[str, Any] | None:
    stripped = strip_swift_comments(text)
    manifest_kind = tuist_manifest_kind(filename)
    if manifest_kind is None:
        return None

    payload: dict[str, Any] = {
        "ecosystem": "tuist",
        "language": "swift",
        "manifest": manifest_kind,
    }

    root_call = first_call(stripped, root_call_name(manifest_kind))
    if root_call is not None:
        name = argument_name(root_call.body)
        if name is not None:
            payload["name"] = name

    if manifest_kind == "project":
        targets = tuist_targets(stripped)
        if targets:
            payload["targets"] = targets
            products = tuist_products(targets)
            if products:
                payload["products"] = products
            source_globs = sorted(
                {glob for target in targets for glob in target.get("sources", [])}
            )
            if source_globs:
                payload["sourceGlobs"] = source_globs
            resource_globs = sorted(
                {glob for target in targets for glob in target.get("resources", [])}
            )
            if resource_globs:
                payload["resourceGlobs"] = resource_globs
        if "name" not in payload and targets:
            payload["name"] = targets[0]["name"]

    if manifest_kind == "workspace" and root_call is not None:
        projects = string_argument_values(root_call.body, "projects")
        if projects:
            payload["projects"] = projects

    return payload if len(payload) > 3 else None


def tuist_manifest_kind(filename: str) -> str | None:
    if filename == "Project.swift":
        return "project"
    if filename == "Workspace.swift":
        return "workspace"
    if filename == "Tuist.swift":
        return "config"
    return None


def root_call_name(manifest_kind: str) -> str:
    if manifest_kind == "project":
        return "Project"
    if manifest_kind == "workspace":
        return "Workspace"
    return "Config"


def tuist_targets(text: str) -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = []
    for call in calls_named(text, ".target"):
        name = argument_name(call.body)
        if name is None:
            continue
        target: dict[str, Any] = {"name": name}
        product = argument_product(call.body)
        if product is not None:
            target["product"] = product
        platforms = argument_platforms(call.body)
        if platforms:
            target["platforms"] = platforms
        sources = string_argument_values(call.body, "sources")
        if sources:
            target["sources"] = sources
        resources = string_argument_values(call.body, "resources")
        if resources:
            target["resources"] = resources
        targets.append(target)
    return sorted(targets, key=lambda item: item["name"])


def tuist_products(targets: list[dict[str, Any]]) -> list[dict[str, str]]:
    products = [
        {"name": target["name"], "type": target["product"]}
        for target in targets
        if isinstance(target.get("product"), str)
    ]
    return sorted(products, key=lambda item: (item["type"], item["name"]))


def argument_name(body: str) -> str | None:
    match = NAME_RE.search(body)
    if match is None:
        return None
    return unescape_swift_string(match.group(1))


def argument_product(body: str) -> str | None:
    match = PRODUCT_RE.search(body)
    return match.group(1) if match is not None else None


def argument_platforms(body: str) -> list[str]:
    values: set[str] = set()
    for argument_name_value in ("platform", "destinations", "deploymentTargets"):
        value = argument_value(body, argument_name_value)
        if value is None:
            continue
        values.update(match.group(1) for match in DOT_PLATFORM_RE.finditer(value))
    if not values:
        values.update(match.group(1) for match in PLATFORM_RE.finditer(body))
    return sorted(values)


def string_argument_values(body: str, name: str) -> list[str]:
    value = argument_value(body, name)
    if value is None:
        return []
    included = {unescape_swift_string(match.group(1)) for match in STRING_RE.finditer(value)}
    excluded = excluded_string_values(value)
    return sorted(included - excluded)


def excluded_string_values(value: str) -> set[str]:
    excluding = argument_value(value, "excluding")
    if excluding is None:
        return set()
    return {unescape_swift_string(match.group(1)) for match in STRING_RE.finditer(excluding)}


def argument_value(body: str, name: str) -> str | None:
    match = re.search(rf"\b{re.escape(name)}\s*:", body)
    if match is None:
        return None
    start = match.end()
    end = top_level_argument_end(body, start)
    return body[start:end].strip()


def top_level_argument_end(text: str, start: int) -> int:
    depth = 0
    quote = False
    escape = False
    for index in range(start, len(text)):
        char = text[index]
        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
            continue
        if char in "([{":
            depth += 1
            continue
        if char in ")]}":
            if depth == 0:
                return index
            depth -= 1
            continue
        if char == "," and depth == 0:
            return index
    return len(text)


def first_call(text: str, name: str) -> TuistManifestCall | None:
    calls = calls_named(text, name)
    return calls[0] if calls else None


def calls_named(text: str, name: str) -> list[TuistManifestCall]:
    calls: list[TuistManifestCall] = []
    search_start = 0
    while True:
        start = text.find(f"{name}(", search_start)
        if start == -1:
            break
        open_index = start + len(name)
        close_index = matching_paren_index(text, open_index)
        if close_index is None:
            search_start = open_index + 1
            continue
        calls.append(TuistManifestCall(name=name, body=text[open_index + 1 : close_index]))
        search_start = close_index + 1
    return calls


def matching_paren_index(text: str, open_index: int) -> int | None:
    if open_index >= len(text) or text[open_index] != "(":
        return None
    depth = 0
    quote = False
    escape = False
    for index in range(open_index, len(text)):
        char = text[index]
        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
    return None


def unescape_swift_string(value: str) -> str:
    result: list[str] = []
    index = 0
    while index < len(value):
        char = value[index]
        if char != "\\":
            result.append(char)
            index += 1
            continue
        if index + 1 >= len(value):
            result.append(char)
            index += 1
            continue
        escaped = value[index + 1]
        simple_escape = {
            "0": "\0",
            "\\": "\\",
            "t": "\t",
            "n": "\n",
            "r": "\r",
            '"': '"',
            "'": "'",
        }.get(escaped)
        if simple_escape is not None:
            result.append(simple_escape)
            index += 2
            continue
        unicode_escape = swift_unicode_escape(value, index)
        if unicode_escape is not None:
            character, end = unicode_escape
            result.append(character)
            index = end
            continue
        result.append(f"\\{escaped}")
        index += 2
    return "".join(result)


def swift_unicode_escape(value: str, start: int) -> tuple[str, int] | None:
    if not value.startswith("\\u{", start):
        return None
    end = value.find("}", start + 3)
    if end == -1:
        return None
    digits = value[start + 3 : end]
    if not 1 <= len(digits) <= 8 or not re.fullmatch(r"[0-9A-Fa-f]+", digits):
        return None
    try:
        return chr(int(digits, 16)), end + 1
    except ValueError:
        return None
