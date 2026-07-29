# ruff: noqa: E501

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

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
<section class="review-actions" aria-label="Reviewer actions">
<div class="service-fields"><label>Decision service<input id="service-url" type="url" value="http://127.0.0.1:8765"></label><label>CSRF token<input id="csrf-token" type="password" autocomplete="off"></label><label>Reviewer<input id="reviewer" type="text" maxlength="200"></label></div>
<div class="action-fields"><label>Disposition<select id="disposition"><option value="accept_for_intake">Accept for intake</option><option value="request_revision">Request revision</option><option value="defer">Defer</option><option value="do_not_promote">Do not promote</option></select></label><label>Reason<select id="reason-code"></select></label><label>Notes<textarea id="decision-notes" maxlength="4000"></textarea></label><button id="record-decision" type="button">Record decision</button></div>
<div class="exchange"><span id="decision-status">Decision service not connected.</span><button id="refresh-decisions" type="button">Refresh</button><button id="export-decisions" type="button">Export</button><label class="file-action">Import<input id="import-decisions" type="file" accept="application/json"></label></div>
</section>
<section class="controls" aria-label="Catalog filters"><label>Search<input id="search" type="search" placeholder="Candidate ID"></label><label>Readiness<select id="readiness"></select></label><label>Warnings<select id="warnings"></select></label><label>Correction<select id="corrected"></select></label><label>Ecosystem<select id="ecosystem"></select></label><label>Shape<select id="shape"></select></label><label>Preflight<select id="preflight"></select></label><label>Review state<select id="review-state"></select></label><label>Sort<select id="sort"><option value="id">Candidate ID</option><option value="warnings">Warnings</option><option value="ecosystem">Ecosystem</option></select></label></section>
<section class="queue"><button id="previous" type="button" aria-label="Previous candidate">Previous</button><span id="queue-position"></span><button id="next" type="button" aria-label="Next candidate">Next</button></section>
<section><table><thead><tr><th>Candidate</th><th>Readiness</th><th>Warnings</th><th>Correction</th><th>Ecosystem</th><th>Shape</th><th>Preflight</th><th>Review</th></tr></thead><tbody id="results"></tbody></table></section><aside id="detail" class="detail" aria-live="polite"></aside>
</main><script src="workbench.js"></script></body></html>"""

WORKBENCH_CSS = """*{box-sizing:border-box}body{margin:0;background:#f6f7f9;color:#172033;font:14px system-ui,sans-serif}main{max-width:1400px;margin:auto;padding:32px}header{display:flex;justify-content:space-between;gap:24px;align-items:flex-end;border-bottom:1px solid #ccd3dc;padding-bottom:20px}.eyebrow{font-size:12px;font-weight:700;color:#2563a9;letter-spacing:0}.boundary{max-width:350px;color:#5d6778}h1{margin:3px 0;font-size:28px}.summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:24px 0}.metric,.controls label,.queue,table,.detail,.review-actions{background:#fff;border:1px solid #d8dee7;border-radius:6px}.metric{padding:14px}.metric b{display:block;font-size:24px}.review-actions{padding:14px;margin-bottom:16px}.service-fields,.action-fields,.exchange{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;align-items:end}.action-fields,.exchange{margin-top:10px}.review-actions label{display:grid;gap:5px;color:#4b5565;font-size:12px;font-weight:600}.review-actions input,.review-actions select,.review-actions textarea{width:100%;border:1px solid #adb8c7;border-radius:4px;padding:7px;background:#fff;color:#172033}.review-actions textarea{height:52px;resize:vertical}.exchange{display:flex;align-items:center;flex-wrap:wrap}.exchange span{margin-right:auto}.file-action{display:inline-block;border:1px solid #2563a9;border-radius:4px;padding:6px 10px;color:#1d4f86;cursor:pointer}.file-action input{display:none}.controls{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:16px}.controls label{padding:9px;display:grid;gap:5px;color:#4b5565;font-size:12px;font-weight:600}.controls input,.controls select{width:100%;border:1px solid #adb8c7;border-radius:4px;padding:7px;background:#fff;color:#172033}.queue{display:flex;justify-content:center;gap:14px;align-items:center;padding:10px;margin-bottom:16px}button{border:1px solid #2563a9;background:#fff;color:#1d4f86;border-radius:4px;padding:6px 10px;cursor:pointer}button:disabled{opacity:.45;cursor:default}table{width:100%;border-collapse:separate;border-spacing:0;overflow:hidden}th,td{text-align:left;padding:10px;border-bottom:1px solid #e4e8ee}th{font-size:12px;color:#526070;background:#f0f3f7}tr:last-child td{border-bottom:0}.selected td{background:#e7f0fb}.badge{display:inline-block;padding:2px 6px;border-radius:3px;background:#edf2f7;color:#38485a;font-size:12px}.detail{margin-top:16px;padding:16px}.detail h2{font-size:18px;margin:0 0 12px}.detail h3{font-size:14px;margin:18px 0 6px}.detail pre{margin:0;max-height:320px;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere;background:#f5f7fa;border:1px solid #e0e5eb;padding:10px}@media(max-width:800px){main{padding:16px}header{display:block}.summary{grid-template-columns:repeat(2,1fr)}table{display:block;overflow:auto;white-space:nowrap}}"""

WORKBENCH_JS = """'use strict';
const state={items:[],details:new Map(),comparisons:new Map(),current:new Map(),reasons:[],cursor:0};const fields=['readiness','warnings','corrected','ecosystem','shape','preflight','review-state'];const reviewStates=['unreviewed','in_review','accept_for_intake','request_revision','defer','do_not_promote'];
const value=(id)=>document.getElementById(id).value;const setText=(node,text)=>node.textContent=String(text);
function option(select,label,value){const node=document.createElement('option');node.value=value;setText(node,label);select.append(node)}
function selectOptions(id,values){const select=document.getElementById(id);option(select,'All','');[...values].sort().forEach(item=>option(select,item,item))}
function filtered(){const search=value('search').trim().toLowerCase();let rows=state.items.filter(item=>!search||item.candidateId.toLowerCase().includes(search));const filters={readiness:'readiness',ecosystem:'ecosystem',shape:'packageShape',preflight:'preflightStatus','review-state':'reviewState'};Object.entries(filters).forEach(([control,key])=>{if(value(control))rows=rows.filter(item=>item[key]===value(control))});if(value('warnings'))rows=rows.filter(item=>value('warnings')==='has_warnings'?item.warningCount>0:item.warningCount===0);if(value('corrected'))rows=rows.filter(item=>String(item.corrected)===value('corrected'));const sort=value('sort');rows.sort((a,b)=>sort==='warnings'?b.warningCount-a.warningCount||a.candidateId.localeCompare(b.candidateId):a[sort==='ecosystem'?'ecosystem':'candidateId'].localeCompare(b[sort==='ecosystem'?'ecosystem':'candidateId']));return rows}
function renderDetail(item){const target=document.getElementById('detail');target.replaceChildren();const detail=state.details.get(item?.candidateId);if(!detail){if(item)setText(target,'Detailed evidence is not included in this bundle.');return}const heading=document.createElement('h2');setText(heading,`Detail: ${item.candidateId}`);target.append(heading);const comparison=state.comparisons.get(item.candidateId);if(comparison){const title=document.createElement('h3');setText(title,'Static versus Codex Spark proposal');const pre=document.createElement('pre');setText(pre,JSON.stringify(comparison,null,2));target.append(title,pre)}detail.sections.forEach(section=>{const title=document.createElement('h3');setText(title,section.id);const pre=document.createElement('pre');setText(pre,section.content);target.append(title,pre)})}
function render(){const rows=filtered();state.cursor=Math.min(state.cursor,Math.max(rows.length-1,0));const body=document.getElementById('results');body.replaceChildren();rows.forEach((item,index)=>{const tr=document.createElement('tr');if(index===state.cursor)tr.className='selected';['candidateId','readiness','warningCount','corrected','ecosystem','packageShape','preflightStatus','reviewState'].forEach(key=>{const td=document.createElement('td');const span=document.createElement('span');span.className='badge';setText(span,item[key]);td.append(span);tr.append(td)});tr.addEventListener('click',()=>{state.cursor=index;save();render()});body.append(tr)});const selected=rows[state.cursor];renderDetail(selected);if(selected)loadCurrent(selected);setText(document.getElementById('queue-position'),rows.length?`Queue ${state.cursor+1} of ${rows.length}`:'No matching candidates');document.getElementById('previous').disabled=!rows.length||state.cursor===0;document.getElementById('next').disabled=!rows.length||state.cursor>=rows.length-1;save(rows)}
function save(rows=filtered()){const id=rows[state.cursor]?.candidateId||'';localStorage.setItem('specHarvester.reviewQueue',id);const url=new URL(location);url.searchParams.set('cursor',id);history.replaceState(null,'',url)}
function summary(payload,review=null){const target=document.getElementById('summary');target.replaceChildren();const metrics=[['Candidates',payload.candidateCount],['Ready',payload.readyCount],['Warnings',payload.warningCount],['Corrected',payload.correctedCount],['Preflight passed',payload.preflightPassedCount]];if(review)metrics.push(['Reviewed',review.reviewedCount],['Unreviewed',review.unreviewedCount]);metrics.forEach(([label,count])=>{const node=document.createElement('div');node.className='metric';const b=document.createElement('b');setText(b,count);const p=document.createElement('span');setText(p,label);node.append(b,p);target.append(node)})}
const serviceUrl=()=>document.getElementById('service-url').value.replace(/\\/$/,'');
const selectedItem=()=>filtered()[state.cursor];
function status(text){setText(document.getElementById('decision-status'),text)}
async function serviceFetch(path,options={}){const response=await fetch(`${serviceUrl()}${path}`,options);const payload=await response.json();if(!response.ok)throw new Error(payload.message||`HTTP ${response.status}`);return payload}
function refreshReasons(){const disposition=value('disposition');const select=document.getElementById('reason-code');select.replaceChildren();state.reasons.filter(reason=>reason.allowedDispositions.includes(disposition)).forEach(reason=>option(select,reason.label,reason.code))}
async function loadCurrent(item){try{const response=await fetch(`${serviceUrl()}/v0/decisions/${encodeURIComponent(item.candidateId)}`);if(response.status===404){state.current.delete(item.candidateId);status(`${item.candidateId}: unreviewed`);return}const payload=await response.json();if(!response.ok)throw new Error(payload.message||`HTTP ${response.status}`);state.current.set(item.candidateId,payload);status(`${item.candidateId}: ${payload.decision.disposition}`)}catch(error){status(`Decision service unavailable: ${error.message}`)}}
async function refreshService(){try{const [reasons,progress,current]=await Promise.all([serviceFetch('/v0/reasons'),serviceFetch('/v0/summary'),serviceFetch('/v0/decisions')]);state.reasons=reasons.codes;refreshReasons();state.current.clear();current.decisions.forEach(record=>{state.current.set(record.decision.binding.candidateId,record);const item=state.items.find(candidate=>candidate.candidateId===record.decision.binding.candidateId);if(item)item.reviewState=record.decision.disposition});summary({candidateCount:state.items.length,readyCount:state.items.filter(x=>x.readiness==='ready_for_author_review').length,warningCount:state.items.filter(x=>x.warningCount>0).length,correctedCount:state.items.filter(x=>x.corrected).length,preflightPassedCount:state.items.filter(x=>x.preflightStatus==='passed').length},progress);const item=selectedItem();if(item)await loadCurrent(item)}catch(error){status(`Decision service unavailable: ${error.message}`)}}
async function recordDecision(){const item=selectedItem();if(!item){status('No candidate selected.');return}const current=state.current.get(item.candidateId);const action={candidateId:item.candidateId,disposition:value('disposition'),reviewer:value('reviewer').trim(),reasonCode:value('reason-code'),notes:value('decision-notes').trim(),priorDecisionSha256:current?.decisionSha256||null};try{await serviceFetch('/v0/actions',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':value('csrf-token')},body:JSON.stringify(action)});item.reviewState=action.disposition;await refreshService();render()}catch(error){status(`Decision rejected: ${error.message}`)}}
async function exportDecisions(){try{const payload=await serviceFetch('/v0/export');const link=document.createElement('a');link.href=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)+'\\n'],{type:'application/json'}));link.download='spec-harvester-review-decisions.json';link.click();URL.revokeObjectURL(link.href);status(`Exported ${payload.decisions.length} decision records.`)}catch(error){status(`Export failed: ${error.message}`)}}
async function importDecisions(file){try{const payload=JSON.parse(await file.text());const result=await serviceFetch('/v0/import',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':value('csrf-token')},body:JSON.stringify(payload)});await refreshService();status(`Imported ${result.decisionCount} decision records.`);render()}catch(error){status(`Import failed: ${error.message}`)}}
Promise.all([fetch('catalog.json').then(response=>response.json()),fetch('details.json').then(response=>response.ok?response.json():null).catch(()=>null)]).then(([payload,detailSet])=>{state.items=payload.items;if(detailSet){detailSet.details.forEach(detail=>state.details.set(detail.binding.candidateId,detail));detailSet.comparisons.forEach(comparison=>state.comparisons.set(comparison.binding.candidateId,comparison))}summary({candidateCount:state.items.length,readyCount:state.items.filter(x=>x.readiness==='ready_for_author_review').length,warningCount:state.items.filter(x=>x.warningCount>0).length,correctedCount:state.items.filter(x=>x.corrected).length,preflightPassedCount:state.items.filter(x=>x.preflightStatus==='passed').length});selectOptions('readiness',new Set(state.items.map(x=>x.readiness)));selectOptions('ecosystem',new Set(state.items.map(x=>x.ecosystem)));selectOptions('shape',new Set(state.items.map(x=>x.packageShape)));selectOptions('preflight',new Set(state.items.map(x=>x.preflightStatus)));selectOptions('review-state',new Set(reviewStates));option(document.getElementById('warnings'),'All','');option(document.getElementById('warnings'),'Has warnings','has_warnings');option(document.getElementById('warnings'),'No warnings','no_warnings');option(document.getElementById('corrected'),'All','');option(document.getElementById('corrected'),'Corrected','true');option(document.getElementById('corrected'),'Original','false');const retained=new URL(location).searchParams.get('cursor')||localStorage.getItem('specHarvester.reviewQueue');const retainedQueue=filtered();const index=retainedQueue.findIndex(x=>x.candidateId===retained);if(index>=0)state.cursor=index;fields.concat(['sort']).forEach(id=>document.getElementById(id).addEventListener('input',()=>{state.cursor=0;render()}));document.getElementById('previous').addEventListener('click',()=>{state.cursor--;render()});document.getElementById('next').addEventListener('click',()=>{state.cursor++;render()});document.getElementById('disposition').addEventListener('input',refreshReasons);document.getElementById('record-decision').addEventListener('click',recordDecision);document.getElementById('refresh-decisions').addEventListener('click',refreshService);document.getElementById('export-decisions').addEventListener('click',exportDecisions);document.getElementById('import-decisions').addEventListener('change',event=>{const file=event.target.files[0];if(file)importDecisions(file)});render();refreshService()}).catch(error=>{setText(document.body,`Cannot load local review catalog: ${error.message}`)});"""
