from __future__ import annotations

INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>SpecHarvester Spec Viewer</title>
  <meta
    name="description"
    content="Static browser preview for generated SpecPM candidate packages."
  />
  <link rel="stylesheet" href="./assets/spec-renderer.css" />
</head>
<body>
  <header class="shell-header">
    <div>
      <p class="eyebrow">SpecHarvester Static Preview</p>
      <h1 id="package-title">Loading candidate package...</h1>
      <p id="package-summary" class="lede"></p>
    </div>
    <div id="status-card" class="status-card">Loading</div>
  </header>

  <main class="layout">
    <aside class="sidebar">
      <div class="panel">
        <h2>Package</h2>
        <div id="package-facts" class="facts"></div>
      </div>
      <div class="panel">
        <h2>Capabilities</h2>
        <div id="capability-list" class="token-list"></div>
      </div>
      <div class="panel">
        <h2>Intents</h2>
        <div id="intent-list" class="token-list"></div>
      </div>
    </aside>

    <section class="content">
      <section class="panel">
        <div class="panel-head">
          <h2>Boundary Specs</h2>
          <span id="spec-count" class="pill">0</span>
        </div>
        <div id="spec-list" class="spec-list"></div>
      </section>

      <section class="panel">
        <div class="panel-head">
          <h2>Diagnostics</h2>
          <span id="diagnostic-count" class="pill">0</span>
        </div>
        <div id="diagnostic-list" class="diagnostic-list"></div>
      </section>

      <section class="panel raw-panel">
        <div class="panel-head">
          <h2>Normalized JSON</h2>
          <a href="./spec-package.json" class="button">Open JSON</a>
        </div>
        <pre id="raw-json">{}</pre>
      </section>
    </section>
  </main>

  <script id="spec-package-data" type="application/json">__SPEC_PACKAGE_JSON__</script>
  <script src="./assets/spec-renderer.js" defer></script>
</body>
</html>
"""


VIEWER_CSS = """:root {
  color-scheme: light;
  --ink: #18221f;
  --muted: #60716b;
  --paper: #f6f0e6;
  --panel: #fffaf0;
  --line: #dfd1bd;
  --accent: #c5532c;
  --accent-dark: #7b2f1d;
  --ok: #24724f;
  --warn: #8a5a00;
  --shadow: 0 24px 80px rgba(57, 41, 24, 0.14);
  font-family: "Avenir Next", "Trebuchet MS", sans-serif;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  color: var(--ink);
  background:
    radial-gradient(circle at top left, rgba(197, 83, 44, 0.18), transparent 32rem),
    linear-gradient(135deg, #f9f1df 0%, #ecdfc8 45%, #f8f5ee 100%);
}

.shell-header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 2rem;
  align-items: end;
  padding: 4rem clamp(1rem, 4vw, 4rem) 2rem;
}

.eyebrow {
  margin: 0 0 0.5rem;
  color: var(--accent-dark);
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

h1,
h2,
h3,
p {
  margin-top: 0;
}

h1 {
  max-width: 960px;
  margin-bottom: 0.75rem;
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(2.4rem, 8vw, 6.5rem);
  line-height: 0.9;
  letter-spacing: -0.06em;
}

h2 {
  margin-bottom: 1rem;
  font-size: 1rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

h3 {
  margin-bottom: 0.45rem;
  font-size: 1.1rem;
}

.lede {
  max-width: 780px;
  color: var(--muted);
  font-size: 1.08rem;
  line-height: 1.6;
}

.layout {
  display: grid;
  grid-template-columns: minmax(260px, 0.35fr) minmax(0, 1fr);
  gap: 1.25rem;
  padding: 0 clamp(1rem, 4vw, 4rem) 4rem;
}

.sidebar,
.content {
  display: grid;
  gap: 1.25rem;
  align-content: start;
  min-width: 0;
}

.panel,
.status-card {
  border: 1px solid var(--line);
  border-radius: 28px;
  background: rgba(255, 250, 240, 0.84);
  box-shadow: var(--shadow);
}

.panel {
  padding: 1.35rem;
  min-width: 0;
}

.status-card {
  min-width: 180px;
  padding: 1rem 1.25rem;
  color: var(--ok);
  font-weight: 800;
  text-align: center;
}

.status-card.warn {
  color: var(--warn);
}

.panel-head {
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
}

.facts {
  display: grid;
  gap: 0.75rem;
}

.fact {
  display: grid;
  gap: 0.2rem;
  padding-bottom: 0.7rem;
  border-bottom: 1px dashed var(--line);
}

.fact span {
  color: var(--muted);
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
}

.fact strong {
  overflow-wrap: anywhere;
}

.pill,
.token,
.button {
  display: inline-flex;
  border: 1px solid rgba(197, 83, 44, 0.24);
  border-radius: 999px;
  background: rgba(197, 83, 44, 0.08);
  color: var(--accent-dark);
  font-weight: 700;
}

.pill {
  padding: 0.25rem 0.65rem;
  font-size: 0.78rem;
}

.token-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
}

.token,
.button {
  padding: 0.45rem 0.7rem;
  text-decoration: none;
}

.token {
  max-width: 100%;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.spec-list,
.diagnostic-list {
  display: grid;
  gap: 1rem;
}

.spec-card,
.diagnostic-card {
  border: 1px solid var(--line);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.42);
  padding: 1rem;
}

.section-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.85rem;
  margin-top: 1rem;
}

.section-box {
  border-radius: 16px;
  background: rgba(246, 240, 230, 0.72);
  padding: 0.85rem;
  min-width: 0;
}

.section-box ul {
  margin: 0.4rem 0 0;
  padding-left: 1.1rem;
}

.muted,
.empty {
  color: var(--muted);
}

pre {
  overflow: auto;
  max-height: 36rem;
  margin: 0;
  border-radius: 18px;
  background: #18221f;
  color: #f8f5ee;
  padding: 1rem;
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 0.86rem;
  line-height: 1.55;
}

@media (max-width: 860px) {
  .shell-header,
  .layout {
    grid-template-columns: 1fr;
  }

  .shell-header {
    padding-top: 2rem;
  }

  .status-card {
    text-align: left;
  }

  .section-grid {
    grid-template-columns: 1fr;
  }
}
"""


VIEWER_JS = """document.addEventListener("DOMContentLoaded", () => {
  loadSpecPackage().catch((error) => {
    document.querySelector("#status-card").textContent = `Load failed: ${error.message}`;
    document.querySelector("#status-card").classList.add("warn");
  });
});

async function loadSpecPackage() {
  const embedded = embeddedPayload();
  if (embedded) {
    renderPackage(embedded);
    return;
  }
  const response = await fetch("./spec-package.json", { headers: { Accept: "application/json" } });
  if (!response.ok) {
    throw new Error(`spec-package.json returned HTTP ${response.status}`);
  }
  const payload = await response.json();
  renderPackage(payload);
}

function embeddedPayload() {
  const node = document.querySelector("#spec-package-data");
  const text = node?.textContent?.trim();
  if (!text) {
    return null;
  }
  return JSON.parse(text);
}

function renderPackage(payload) {
  const pkg = payload.package || {};
  const metadata = pkg.metadata || {};
  document.querySelector("#package-title").textContent = metadata.name || pkg.id || "SpecPackage";
  document.querySelector("#package-summary").textContent = metadata.summary || "";

  const statusCard = document.querySelector("#status-card");
  const validation = payload.validation || {};
  statusCard.textContent = validationLabel(validation);
  statusCard.classList.toggle(
    "warn",
    validation.status !== "ok" && validation.status !== "not_provided"
  );

  document.querySelector("#package-facts").innerHTML = facts([
    ["Package ID", pkg.id],
    ["Version", pkg.version],
    ["License", metadata.license],
    ["Manifest", pkg.manifestPath],
    ["SpecPM API", pkg.apiVersion],
    ["Preview Only", String(pkg.previewOnly)]
  ]);
  document.querySelector("#capability-list").innerHTML = tokens(pkg.capabilities || []);
  document.querySelector("#intent-list").innerHTML = tokens(pkg.intents || []);

  const specs = payload.specs || [];
  document.querySelector("#spec-count").textContent = String(specs.length);
  document.querySelector("#spec-list").innerHTML = specs.length
    ? specs.map(renderSpecCard).join("")
    : `<div class="empty">No BoundarySpec files were loaded.</div>`;

  const diagnostics = payload.diagnostics || [];
  document.querySelector("#diagnostic-count").textContent = String(diagnostics.length);
  document.querySelector("#diagnostic-list").innerHTML = diagnostics.length
    ? diagnostics.map(renderDiagnosticCard).join("")
    : `<div class="empty">No renderer diagnostics.</div>`;

  document.querySelector("#raw-json").textContent = JSON.stringify(payload, null, 2);
}

function renderSpecCard(spec) {
  const metadata = spec.metadata || {};
  const intent = spec.intent || {};
  return `
    <article class="spec-card">
      <p class="eyebrow">${escapeHtml(spec.path || "spec")}</p>
      <h3>${escapeHtml(metadata.title || metadata.id || "BoundarySpec")}</h3>
      <p class="muted">${escapeHtml(intent.summary || "")}</p>
      <div class="section-grid">
        ${sectionBox("Scope Includes", spec.scope?.includes || [])}
        ${sectionBox("Scope Excludes", spec.scope?.excludes || [])}
        ${sectionBox("Interfaces Inbound", interfaceNames(spec.interfaces?.inbound || []))}
        ${sectionBox("Evidence", evidenceNames(spec.evidence || []))}
        ${sectionBox("Effects", effectNames(spec.effects?.sideEffects || []))}
        ${sectionBox("Constraints", constraintNames(spec.constraints || []))}
      </div>
    </article>
  `;
}

function renderDiagnosticCard(diagnostic) {
  return `
    <article class="diagnostic-card">
      <p class="eyebrow">
        ${escapeHtml(diagnostic.severity || "info")} /
        ${escapeHtml(diagnostic.code || "diagnostic")}
      </p>
      <strong>${escapeHtml(diagnostic.path || "candidate")}</strong>
      <p class="muted">${escapeHtml(diagnostic.message || "")}</p>
    </article>
  `;
}

function validationLabel(validation) {
  if (validation.status === "ok") {
    return "SpecPM validation: ok";
  }
  if (validation.status === "not_provided") {
    return "SpecPM validation: not provided";
  }
  return `Validation: ${validation.status || "unknown"}`;
}

function facts(rows) {
  return rows.map(([label, value]) => `
    <div class="fact">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value || "")}</strong>
    </div>
  `).join("");
}

function tokens(values) {
  if (!values.length) {
    return `<span class="empty">None declared.</span>`;
  }
  return values.map((value) => `<span class="token">${escapeHtml(value)}</span>`).join("");
}

function sectionBox(title, values) {
  const list = values.length
    ? `<ul>${values.map((value) => `<li>${escapeHtml(value)}</li>`).join("")}</ul>`
    : `<p class="empty">None declared.</p>`;
  return `<div class="section-box"><strong>${escapeHtml(title)}</strong>${list}</div>`;
}

function interfaceNames(values) {
  return values.map((item) => item.name || item.id || item.summary || "interface");
}

function evidenceNames(values) {
  return values.map((item) => item.id || item.kind || item.summary || "evidence");
}

function effectNames(values) {
  return values.map((item) => item.kind || item.id || item.summary || "effect");
}

function constraintNames(values) {
  return values.map((item) => item.id || item.level || item.statement || "constraint");
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}
"""
