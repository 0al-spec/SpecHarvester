# ruff: noqa: E501

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from spec_harvester.candidate_review_schema import load_candidate_review_schema

CATALOG_API_VERSION = "spec-harvester.candidate-review-catalog/v0"
CATALOG_KIND = "SpecHarvesterCandidateReviewCatalog"
CATALOG_AUTHORITY = "local_review_catalog_evidence_only"


@dataclass(frozen=True)
class LocalCandidateReviewBrowserOptions:
    catalog: Path
    output: Path
    details: Path | None = None


def _read_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read candidate review catalog: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("Candidate review catalog must be a JSON object")
    return payload


def load_local_candidate_review_catalog(path: Path) -> dict[str, Any]:
    catalog = _read_json_object(path)
    schema = load_candidate_review_schema()
    errors = list(Draft202012Validator(schema).iter_errors(catalog))
    if errors:
        raise ValueError(f"Candidate review catalog schema is invalid: {errors[0].message}")
    items = catalog.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("Candidate review catalog must contain at least one item")
    required = {
        "candidateId",
        "packetSha256",
        "reviewState",
        "readiness",
        "ecosystem",
        "packageShape",
        "warningCount",
        "corrected",
        "preflightStatus",
    }
    ids: set[str] = set()
    for item in items:
        if not isinstance(item, dict) or set(item) != required:
            raise ValueError("Candidate review catalog item shape is invalid")
        candidate_id = item["candidateId"]
        if not isinstance(candidate_id, str) or not candidate_id or candidate_id in ids:
            raise ValueError("Candidate review catalog identity is invalid")
        ids.add(candidate_id)
        if not isinstance(item["warningCount"], int) or item["warningCount"] < 0:
            raise ValueError("Candidate review catalog warning count is invalid")
        if not isinstance(item["corrected"], bool):
            raise ValueError("Candidate review catalog correction flag is invalid")
    return catalog


def catalog_summary(catalog: dict[str, Any]) -> dict[str, int]:
    items = catalog["items"]
    return {
        "candidateCount": len(items),
        "readyCount": sum(item["readiness"] == "ready_for_author_review" for item in items),
        "warningCount": sum(item["warningCount"] > 0 for item in items),
        "correctedCount": sum(item["corrected"] for item in items),
        "preflightPassedCount": sum(item["preflightStatus"] == "passed" for item in items),
    }


def _candidate_presentations(catalog: dict[str, Any], details: dict[str, Any]) -> dict[str, Any]:
    items = {item["candidateId"]: item for item in catalog["items"]}
    comparisons = {record["binding"]["candidateId"]: record for record in details["comparisons"]}
    presentations: list[dict[str, Any]] = []
    for detail in details["details"]:
        candidate_id = detail["binding"]["candidateId"]
        documents: list[dict[str, Any]] = []
        supporting: list[dict[str, str]] = []
        diagnostic_status = "not_available"
        validation_status = "not_available"
        for section in detail["sections"]:
            section_id = section["id"]
            if section["contentType"] == "application/yaml":
                try:
                    parsed = yaml.safe_load(section["content"])
                except yaml.YAMLError as exc:
                    raise ValueError(
                        f"Candidate YAML presentation is invalid: {candidate_id}/{section_id}"
                    ) from exc
                if not isinstance(parsed, dict):
                    raise ValueError(
                        f"Candidate YAML presentation must be an object: "
                        f"{candidate_id}/{section_id}"
                    )
                documents.append(
                    {
                        "path": section_id,
                        "kind": parsed.get("kind", "YAML"),
                        "parsed": parsed,
                        "raw": section["content"],
                    }
                )
                continue
            supporting.append(
                {
                    "id": section_id,
                    "contentType": section["contentType"],
                    "content": section["content"],
                }
            )
            if section["contentType"] == "application/json":
                try:
                    payload = json.loads(section["content"])
                except json.JSONDecodeError:
                    continue
                if not isinstance(payload, dict):
                    continue
                if section_id.endswith("diagnostics.json"):
                    diagnostic_status = str(payload.get("status", "unknown"))
                elif section_id.endswith("validation-report.json"):
                    validation_status = str(payload.get("status", "unknown"))
        item = items[candidate_id]
        comparison = comparisons[candidate_id]
        supporting.append(
            {
                "id": "static-versus-ai-comparison.json",
                "contentType": "application/json",
                "content": json.dumps(comparison, indent=2, sort_keys=True) + "\n",
            }
        )
        presentations.append(
            {
                "candidateId": candidate_id,
                "health": {
                    "readiness": item["readiness"],
                    "preflight": item["preflightStatus"],
                    "warnings": item["warningCount"],
                    "corrected": item["corrected"],
                    "diagnostics": diagnostic_status,
                    "validation": validation_status,
                    "staticMembers": comparison["static"]["memberCount"],
                    "aiProposal": comparison["ai"]["status"],
                },
                "documents": documents,
                "supporting": supporting,
                "ai": comparison["ai"],
                "semanticReview": comparison.get("semantic"),
            }
        )
    return {
        "apiVersion": "spec-harvester.candidate-review-presentations/v0",
        "sourceBundleSha256": catalog["sourceBundleSha256"],
        "presentations": presentations,
    }


def render_local_candidate_review_browser(
    options: LocalCandidateReviewBrowserOptions,
) -> dict[str, Any]:
    catalog = load_local_candidate_review_catalog(options.catalog)
    output = options.output
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    (output / "catalog.json").write_text(
        json.dumps(catalog, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if options.details is not None:
        details = _read_json_object(options.details)
        if (
            not isinstance(details.get("details"), list)
            or not isinstance(details.get("comparisons"), list)
            or details.get("sourceBundleSha256") != catalog["sourceBundleSha256"]
        ):
            raise ValueError("Candidate detail set is invalid")
        schema = load_candidate_review_schema()
        validator = Draft202012Validator(schema)
        for record in [*details["details"], *details["comparisons"]]:
            errors = list(validator.iter_errors(record))
            if errors:
                raise ValueError(f"Candidate detail set schema is invalid: {errors[0].message}")
        expected_bindings = {item["candidateId"]: item["packetSha256"] for item in catalog["items"]}

        def bindings(records: list[Any]) -> dict[str, str]:
            values = {
                record["binding"]["candidateId"]: record["binding"]["packetSha256"]
                for record in records
            }
            if len(values) != len(records):
                raise ValueError("Candidate detail set contains duplicate bindings")
            return values

        if (
            bindings(details["details"]) != expected_bindings
            or bindings(details["comparisons"]) != expected_bindings
        ):
            raise ValueError("Candidate detail set bindings differ from catalog")
        (output / "details.json").write_text(
            json.dumps(details, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        (output / "presentations.json").write_text(
            json.dumps(_candidate_presentations(catalog, details), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    (output / "index.html").write_text(INDEX_HTML, encoding="utf-8")
    (output / "workbench.css").write_text(WORKBENCH_CSS, encoding="utf-8")
    (output / "workbench.js").write_text(WORKBENCH_JS, encoding="utf-8")
    return {
        "status": "passed",
        "output": str(output),
        "detailCount": len(details["details"]) if options.details is not None else 0,
        **catalog_summary(catalog),
    }


INDEX_HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; connect-src 'self' http://127.0.0.1:* http://localhost:*; style-src 'self'; script-src 'self'; base-uri 'none'; object-src 'none'; frame-ancestors 'none'">
<title>SpecHarvester Candidate Review</title><link rel="stylesheet" href="workbench.css"></head>
<body><main><header><div><p class="eyebrow">LOCAL REVIEW WORKBENCH</p><h1>Candidate review</h1></div><p class="boundary">Candidate evidence only. This is not the accepted public index.</p></header>
<section id="summary" class="summary" aria-label="Corpus summary"></section>
<div class="review-layout">
<section class="review-main">
<h2 id="selected-title">Candidate</h2>
<section class="review-actions" aria-label="Reviewer actions">
<div class="action-fields"><label>Disposition<select id="disposition"><option value="accept_for_intake">Accept for intake</option><option value="request_revision">Request revision</option><option value="defer">Defer</option><option value="do_not_promote">Do not promote</option></select></label><label>Reason<select id="reason-code"></select></label><label>Notes<textarea id="decision-notes" maxlength="4000"></textarea></label><button id="record-decision" type="button">Record decision</button></div>
<div class="exchange"><span id="decision-status">Decision service not connected.</span><button id="refresh-decisions" type="button">Refresh</button><button id="export-decisions" type="button">Export</button><label class="file-action">Import<input id="import-decisions" type="file" accept="application/json"></label></div>
<details class="service-config"><summary>Review service settings</summary><div class="service-fields"><label>Decision service<input id="service-url" type="url" value="http://127.0.0.1:8765"></label><label>CSRF token<input id="csrf-token" type="password" autocomplete="off"></label><label>Reviewer<input id="reviewer" type="text" maxlength="200"></label></div></details>
</section>
<article id="detail" class="detail" aria-live="polite"></article>
</section>
<aside class="candidate-sidebar" aria-label="Candidate queue">
<div class="sidebar-heading"><h2>Candidates</h2><span id="queue-position"></span></div>
<section class="controls" aria-label="Catalog filters"><label class="wide">Search<input id="search" type="search" placeholder="Candidate ID"></label><label>Ecosystem<select id="ecosystem"></select></label><label>AI proposal<select id="ai-proposal"></select></label><label>Review state<select id="review-state"></select></label><details class="more-filters"><summary>More filters</summary><label>Readiness<select id="readiness"></select></label><label>Warnings<select id="warnings"></select></label><label>Correction<select id="corrected"></select></label><label>Shape<select id="shape"></select></label><label>Preflight<select id="preflight"></select></label><label>Sort<select id="sort"><option value="id">Candidate ID</option><option value="warnings">Warnings</option><option value="ecosystem">Ecosystem</option></select></label></details></section>
<section class="queue"><button id="previous" type="button" aria-label="Previous candidate">Previous</button><button id="next" type="button" aria-label="Next candidate">Next</button></section>
<nav id="results" class="candidate-list" aria-label="Candidates"></nav>
</aside>
</div>
</main><script src="workbench.js"></script></body></html>"""

WORKBENCH_CSS = """*{box-sizing:border-box}body{margin:0;background:#f4f6f8;color:#172033;font:14px system-ui,sans-serif}main{max-width:1600px;margin:auto;padding:28px}header{display:flex;justify-content:space-between;gap:24px;align-items:flex-end;border-bottom:1px solid #ccd3dc;padding-bottom:16px}.eyebrow{font-size:12px;font-weight:700;color:#2563a9;letter-spacing:0}.boundary{max-width:350px;color:#5d6778}h1{margin:3px 0;font-size:28px}h2{font-size:20px;margin:0}.summary{display:grid;grid-template-columns:repeat(7,minmax(90px,1fr));gap:8px;margin:16px 0}.metric{background:#fff;border:1px solid #d8dee7;border-radius:6px;padding:10px}.metric b{display:block;font-size:20px}.metric span{font-size:12px;color:#5d6778}.review-layout{display:grid;grid-template-columns:minmax(0,1fr) 390px;gap:20px;align-items:start}.review-main{min-width:0}.review-actions{background:#fff;border:1px solid #d8dee7;border-radius:6px;padding:12px;margin:10px 0 16px}.service-fields,.action-fields{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;align-items:end}.action-fields{grid-template-columns:minmax(150px,.8fr) minmax(150px,.8fr) minmax(220px,1.5fr) auto}.review-actions label,.controls label,.semantic-actions label{display:grid;gap:5px;color:#4b5565;font-size:12px;font-weight:600}.review-actions input,.review-actions select,.review-actions textarea,.controls input,.controls select,.semantic-actions select,.semantic-claim textarea{width:100%;border:1px solid #adb8c7;border-radius:4px;padding:7px;background:#fff;color:#172033}.review-actions textarea{height:50px;resize:vertical}.exchange{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:10px}.exchange span{margin-right:auto;color:#435064}.service-config{margin-top:10px;border-top:1px solid #e4e8ee;padding-top:8px}.service-config summary,.more-filters summary,.evidence-drawer summary,.raw-yaml summary{cursor:pointer;color:#315f91;font-weight:600}.service-fields{margin-top:10px}.file-action{display:inline-block;border:1px solid #2563a9;border-radius:4px;padding:6px 10px;color:#1d4f86;cursor:pointer}.file-action input{display:none}button{border:1px solid #2563a9;background:#fff;color:#1d4f86;border-radius:4px;padding:7px 10px;cursor:pointer}button:disabled{opacity:.45;cursor:default}.candidate-sidebar{position:sticky;top:16px;background:#fff;border:1px solid #d8dee7;border-radius:6px;max-height:calc(100vh - 32px);display:flex;flex-direction:column;overflow:hidden}.sidebar-heading{display:flex;justify-content:space-between;align-items:baseline;padding:14px;border-bottom:1px solid #e4e8ee}.sidebar-heading span{font-size:12px;color:#5d6778}.controls{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:10px;border-bottom:1px solid #e4e8ee}.controls .wide,.more-filters{grid-column:1/-1}.more-filters{padding-top:2px}.more-filters[open]{display:grid;grid-template-columns:1fr 1fr;gap:8px}.more-filters summary{grid-column:1/-1}.queue{display:flex;justify-content:space-between;padding:8px 10px;border-bottom:1px solid #e4e8ee}.candidate-list{overflow:auto;min-height:220px}.candidate-row{display:block;width:100%;border:0;border-bottom:1px solid #e8ecf1;border-radius:0;padding:10px 12px;text-align:left;color:#172033}.candidate-row:hover{background:#f3f7fb}.candidate-row.selected{background:#e4eef9;box-shadow:inset 3px 0 #2563a9}.candidate-name{display:block;font-weight:700;overflow-wrap:anywhere}.candidate-meta{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}.badge{display:inline-block;padding:2px 6px;border-radius:3px;background:#edf2f7;color:#38485a;font-size:11px}.badge.reviewed{background:#e1f2e8;color:#215d3a}.detail{min-width:0}.section-title{font-size:15px;margin:22px 0 10px}.health-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}.health-item{background:#fff;border:1px solid #d8dee7;border-radius:6px;padding:10px}.health-item span{display:block;color:#657084;font-size:11px}.health-item b{display:block;margin-top:4px;overflow-wrap:anywhere}.semantic-comparison{display:grid;grid-template-columns:1fr 1fr;gap:10px}.semantic-panel,.semantic-actions{background:#fff;border:1px solid #d8dee7;border-radius:6px;padding:14px}.semantic-panel h4,.semantic-actions h4{margin:0 0 10px}.claim-group{border-top:1px solid #e4e8ee;padding-top:10px;margin-top:10px}.claim-group h5{margin:0 0 7px}.semantic-claim{display:grid;grid-template-columns:auto 1fr;gap:8px;padding:8px 0}.claim-body{display:grid;gap:4px}.claim-body small{color:#667085;overflow-wrap:anywhere}.semantic-claim textarea{min-height:70px;resize:vertical}.semantic-actions{display:grid;grid-template-columns:minmax(180px,280px) 1fr;gap:14px;align-items:end;margin-top:10px}.semantic-boundary{color:#5d6778;margin:0}.spec-document{background:#fff;border:1px solid #d8dee7;border-radius:6px;padding:18px;margin-bottom:12px}.document-heading{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}.document-heading h3{margin:0;font-size:18px}.document-path{font:12px ui-monospace,SFMono-Regular,monospace;color:#667085;overflow-wrap:anywhere}.document-summary{font-size:15px;line-height:1.5;color:#354052;max-width:900px}.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px;margin:14px 0}.fact{border-left:3px solid #b9c8d9;padding:4px 8px}.fact dt{font-size:11px;color:#657084}.fact dd{margin:3px 0 0;font-weight:600;overflow-wrap:anywhere}.document-group{border-top:1px solid #e4e8ee;padding-top:12px;margin-top:12px}.document-group h4{margin:0 0 8px;font-size:13px}.document-group ul{margin:0;padding-left:20px}.document-group li{margin:5px 0;line-height:1.45}.chips{display:flex;gap:6px;flex-wrap:wrap}.chip{background:#eaf2fb;color:#244e78;border-radius:3px;padding:4px 7px;font-size:12px}.raw-yaml,.evidence-drawer{border-top:1px solid #e4e8ee;padding:10px 0}.raw-yaml pre,.evidence-drawer pre{margin:10px 0 0;max-height:380px;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere;background:#f5f7fa;border:1px solid #e0e5eb;padding:10px;font:12px/1.5 ui-monospace,SFMono-Regular,monospace}@media(max-width:1050px){.review-layout{grid-template-columns:minmax(0,1fr) 330px}.action-fields{grid-template-columns:1fr 1fr}.health-grid{grid-template-columns:repeat(2,1fr)}.semantic-comparison{grid-template-columns:1fr}}@media(max-width:760px){main{padding:14px}header{display:block}.summary{grid-template-columns:repeat(2,1fr)}.review-layout{display:flex;flex-direction:column}.candidate-sidebar{position:static;order:-1;width:100%;max-height:55vh}.service-fields,.action-fields,.semantic-actions{grid-template-columns:1fr}.health-grid{grid-template-columns:repeat(2,1fr)}}"""

WORKBENCH_JS = """'use strict';
const state={items:[],presentations:new Map(),current:new Map(),reasons:[],cursor:0};const fields=['readiness','warnings','corrected','ecosystem','shape','preflight','review-state','ai-proposal'];const reviewStates=['unreviewed','in_review','accept_for_intake','request_revision','defer','do_not_promote'];
const value=(id)=>document.getElementById(id).value;const setText=(node,text)=>node.textContent=String(text);const node=(tag,className,text)=>{const item=document.createElement(tag);if(className)item.className=className;if(text!==undefined)setText(item,text);return item};
function option(select,label,value){const item=node('option','',label);item.value=value;select.append(item)}
function selectOptions(id,values){const select=document.getElementById(id);option(select,'All','');[...values].sort().forEach(item=>option(select,item,item))}
function filtered(){const search=value('search').trim().toLowerCase();let rows=state.items.filter(item=>!search||item.candidateId.toLowerCase().includes(search));const filters={readiness:'readiness',ecosystem:'ecosystem',shape:'packageShape',preflight:'preflightStatus','review-state':'reviewState'};Object.entries(filters).forEach(([control,key])=>{if(value(control))rows=rows.filter(item=>item[key]===value(control))});if(value('ai-proposal'))rows=rows.filter(item=>state.presentations.get(item.candidateId)?.health.aiProposal===value('ai-proposal'));if(value('warnings'))rows=rows.filter(item=>value('warnings')==='has_warnings'?item.warningCount>0:item.warningCount===0);if(value('corrected'))rows=rows.filter(item=>String(item.corrected)===value('corrected'));const sort=value('sort');rows.sort((a,b)=>sort==='warnings'?b.warningCount-a.warningCount||a.candidateId.localeCompare(b.candidateId):a[sort==='ecosystem'?'ecosystem':'candidateId'].localeCompare(b[sort==='ecosystem'?'ecosystem':'candidateId']));return rows}
function valuesAt(record,path){return path.reduce((value,key)=>value&&value[key],record)}
function strings(values){if(!Array.isArray(values))return[];return values.map(value=>{if(typeof value==='string')return value;if(value?.statement)return [value.level,value.id,value.statement].filter(Boolean).join(' · ');if(value?.kind&&(value.path||value.paths)){const paths=value.path||value.paths.join(', ');return [value.id,value.kind,paths].filter(Boolean).join(' · ')}return value?.label||value?.id||value?.path||JSON.stringify(value)})}
function addFacts(target,values){const list=node('dl','facts');values.filter(([,value])=>value!==undefined&&value!==null&&value!=='').forEach(([label,value])=>{const fact=node('div','fact');fact.append(node('dt','',label),node('dd','',Array.isArray(value)?value.join(', '):value));list.append(fact)});if(list.children.length)target.append(list)}
function addGroup(target,title,values,asChips=false){const items=strings(values);if(!items.length)return;const group=node('section','document-group');group.append(node('h4','',title));if(asChips){const chips=node('div','chips');items.forEach(item=>chips.append(node('span','chip',item)));group.append(chips)}else{const list=node('ul');items.forEach(item=>list.append(node('li','',item)));group.append(list)}target.append(group)}
function renderDocument(document){const parsed=document.parsed;const card=node('section','spec-document');const heading=node('div','document-heading');const label=valuesAt(parsed,['metadata','name'])||valuesAt(parsed,['metadata','title'])||valuesAt(parsed,['metadata','id'])||document.kind;heading.append(node('h3','',label),node('span','document-path',document.path));card.append(heading);const summaryText=valuesAt(parsed,['metadata','summary'])||valuesAt(parsed,['intent','summary']);if(summaryText)card.append(node('p','document-summary',summaryText));addFacts(card,[['Kind',parsed.kind],['Version',valuesAt(parsed,['metadata','version'])],['Status',valuesAt(parsed,['metadata','status'])],['License',valuesAt(parsed,['metadata','license'])],['Package ID',valuesAt(parsed,['metadata','id'])]]);const capabilities=valuesAt(parsed,['index','provides','capabilities'])||valuesAt(parsed,['provides','capabilities']);const intentIds=valuesAt(parsed,['index','provides','intents'])||(Array.isArray(capabilities)?capabilities.flatMap(capability=>capability.intentIds||[]):[]);addGroup(card,'Capabilities',capabilities,true);addGroup(card,'Intent IDs',intentIds,true);addGroup(card,'Included scope',valuesAt(parsed,['scope','includes']));addGroup(card,'Excluded scope',valuesAt(parsed,['scope','excludes']));addGroup(card,'Constraints',parsed.constraints);addGroup(card,'Evidence',parsed.evidence);const raw=node('details','raw-yaml');raw.append(node('summary','','Raw YAML'),node('pre','',document.raw));card.append(raw);return card}
function setSemanticControlState(decision){const editing=decision==='edited';document.querySelectorAll('[data-claim-edit]').forEach(control=>{control.disabled=!editing});const selectable=!['rejected','deferred'].includes(decision);document.querySelectorAll('[data-claim-id]').forEach(control=>{control.disabled=!selectable;if(!selectable)control.checked=false})}
function renderSemantic(presentation,target){const semantic=presentation.semanticReview;if(!semantic)return;target.append(node('h3','section-title','Static versus AI semantics'));const comparison=node('section','semantic-comparison');const staticPanel=node('section','semantic-panel');staticPanel.append(node('h4','','Static candidate'));addGroup(staticPanel,'Summaries',semantic.static.summaries);addGroup(staticPanel,'Capabilities',semantic.static.capabilities);addGroup(staticPanel,'Intent IDs',semantic.static.intents,true);addGroup(staticPanel,'Interfaces',semantic.static.interfaces);addGroup(staticPanel,'Evidence',semantic.static.evidence);const aiPanel=node('section','semantic-panel');const sources={baseline:'Baseline',follow_up:'Follow-up',recovery:'Luna recovery'};const source=sources[presentation.ai.campaignSource]||'Unknown';aiPanel.append(node('h4','',`AI proposal · ${source}`));const kinds=[['purpose','Purpose'],['capability','Capabilities'],['interface','Interfaces'],['nearby_intent_difference','Nearby intent differences'],['non_goal','Non-goals']];kinds.forEach(([kind,label])=>{const claims=semantic.ai.claims[kind];if(!claims.length)return;const group=node('section','claim-group');group.append(node('h5','',label));claims.forEach(claim=>{const card=node('label','semantic-claim');const check=node('input');check.type='checkbox';check.checked=true;check.dataset.claimId=claim.id;const body=node('span','claim-body');body.append(node('b','',claim.id),node('span','',claim.text));claim.evidence.forEach(item=>body.append(node('small','',`${item.sourcePath} · ${item.sha256.slice(0,12)}`)));const edit=document.createElement('textarea');edit.value=claim.text;edit.dataset.original=claim.text;edit.dataset.claimEdit=claim.id;edit.maxLength=4000;edit.disabled=true;body.append(edit);card.append(check,body);group.append(card)});aiPanel.append(group)});addGroup(aiPanel,'Observed intent reuse',semantic.ai.observedIntentReuse.map(item=>`${item.intentId} · ${item.rationaleClaimId}`),true);addGroup(aiPanel,'Experimental intent proposals',semantic.ai.experimentalIntents.map(item=>`${item.intentId} · user need ${item.userNeedClaimId}`),true);comparison.append(staticPanel,aiPanel);const actions=node('section','semantic-actions');actions.append(node('h4','','Semantic decision'));const label=node('label','');label.append(node('span','','Decision'));const select=document.createElement('select');select.id='semantic-disposition';[['accepted','Accept'],['edited','Edit and accept'],['rejected','Reject'],['deferred','Defer']].forEach(([value,label])=>option(select,label,value));label.append(select);actions.append(label,node('p','semantic-boundary','Records review evidence only. It does not materialize or publish the proposal.'));select.addEventListener('input',()=>setSemanticControlState(select.value));target.append(comparison,actions)}
function renderDetail(item){const target=document.getElementById('detail');target.replaceChildren();setText(document.getElementById('selected-title'),item?.candidateId||'Candidate');const presentation=state.presentations.get(item?.candidateId);if(!presentation){if(item)setText(target,'Detailed evidence is not included in this bundle.');return}target.append(node('h3','section-title','Spec health'));const health=node('section','health-grid');const labels={readiness:'Readiness',preflight:'Preflight',warnings:'Warnings',corrected:'Corrected',diagnostics:'Diagnostics',validation:'Validation',staticMembers:'Static members',aiProposal:'AI proposal'};['readiness','preflight','validation','diagnostics','warnings','corrected','staticMembers','aiProposal'].forEach(key=>{const metric=node('div','health-item');metric.append(node('span','',labels[key]),node('b','',presentation.health[key]));health.append(metric)});target.append(health);renderSemantic(presentation,target);target.append(node('h3','section-title','Package specifications'));presentation.documents.sort((a,b)=>a.path.endsWith('specpm.yaml')?-1:b.path.endsWith('specpm.yaml')?1:a.path.localeCompare(b.path)).forEach(document=>target.append(renderDocument(document)));target.append(node('h3','section-title','Supporting evidence'));presentation.supporting.forEach(section=>{const drawer=node('details','evidence-drawer');drawer.append(node('summary','',section.id),node('pre','',section.content));target.append(drawer)})}
function render(){const rows=filtered();state.cursor=Math.min(state.cursor,Math.max(rows.length-1,0));const results=document.getElementById('results');results.replaceChildren();rows.forEach((item,index)=>{const row=node('button',index===state.cursor?'candidate-row selected':'candidate-row');row.type='button';row.append(node('span','candidate-name',item.candidateId));const meta=node('span','candidate-meta');meta.append(node('span','badge',item.ecosystem),node('span','badge',item.packageShape),node('span',item.reviewState==='unreviewed'?'badge':'badge reviewed',item.reviewState));if(item.warningCount)meta.append(node('span','badge',`${item.warningCount} warnings`));row.append(meta);row.addEventListener('click',()=>{state.cursor=index;save();render()});results.append(row)});const selected=rows[state.cursor];renderDetail(selected);if(selected)loadCurrent(selected);setText(document.getElementById('queue-position'),rows.length?`${state.cursor+1} of ${rows.length}`:'No matches');document.getElementById('previous').disabled=!rows.length||state.cursor===0;document.getElementById('next').disabled=!rows.length||state.cursor>=rows.length-1;const selectedRow=results.querySelector('.selected');if(selectedRow)selectedRow.scrollIntoView({block:'nearest'});save(rows)}
function save(rows=filtered()){const id=rows[state.cursor]?.candidateId||'';localStorage.setItem('specHarvester.reviewQueue',id);const url=new URL(location);url.searchParams.set('cursor',id);history.replaceState(null,'',url)}
function summary(payload,review=null){const target=document.getElementById('summary');target.replaceChildren();const metrics=[['Candidates',payload.candidateCount],['Ready',payload.readyCount],['Warnings',payload.warningCount],['Corrected',payload.correctedCount],['Preflight passed',payload.preflightPassedCount]];if(review)metrics.push(['Reviewed',review.reviewedCount],['Unreviewed',review.unreviewedCount]);metrics.forEach(([label,count])=>{const item=node('div','metric');item.append(node('b','',count),node('span','',label));target.append(item)})}
const serviceUrl=()=>document.getElementById('service-url').value.replace(/\\/$/,'');const selectedItem=()=>filtered()[state.cursor];function status(text){setText(document.getElementById('decision-status'),text)}
async function serviceFetch(path,options={}){const response=await fetch(`${serviceUrl()}${path}`,options);const payload=await response.json();if(!response.ok)throw new Error(payload.message||`HTTP ${response.status}`);return payload}
function refreshReasons(){const disposition=value('disposition');const select=document.getElementById('reason-code');select.replaceChildren();state.reasons.filter(reason=>reason.allowedDispositions.includes(disposition)).forEach(reason=>option(select,reason.label,reason.code))}
function restoreCurrent(item,payload){if(selectedItem()?.candidateId!==item.candidateId)return;const decision=payload.decision;document.getElementById('disposition').value=decision.disposition;refreshReasons();document.getElementById('reason-code').value=decision.reasonCode;document.getElementById('decision-notes').value=decision.notes||'';document.getElementById('reviewer').value=decision.reviewer;const semantic=decision.semanticReview;const select=document.getElementById('semantic-disposition');if(!semantic||!select)return;select.value=semantic.decision;const selected=new Set(semantic.acceptedOrEditedClaimIds);document.querySelectorAll('[data-claim-id]').forEach(control=>{control.checked=selected.has(control.dataset.claimId)});const edits=new Map((semantic.editedClaims||[]).map(edit=>[edit.claimId,edit.text]));document.querySelectorAll('[data-claim-edit]').forEach(control=>{control.value=edits.get(control.dataset.claimEdit)||control.dataset.original});setSemanticControlState(semantic.decision)}
async function loadCurrent(item){try{const response=await fetch(`${serviceUrl()}/v0/decisions/${encodeURIComponent(item.candidateId)}`);if(response.status===404){state.current.delete(item.candidateId);status(`${item.candidateId}: unreviewed`);return}const payload=await response.json();if(!response.ok)throw new Error(payload.message||`HTTP ${response.status}`);state.current.set(item.candidateId,payload);restoreCurrent(item,payload);status(`${item.candidateId}: ${payload.decision.disposition}`)}catch(error){status(`Decision service unavailable: ${error.message}`)}}
async function refreshService(){try{const [reasons,progress,current]=await Promise.all([serviceFetch('/v0/reasons'),serviceFetch('/v0/summary'),serviceFetch('/v0/decisions')]);state.reasons=reasons.codes;refreshReasons();state.current.clear();current.decisions.forEach(record=>{state.current.set(record.decision.binding.candidateId,record);const item=state.items.find(candidate=>candidate.candidateId===record.decision.binding.candidateId);if(item)item.reviewState=record.decision.disposition});summary({candidateCount:state.items.length,readyCount:state.items.filter(x=>x.readiness==='ready_for_author_review').length,warningCount:state.items.filter(x=>x.warningCount>0).length,correctedCount:state.items.filter(x=>x.corrected).length,preflightPassedCount:state.items.filter(x=>x.preflightStatus==='passed').length},progress);const item=selectedItem();if(item)await loadCurrent(item);render()}catch(error){status(`Decision service unavailable: ${error.message}`)}}
async function recordDecision(){const item=selectedItem();if(!item){status('No candidate selected.');return}const current=state.current.get(item.candidateId);const reviewer=value('reviewer').trim();const action={candidateId:item.candidateId,disposition:value('disposition'),reviewer,reasonCode:value('reason-code'),notes:value('decision-notes').trim(),priorDecisionSha256:current?.decisionSha256||null};const presentation=state.presentations.get(item.candidateId);if(presentation?.semanticReview){const decision=value('semantic-disposition');const selected=[...document.querySelectorAll('[data-claim-id]:checked')].map(control=>control.dataset.claimId);const editedClaims=decision==='edited'?[...document.querySelectorAll('[data-claim-edit]')].filter(control=>selected.includes(control.dataset.claimEdit)&&control.value!==control.dataset.original).map(control=>({claimId:control.dataset.claimEdit,text:control.value.trim()})):[];action.semanticAction={decision,acceptedOrEditedClaimIds:['rejected','deferred'].includes(decision)?[]:selected,editedClaims,...presentation.semanticReview.binding}}try{await serviceFetch('/v0/actions',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':value('csrf-token')},body:JSON.stringify(action)});item.reviewState=action.disposition;await refreshService()}catch(error){status(`Decision rejected: ${error.message}`)}}
async function exportDecisions(){try{const payload=await serviceFetch('/v0/export');const link=node('a');link.href=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)+'\\n'],{type:'application/json'}));link.download='spec-harvester-review-decisions.json';link.click();URL.revokeObjectURL(link.href);status(`Exported ${payload.decisions.length} decision records.`)}catch(error){status(`Export failed: ${error.message}`)}}
async function importDecisions(file){try{const payload=JSON.parse(await file.text());const result=await serviceFetch('/v0/import',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':value('csrf-token')},body:JSON.stringify(payload)});await refreshService();status(`Imported ${result.decisionCount} decision records.`)}catch(error){status(`Import failed: ${error.message}`)}}
Promise.all([fetch('catalog.json').then(response=>response.json()),fetch('presentations.json').then(response=>response.ok?response.json():null).catch(()=>null)]).then(([payload,presentationSet])=>{state.items=payload.items;if(presentationSet)presentationSet.presentations.forEach(item=>state.presentations.set(item.candidateId,item));summary({candidateCount:state.items.length,readyCount:state.items.filter(x=>x.readiness==='ready_for_author_review').length,warningCount:state.items.filter(x=>x.warningCount>0).length,correctedCount:state.items.filter(x=>x.corrected).length,preflightPassedCount:state.items.filter(x=>x.preflightStatus==='passed').length});selectOptions('readiness',new Set(state.items.map(x=>x.readiness)));selectOptions('ecosystem',new Set(state.items.map(x=>x.ecosystem)));selectOptions('shape',new Set(state.items.map(x=>x.packageShape)));selectOptions('preflight',new Set(state.items.map(x=>x.preflightStatus)));selectOptions('review-state',new Set(reviewStates));selectOptions('ai-proposal',new Set([...state.presentations.values()].map(x=>x.health.aiProposal)));option(document.getElementById('warnings'),'All','');option(document.getElementById('warnings'),'Has warnings','has_warnings');option(document.getElementById('warnings'),'No warnings','no_warnings');option(document.getElementById('corrected'),'All','');option(document.getElementById('corrected'),'Corrected','true');option(document.getElementById('corrected'),'Original','false');const retained=new URL(location).searchParams.get('cursor')||localStorage.getItem('specHarvester.reviewQueue');const retainedQueue=filtered();const index=retainedQueue.findIndex(x=>x.candidateId===retained);if(index>=0)state.cursor=index;fields.concat(['sort']).forEach(id=>document.getElementById(id).addEventListener('input',()=>{state.cursor=0;render()}));document.getElementById('previous').addEventListener('click',()=>{state.cursor--;render()});document.getElementById('next').addEventListener('click',()=>{state.cursor++;render()});document.getElementById('disposition').addEventListener('input',refreshReasons);document.getElementById('record-decision').addEventListener('click',recordDecision);document.getElementById('refresh-decisions').addEventListener('click',refreshService);document.getElementById('export-decisions').addEventListener('click',exportDecisions);document.getElementById('import-decisions').addEventListener('change',event=>{const file=event.target.files[0];if(file)importDecisions(file)});render();refreshService()}).catch(error=>{setText(document.body,`Cannot load local review catalog: ${error.message}`)});"""
