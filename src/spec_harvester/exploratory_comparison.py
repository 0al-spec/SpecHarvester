"""Offline P56 review handoff; original and historical bytes stay separate."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import tarfile
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from urllib.parse import quote

import yaml

from spec_harvester.static_spec_renderer import (
    StaticSpecRendererOptions,
    render_static_spec_site,
)

STYLE = """
*{box-sizing:border-box}body{margin:0;color:#20252a;background:#f7f8fa;
font:15px/1.5 system-ui,sans-serif;letter-spacing:0}header,main{padding:16px 24px}
h1{font-size:24px;margin:0 0 8px}h2{font-size:19px;margin:8px 0}h3{font-size:16px}
a{color:#075d9a;text-underline-offset:3px}nav{display:flex;gap:16px;flex-wrap:wrap}
header{border-bottom:1px solid #ccd2d9;background:white}p{margin:8px 0}
.comparison{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px}
.comparison section{min-width:0}iframe{width:100%;height:72vh;border:1px solid #bcc6cd;
background:white}pre{white-space:pre-wrap;overflow-wrap:anywhere;
font:14px/1.6 ui-monospace,monospace}
code,dd,li,p{overflow-wrap:anywhere}details{border-top:1px solid #d5dce1;padding:10px 0}
summary{cursor:pointer;font-weight:600}dl{display:grid;
grid-template-columns:minmax(100px,22%) minmax(0,1fr);gap:8px}
dt{font-weight:600}dd{margin:0;min-width:0}ul{padding-left:22px}
.warning{border-left:3px solid #a55e00;padding:4px 12px;background:#fff5de}
.muted{color:#53606b}.metadata{font-size:13px}.files{columns:2}
@media(max-width:800px){.comparison{grid-template-columns:1fr}header,main{padding:12px}
iframe{height:65vh}.files{columns:1}dl{grid-template-columns:1fr}}
"""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_path(value: str) -> str:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or any(p in (".", "..", "") for p in value.split("/")):
        raise ValueError("unsafe_path")
    if "\\" in value or ":" in value:
        raise ValueError("unsafe_path")
    return value


def escaped(value: object) -> str:
    return html.escape(str(value), quote=True)


def structured(value: object) -> str:
    if isinstance(value, dict):
        return (
            "<dl>"
            + "".join(f"<dt>{escaped(k)}</dt><dd>{structured(v)}</dd>" for k, v in value.items())
            + "</dl>"
        )
    if isinstance(value, list):
        return "<ul>" + "".join(f"<li>{structured(v)}</li>" for v in value) + "</ul>"
    return escaped(value if value is not None else "Not provided")


def page(title: str, body: str) -> str:
    return (
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; '
        "style-src 'unsafe-inline'; frame-src 'self'; base-uri 'none'; form-action 'none'\">"
        f"<title>{escaped(title)}</title><style>{STYLE}</style>"
        f"<body>{body}</body></html>"
    )


class FrozenArchive:
    def __init__(self, path: Path, expected: str):
        self.path, self.expected = path, expected

    def read(self, selected: dict[str, str], *, exact: bool = False) -> dict[str, bytes]:
        if self.path.is_symlink() or self.path.stat().st_size > 32 * 1024 * 1024:
            raise ValueError("unsafe_archive")
        if digest(self.path.read_bytes()) != self.expected:
            raise ValueError("archive_digest_mismatch")
        found, seen, size = {}, set(), 0
        with tarfile.open(self.path) as archive:
            for member in archive:
                name = safe_path(member.name.rstrip("/") if member.isdir() else member.name)
                if name in seen or not (member.isfile() or member.isdir()):
                    raise ValueError("unsafe_archive_member")
                seen.add(name)
                size += member.size
                if size > 512 * 1024 * 1024 or len(seen) > 50000:
                    raise ValueError("archive_budget_exceeded")
                if member.isfile() and name in selected:
                    data = archive.extractfile(member).read()
                    if digest(data) != selected[name]:
                        raise ValueError("member_digest_mismatch")
                    found[name] = data
                elif exact and member.isfile():
                    raise ValueError("unexpected_archive_member")
        if found.keys() != selected.keys():
            raise ValueError("missing_archive_member")
        return found


class ExploratoryComparison:
    def __init__(self, repository: Path, output: Path):
        self.repository, self.output = repository.resolve(), output.absolute()

    def write(self) -> dict:
        if self.output.exists() or self.output.is_symlink():
            raise ValueError("output_must_not_exist")
        if self.output.resolve().is_relative_to(self.repository):
            raise ValueError("output_must_be_outside_repository")
        evidence = self.repository / "SPECS/EVIDENCE/P56-T4"
        report = json.loads((evidence / "generation-report.json").read_text())
        lock_bytes = (evidence / "baseline-lock.json").read_bytes()
        preparation_bytes = (evidence / "preparation.json").read_bytes()
        if (
            digest(lock_bytes) != report["baselineLockSha256"]
            or digest(preparation_bytes) != report["preparationSha256"]
        ):
            raise ValueError("input_digest_mismatch")
        lock, preparation = json.loads(lock_bytes), json.loads(preparation_bytes)
        rows = report["repositories"]
        ids = [safe_path(row["repositoryId"]) for row in rows]
        if len(ids) != 5 or len(set(ids)) != 5 or any("/" in key for key in ids):
            raise ValueError("invalid_five_target_set")
        for row in rows:
            for field in ("errorCount", "warningCount"):
                if type(row.get(field)) is not int or row[field] < 0:
                    raise ValueError("invalid_diagnostic_count")
        originals = FrozenArchive(
            evidence / safe_path(report["archive"]["path"]), report["archive"]["sha256"]
        ).read(report["archive"]["members"], exact=True)
        benchmark = json.loads(
            (self.repository / "SPECS/EVIDENCE/P56-T1/benchmark.json").read_text()
        )
        expected = {r["repository"]: r["revision"] for r in benchmark["repositories"]}
        if {r["repository"]: r["revision"] for r in rows} != expected:
            raise ValueError("source_identity_mismatch")
        for row, source in zip(rows, preparation["repositories"], strict=True):
            key = row["repositoryId"]
            if row["repository"] != source["repository"] or row["revision"] != source["revision"]:
                raise ValueError("source_identity_mismatch")
            prefix = f"records/{key}/original/candidate/"
            files = {
                p[len(prefix) :]: digest(d) for p, d in originals.items() if p.startswith(prefix)
            }
            if (
                files != row["files"]
                or digest(json.dumps(files, sort_keys=True, separators=(",", ":")).encode())
                != row["candidateSha256"]
            ):
                raise ValueError("candidate_identity_mismatch")
            if digest(originals[f"records/{key}/readme/README.md"]) != source["readmeSha256"]:
                raise ValueError("readme_identity_mismatch")
        selected = {key: {} for key in lock["archives"]}
        for key in ids:
            prior = lock["repositories"].get(key)
            if prior is None:
                continue
            for path, sha in prior["candidateFiles"].items():
                selected[prior["candidateArchive"]][prior["candidateMemberPrefix"] + path] = sha
            selected[prior["semanticArchive"]][prior["semanticMember"]] = prior[
                "semanticRecordSha256"
            ]
        baselines = {
            key: FrozenArchive(self.repository / safe_path(item["path"]), item["sha256"]).read(
                selected[key]
            )
            for key, item in lock["archives"].items()
        }
        # All inputs verify before any review output is emitted.
        self.output.mkdir(parents=True)
        catalog = []
        for row, source in zip(rows, preparation["repositories"], strict=True):
            key = row["repositoryId"]
            root = self.output / key
            root.mkdir()
            prefix = f"records/{key}/original/candidate/"
            candidate = {
                p[len(prefix) :]: data for p, data in originals.items() if p.startswith(prefix)
            }
            self.package(root / "new", candidate, "New v2 candidate")
            readme = originals[f"records/{key}/readme/README.md"]
            (root / "README.md").write_bytes(readme)
            (root / "readme.html").write_text(
                page(
                    "Pinned README",
                    "<main><h1>Pinned README</h1>"
                    f"<p>{escaped(row['repository'])} @ <code>{escaped(row['revision'])}</code></p>"
                    '<a href="README.md" download>Original README</a>'
                    f"<pre>{escaped(readme.decode())}</pre></main>",
                )
            )
            prior = lock["repositories"].get(key)
            count = self.prior(root, prior, baselines)
            nav = "".join(f'<a href="../{item}/index.html">{escaped(item)}</a>' for item in ids)
            findings = row["sourceIntegrityFindings"]
            notes = "".join(f"<li>{escaped(v)}</li>" for v in findings)
            warnings = f"{row['errorCount']} SpecPM errors / {row['warningCount']} warnings"
            body = f"<header><nav>{nav}</nav><h1>{escaped(row['repository'])}</h1>"
            body += (
                f'<p class="metadata">{escaped(row["revision"])} | '
                f"{escaped(row['model'])} / medium | {escaped(warnings)} | Human review pending</p>"
            )
            body += f"<p>{escaped(row['requestedScope'])}</p>"
            if notes:
                body += (
                    f'<details class="warning"><summary>{len(findings)} evidence review findings'
                    f"</summary><ul>{notes}</ul></details>"
                )
            body += (
                '<p class="muted">Preview only. Historical boundaries and source bundles differ; '
                "no controlled model comparison.</p></header>"
            )
            body += '<main class="comparison"><section><h2>New v2 candidate</h2><nav>'
            body += (
                '<a href="new/complete.html" target="new">Complete spec</a>'
                '<a href="new/index.html" target="new">Viewer overview</a>'
            )
            body += '<a href="new/files.html" target="new">Original files</a></nav>'
            body += (
                '<iframe title="New v2 candidate" name="new" src="new/complete.html" '
                'sandbox="allow-scripts allow-downloads"></iframe></section>'
                "<section><h2>Reference</h2><nav>"
                '<a href="readme.html" target="reference">Pinned README</a>'
                '<a href="prior.html" target="reference">Retained packages</a>'
                '<a href="semantic.html" target="reference">Semantic proposal</a></nav>'
                '<iframe title="Reference surface" name="reference" src="readme.html" '
                'sandbox="allow-scripts allow-downloads"></iframe></section></main>'
            )
            (root / "index.html").write_text(page(row["repository"], body))
            catalog.append(
                {
                    "repository": row["repository"],
                    "repositoryId": key,
                    "revision": row["revision"],
                    "candidateSha256": row["candidateSha256"],
                    "readmeSha256": source["readmeSha256"],
                    "retainedPackageCount": count,
                    "humanReview": "pending",
                    "path": f"{key}/index.html",
                }
            )
        links = "".join(
            f'<li><a href="{r["path"]}">{escaped(r["repository"])}</a></li>' for r in catalog
        )
        (self.output / "index.html").write_text(
            page(
                "P56 comparison",
                "<main><h1>P56 package comparison</h1>"
                f"<p>Five original candidates. Human review pending.</p><ul>{links}</ul></main>",
            )
        )
        result = {
            "protocol": report["protocol"],
            "generationReportSha256": digest((evidence / "generation-report.json").read_bytes()),
            "baselineLockSha256": report["baselineLockSha256"],
            "repositories": catalog,
            "publicationAuthorized": False,
            "humanReview": "pending",
        }
        (self.output / "comparison.json").write_text(json.dumps(result, indent=2) + "\n")
        questions = [
            "Purpose and intended consumer?",
            "Getting started with the public interface?",
            "Useful operations and configuration?",
            "Limitations, prerequisites and side effects?",
            "Pinned evidence supporting consequential claims?",
        ]
        worksheet = {
            "protocol": report["protocol"],
            "humanReview": "pending",
            "reviewer": None,
            "repositories": [
                {
                    "repositoryId": r["repositoryId"],
                    "reviewMinutes": None,
                    "editMinutes": None,
                    "proposedEdits": [],
                    "humanDisposition": None,
                    "surfaces": {
                        surface: {
                            "status": "not_reviewed",
                            "sourceLookups": [],
                            "answers": [
                                {"question": q, "verdict": None, "reason": None} for q in questions
                            ],
                        }
                        for surface in (
                            "new_candidate",
                            "pinned_readme",
                            "retained_packages",
                            "semantic_proposal",
                        )
                    },
                }
                for r in catalog
            ],
        }
        (self.output / "human-review-template.json").write_text(
            json.dumps(worksheet, indent=2) + "\n"
        )
        return result

    def package(self, output: Path, files: dict[str, bytes], label: str) -> None:
        with TemporaryDirectory(prefix="p56-render-") as temporary:
            candidate = Path(temporary)
            for path, data in files.items():
                target = candidate / safe_path(path)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            result = render_static_spec_site(StaticSpecRendererOptions(candidate, output))
            if result["status"] != "ok":
                raise ValueError("retained_package_render_failed")
        # Keep the existing viewer local, including its optional font stylesheet.
        css = output / "assets/spec-renderer.css"
        stylesheet = css.read_text()
        if stylesheet.startswith('@import url("https://fonts.googleapis.com/'):
            css.write_text(stylesheet.partition("\n")[2])
        index = output / "index.html"
        policy = (
            '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; '
            "script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; "
            "base-uri 'none'; form-action 'none'\">"
        )
        index.write_text(index.read_text().replace("<head>", "<head>" + policy, 1))
        docs, links = [], []
        for path, data in sorted(files.items()):
            raw = output / "original" / safe_path(path)
            raw.parent.mkdir(parents=True, exist_ok=True)
            raw.write_bytes(data)
            view = output / "text" / (path + ".html")
            view.parent.mkdir(parents=True, exist_ok=True)
            view.write_text(
                page(
                    path,
                    f"<main><h1>{escaped(path)}</h1><pre>{escaped(data.decode())}</pre></main>",
                )
            )
            links.append(
                f'<li><a href="text/{quote(path)}.html">{escaped(path)}</a> '
                f'<a href="original/{quote(path)}" download>Original</a></li>'
            )
            if path.endswith(".spec.yaml"):
                spec = yaml.safe_load(data)
                docs.append(
                    f"<h2>{escaped(path)}</h2><h3>Purpose</h3>" + structured(spec.get("intent"))
                )
                for field, value in spec.items():
                    if field != "intent":
                        opened = " open" if field in ("scope", "provides") else ""
                        docs.append(
                            f"<details{opened}><summary>{escaped(field)}</summary>"
                            + structured(value)
                            + "</details>"
                        )
        if "specpm.yaml" in files:
            docs.append(
                "<details><summary>Package manifest: specpm.yaml</summary>"
                + structured(yaml.safe_load(files["specpm.yaml"]))
                + "</details>"
            )
        (output / "files.html").write_text(
            page(label, "<main><h1>Original files</h1><ul>" + "".join(links) + "</ul></main>")
        )
        (output / "complete.html").write_text(
            page(label, f"<main><h1>{escaped(label)}</h1>" + "".join(docs) + "</main>")
        )

    def prior(self, root: Path, prior: dict | None, baselines: dict) -> int:
        if prior is None:
            for name in ("prior", "semantic"):
                (root / f"{name}.html").write_text(
                    page("Unavailable", "<main><h1>Retained baseline unavailable</h1></main>")
                )
            return 0
        prefix = prior["candidateMemberPrefix"]
        files = {
            p[len(prefix) :]: data
            for p, data in baselines[prior["candidateArchive"]].items()
            if p.startswith(prefix)
        }
        manifests = sorted(p for p in files if p.endswith("/specpm.yaml"))
        links = []
        for number, manifest in enumerate(manifests):
            member_prefix = manifest.removesuffix("specpm.yaml")
            subset = {
                p[len(member_prefix) :]: data
                for p, data in files.items()
                if p.startswith(member_prefix)
            }
            self.package(root / "retained" / str(number), subset, member_prefix.rstrip("/"))
            links.append(
                f"<li>{escaped(member_prefix)}: "
                f'<a href="retained/{number}/complete.html">Complete spec</a> / '
                f'<a href="retained/{number}/index.html">Viewer</a> / '
                f'<a href="retained/{number}/files.html">Files</a></li>'
            )
        note = structured(
            {k: prior[k] for k in ("candidateProducer", "retainedRevision", "caveats")}
        )
        collection_links = []
        for path, data in sorted(files.items()):
            raw = root / "retained-files" / safe_path(path)
            raw.parent.mkdir(parents=True, exist_ok=True)
            raw.write_bytes(data)
            collection_links.append(
                f'<li><a href="retained-files/{quote(path)}" download>{escaped(path)}</a></li>'
            )
        (root / "prior.html").write_text(
            page(
                "Retained packages",
                "<main><h1>Retained packages</h1>"
                + note
                + "<ul>"
                + "".join(links)
                + "</ul><details><summary>Complete original retained file set</summary><ul>"
                + "".join(collection_links)
                + "</ul></details></main>",
            )
        )
        semantic = baselines[prior["semanticArchive"]][prior["semanticMember"]]
        (root / "semantic.json").write_bytes(semantic)
        data = json.loads(semantic)
        status = (
            "Rejected historical proposal; no portable proposal"
            if "portableProposal" in data and data["portableProposal"] is None
            else "Historical proposal only; not applied"
        )
        body = f'<main><h1>Semantic proposal</h1><p class="warning">{escaped(status)}</p>'
        body += (
            f"<p>{escaped(prior['semanticModel'])} | {escaped(prior['retainedRevision'])}</p>"
            + structured(prior["caveats"])
        )
        proposal = data.get("proposal") or data.get("semanticPass", {}).get("proposal")
        body += "<h2>Proposed content</h2>" + structured(proposal)
        body += (
            "<details><summary>Full technical record</summary>"
            + structured(data)
            + '</details><a href="semantic.json" download>Original semantic record</a></main>'
        )
        (root / "semantic.html").write_text(page("Semantic proposal", body))
        return len(manifests)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(ExploratoryComparison(args.repository, args.output).write(), indent=2))


if __name__ == "__main__":
    main()
