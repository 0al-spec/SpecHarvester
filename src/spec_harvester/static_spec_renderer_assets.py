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
        <div class="reading-tools">
          <div>
            <label class="search-label" for="spec-search">Filter visible content</label>
            <input
              id="spec-search"
              class="search-input"
              type="search"
              placeholder="interface, evidence, intent..."
            />
          </div>
          <div class="button-row">
            <button id="expand-all" class="button" type="button">Expand all</button>
            <button id="collapse-all" class="button" type="button">Collapse all</button>
          </div>
          <nav id="spec-outline" class="outline"></nav>
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


VIEWER_CSS = """@import url("https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap");

:root {
  color-scheme: light;
  --ink: #0b0b0c;
  --paper: #f3f1ec;
  --paper-2: #e8e5dd;
  --rule: #1b1c1e;
  --rule-soft: rgba(11, 11, 12, 0.14);
  --muted: #55524b;
  --muted-2: #7a766d;
  --signal: oklch(74% 0.14 240);
  --signal-ink: oklch(46% 0.13 240);
  --warn: #8a5a00;
  --serif: "Instrument Serif", "Times New Roman", serif;
  --sans: "Inter", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
  font-family: var(--sans);
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  color: var(--ink);
  overflow-x: hidden;
  background:
    linear-gradient(to right, rgba(11, 11, 12, 0.045) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(11, 11, 12, 0.045) 1px, transparent 1px),
    radial-gradient(
      circle at 78% 12%,
      color-mix(in oklab, var(--signal) 22%, transparent),
      transparent 28rem
    ),
    var(--paper);
  background-size: 80px 80px, 80px 80px, auto, auto;
  font-size: 15px;
  line-height: 1.5;
  letter-spacing: -0.005em;
  -webkit-font-smoothing: antialiased;
}

.shell-header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 2rem;
  align-items: end;
  max-width: 1440px;
  margin: 0 auto;
  padding: 4.8rem clamp(1.25rem, 4vw, 3.5rem) 2.4rem;
  border-bottom: 1px solid var(--rule);
}

.eyebrow {
  display: flex;
  gap: 0.7rem;
  align-items: center;
  margin: 0 0 1.1rem;
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.68rem;
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.eyebrow::before {
  width: 28px;
  height: 1px;
  background: currentColor;
  content: "";
  opacity: 0.7;
}

h1,
h2,
h3,
p {
  margin-top: 0;
}

h1 {
  max-width: 960px;
  margin-bottom: 1rem;
  font-family: var(--serif);
  font-size: clamp(3.4rem, 7.5vw, 7.4rem);
  font-weight: 400;
  line-height: 0.96;
  letter-spacing: -0.025em;
}

h2 {
  margin-bottom: 1rem;
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.74rem;
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

h3 {
  margin-bottom: 0.45rem;
  font-size: 1.1rem;
}

.lede {
  max-width: 780px;
  color: var(--muted);
  font-size: 1.02rem;
  line-height: 1.6;
}

.layout {
  display: grid;
  grid-template-columns: minmax(260px, 0.35fr) minmax(0, 1fr);
  gap: 0;
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 clamp(1.25rem, 4vw, 3.5rem) 4rem;
}

.sidebar,
.content {
  display: grid;
  gap: 0;
  align-content: start;
  min-width: 0;
}

.sidebar {
  position: sticky;
  top: 0;
  max-height: 100vh;
  overflow: auto;
}

.panel,
.status-card {
  border: 1px solid var(--rule);
  background: color-mix(in oklab, var(--paper) 86%, white);
}

.panel {
  padding: 1.6rem;
  min-width: 0;
  border-top: 0;
}

.status-card {
  min-width: 180px;
  padding: 0.85rem 1rem;
  color: var(--signal-ink);
  font-family: var(--mono);
  font-size: 0.68rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-align: center;
  text-transform: uppercase;
}

.status-card.warn {
  color: var(--warn);
}

.content {
  border-left: 1px solid var(--rule);
}

.content .panel {
  border-left: 0;
}

.sidebar .panel + .panel,
.content .panel + .panel {
  border-top: 0;
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
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--rule-soft);
}

.fact span {
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.78rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.fact strong {
  overflow-wrap: anywhere;
}

.pill,
.token,
.button {
  display: inline-flex;
  border: 1px solid var(--rule-soft);
  border-radius: 0;
  background: color-mix(in oklab, var(--paper-2) 72%, transparent);
  color: var(--ink);
  font-family: var(--mono);
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.02em;
}

button.button {
  cursor: pointer;
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
  align-items: center;
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
  border-top: 1px solid var(--rule-soft);
  background: transparent;
  padding: 1.15rem 0 0;
}

.spec-card {
  scroll-margin-top: 1rem;
}

.spec-summary {
  display: grid;
  gap: 0.35rem;
  cursor: pointer;
  list-style: none;
}

.spec-summary::-webkit-details-marker,
.section-summary::-webkit-details-marker {
  display: none;
}

.spec-summary::before,
.section-summary::before {
  color: var(--signal-ink);
  font-family: var(--mono);
  font-size: 0.72rem;
  content: "+";
}

.spec-card[open] > .spec-summary::before,
.section-box[open] > .section-summary::before {
  content: "-";
}

.section-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.85rem;
  margin-top: 1rem;
}

.section-box {
  border-left: 1px solid var(--rule);
  background: color-mix(in oklab, var(--paper-2) 52%, transparent);
  padding: 0.9rem 1rem;
  min-width: 0;
}

.section-summary {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  gap: 0.55rem;
  align-items: center;
  cursor: pointer;
  list-style: none;
}

.count {
  color: var(--muted-2);
  font-family: var(--mono);
  font-size: 0.68rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.section-box ul {
  margin: 0.4rem 0 0;
  padding-left: 1.1rem;
}

.search-label {
  display: block;
  margin-bottom: 0.45rem;
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.search-input {
  width: 100%;
  border: 1px solid var(--rule);
  border-radius: 0;
  background: var(--paper);
  color: var(--ink);
  padding: 0.7rem 0.75rem;
  font: inherit;
}

.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin: 0;
}

.outline {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem 0.75rem;
  align-items: center;
}

.outline a {
  color: var(--ink);
  font-family: var(--mono);
  font-size: 0.72rem;
  overflow-wrap: anywhere;
  text-decoration: none;
}

.outline a:hover {
  color: var(--signal-ink);
}

.reading-tools {
  display: grid;
  grid-template-columns: minmax(16rem, 1fr) auto;
  gap: 0.8rem 1rem;
  align-items: end;
  margin: 0.35rem 0 1.15rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--rule-soft);
}

.reading-tools .outline {
  grid-column: 1 / -1;
}

.is-hidden {
  display: none;
}

.muted,
.empty {
  color: var(--muted);
}

pre {
  overflow: auto;
  max-height: 36rem;
  margin: 0;
  border: 1px solid var(--rule);
  background: var(--ink);
  color: var(--paper);
  padding: 1rem;
  font-family: var(--mono);
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

  .content {
    border-left: 0;
  }

  .sidebar {
    position: static;
    max-height: none;
  }

  .content .panel {
    border-left: 1px solid var(--rule);
  }

  .section-grid {
    grid-template-columns: 1fr;
  }

  .reading-tools {
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
  renderOutline(specs);
  bindReadingControls();

  const diagnostics = payload.diagnostics || [];
  document.querySelector("#diagnostic-count").textContent = String(diagnostics.length);
  document.querySelector("#diagnostic-list").innerHTML = diagnostics.length
    ? diagnostics.map(renderDiagnosticCard).join("")
    : `<div class="empty">No renderer diagnostics.</div>`;

  document.querySelector("#raw-json").textContent = JSON.stringify(payload, null, 2);
}

function renderSpecCard(spec, index) {
  const metadata = spec.metadata || {};
  const intent = spec.intent || {};
  const title = metadata.title || metadata.id || "BoundarySpec";
  const summary = intent.summary || "";
  const searchText = [
    spec.path,
    title,
    summary,
    ...(spec.scope?.includes || []),
    ...(spec.scope?.excludes || []),
    ...interfaceNames(spec.interfaces?.inbound || []),
    ...evidenceNames(spec.evidence || []),
    ...effectNames(spec.effects?.sideEffects || []),
    ...constraintNames(spec.constraints || [])
  ].join(" ");
  return `
    <details class="spec-card" id="spec-${index + 1}" open data-search="${escapeHtml(searchText)}">
      <summary class="spec-summary">
        <p class="eyebrow">${escapeHtml(spec.path || "spec")}</p>
        <h3>${escapeHtml(title)}</h3>
        <p class="muted">${escapeHtml(summary)}</p>
      </summary>
      <div class="section-grid">
        ${sectionBox("Scope Includes", spec.scope?.includes || [])}
        ${sectionBox("Scope Excludes", spec.scope?.excludes || [])}
        ${sectionBox("Interfaces Inbound", interfaceNames(spec.interfaces?.inbound || []))}
        ${sectionBox("Evidence", evidenceNames(spec.evidence || []))}
        ${sectionBox("Effects", effectNames(spec.effects?.sideEffects || []))}
        ${sectionBox("Constraints", constraintNames(spec.constraints || []))}
      </div>
    </details>
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
  return `
    <details class="section-box">
      <summary class="section-summary">
        <strong>${escapeHtml(title)}</strong>
        <span class="count">${values.length}</span>
      </summary>
      ${list}
    </details>
  `;
}

function renderOutline(specs) {
  const outline = document.querySelector("#spec-outline");
  outline.innerHTML = specs.length
    ? specs.map((spec, index) => {
      const metadata = spec.metadata || {};
      const title = metadata.title || metadata.id || spec.path || `Spec ${index + 1}`;
      return `<a href="#spec-${index + 1}">${escapeHtml(title)}</a>`;
    }).join("")
    : `<span class="empty">No specs loaded.</span>`;
}

function bindReadingControls() {
  const search = document.querySelector("#spec-search");
  const expand = document.querySelector("#expand-all");
  const collapse = document.querySelector("#collapse-all");

  search?.addEventListener("input", () => filterSpecs(search.value));
  expand?.addEventListener("click", () => toggleDetails(true));
  collapse?.addEventListener("click", () => toggleDetails(false));
}

function filterSpecs(query) {
  const normalized = query.trim().toLowerCase();
  document.querySelectorAll(".spec-card").forEach((card) => {
    const searchText = card.getAttribute("data-search")?.toLowerCase() || "";
    const visible = !normalized || searchText.includes(normalized);
    card.classList.toggle("is-hidden", !visible);
    if (visible && normalized) {
      card.open = true;
    }
  });
}

function toggleDetails(open) {
  document.querySelectorAll(".spec-card, .section-box").forEach((details) => {
    details.open = open;
  });
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
