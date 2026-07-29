# ruff: noqa: E501

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

CATALOG_API_VERSION = "spec-harvester.candidate-review-catalog/v0"
CATALOG_KIND = "SpecHarvesterCandidateReviewCatalog"
CATALOG_AUTHORITY = "local_review_catalog_evidence_only"


@dataclass(frozen=True)
class LocalCandidateReviewBrowserOptions:
    catalog: Path
    output: Path


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
    schema_path = (
        Path(__file__).resolve().parents[2]
        / "schemas"
        / "local-candidate-review-workbench-v0.schema.json"
    )
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read candidate review schema: {exc}") from exc
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
    (output / "index.html").write_text(INDEX_HTML, encoding="utf-8")
    (output / "workbench.css").write_text(WORKBENCH_CSS, encoding="utf-8")
    (output / "workbench.js").write_text(WORKBENCH_JS, encoding="utf-8")
    return {"status": "passed", "output": str(output), **catalog_summary(catalog)}


INDEX_HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; connect-src 'self'; style-src 'self'; script-src 'self'; base-uri 'none'; object-src 'none'; frame-ancestors 'none'">
<title>SpecHarvester Candidate Review</title><link rel="stylesheet" href="workbench.css"></head>
<body><main><header><div><p class="eyebrow">LOCAL REVIEW WORKBENCH</p><h1>Candidate review</h1></div><p class="boundary">Candidate evidence only. This is not the accepted public index.</p></header>
<section id="summary" class="summary" aria-label="Corpus summary"></section>
<section class="controls" aria-label="Catalog filters"><label>Search<input id="search" type="search" placeholder="Candidate ID"></label><label>Readiness<select id="readiness"></select></label><label>Warnings<select id="warnings"></select></label><label>Correction<select id="corrected"></select></label><label>Ecosystem<select id="ecosystem"></select></label><label>Shape<select id="shape"></select></label><label>Preflight<select id="preflight"></select></label><label>Review state<select id="review-state"></select></label><label>Sort<select id="sort"><option value="id">Candidate ID</option><option value="warnings">Warnings</option><option value="ecosystem">Ecosystem</option></select></label></section>
<section class="queue"><button id="previous" type="button" aria-label="Previous candidate">Previous</button><span id="queue-position"></span><button id="next" type="button" aria-label="Next candidate">Next</button></section>
<section><table><thead><tr><th>Candidate</th><th>Readiness</th><th>Warnings</th><th>Correction</th><th>Ecosystem</th><th>Shape</th><th>Preflight</th><th>Review</th></tr></thead><tbody id="results"></tbody></table></section>
</main><script src="workbench.js"></script></body></html>"""

WORKBENCH_CSS = """*{box-sizing:border-box}body{margin:0;background:#f6f7f9;color:#172033;font:14px system-ui,sans-serif}main{max-width:1400px;margin:auto;padding:32px}header{display:flex;justify-content:space-between;gap:24px;align-items:flex-end;border-bottom:1px solid #ccd3dc;padding-bottom:20px}.eyebrow{font-size:12px;font-weight:700;color:#2563a9;letter-spacing:0}.boundary{max-width:350px;color:#5d6778}h1{margin:3px 0;font-size:28px}.summary{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:24px 0}.metric,.controls label,.queue,table{background:#fff;border:1px solid #d8dee7;border-radius:6px}.metric{padding:14px}.metric b{display:block;font-size:24px}.controls{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:16px}.controls label{padding:9px;display:grid;gap:5px;color:#4b5565;font-size:12px;font-weight:600}.controls input,.controls select{width:100%;border:1px solid #adb8c7;border-radius:4px;padding:7px;background:#fff;color:#172033}.queue{display:flex;justify-content:center;gap:14px;align-items:center;padding:10px;margin-bottom:16px}button{border:1px solid #2563a9;background:#fff;color:#1d4f86;border-radius:4px;padding:6px 10px;cursor:pointer}button:disabled{opacity:.45;cursor:default}table{width:100%;border-collapse:separate;border-spacing:0;overflow:hidden}th,td{text-align:left;padding:10px;border-bottom:1px solid #e4e8ee}th{font-size:12px;color:#526070;background:#f0f3f7}tr:last-child td{border-bottom:0}.selected td{background:#e7f0fb}.badge{display:inline-block;padding:2px 6px;border-radius:3px;background:#edf2f7;color:#38485a;font-size:12px}@media(max-width:800px){main{padding:16px}header{display:block}.summary{grid-template-columns:repeat(2,1fr)}table{display:block;overflow:auto;white-space:nowrap}}"""

WORKBENCH_JS = """'use strict';
const state={items:[],cursor:0};const fields=['readiness','warnings','corrected','ecosystem','shape','preflight','review-state'];
const value=(id)=>document.getElementById(id).value;const setText=(node,text)=>node.textContent=String(text);
function option(select,label,value){const node=document.createElement('option');node.value=value;setText(node,label);select.append(node)}
function selectOptions(id,values){const select=document.getElementById(id);option(select,'All','');[...values].sort().forEach(item=>option(select,item,item))}
function filtered(){const search=value('search').trim().toLowerCase();let rows=state.items.filter(item=>!search||item.candidateId.toLowerCase().includes(search));const filters={readiness:'readiness',ecosystem:'ecosystem',shape:'packageShape',preflight:'preflightStatus','review-state':'reviewState'};Object.entries(filters).forEach(([control,key])=>{if(value(control))rows=rows.filter(item=>item[key]===value(control))});if(value('warnings'))rows=rows.filter(item=>value('warnings')==='has_warnings'?item.warningCount>0:item.warningCount===0);if(value('corrected'))rows=rows.filter(item=>String(item.corrected)===value('corrected'));const sort=value('sort');rows.sort((a,b)=>sort==='warnings'?b.warningCount-a.warningCount||a.candidateId.localeCompare(b.candidateId):a[sort==='ecosystem'?'ecosystem':'candidateId'].localeCompare(b[sort==='ecosystem'?'ecosystem':'candidateId']));return rows}
function render(){const rows=filtered();state.cursor=Math.min(state.cursor,Math.max(rows.length-1,0));const body=document.getElementById('results');body.replaceChildren();rows.forEach((item,index)=>{const tr=document.createElement('tr');if(index===state.cursor)tr.className='selected';['candidateId','readiness','warningCount','corrected','ecosystem','packageShape','preflightStatus','reviewState'].forEach(key=>{const td=document.createElement('td');const span=document.createElement('span');span.className='badge';setText(span,item[key]);td.append(span);tr.append(td)});tr.addEventListener('click',()=>{state.cursor=index;save();render()});body.append(tr)});setText(document.getElementById('queue-position'),rows.length?`Queue ${state.cursor+1} of ${rows.length}`:'No matching candidates');document.getElementById('previous').disabled=!rows.length||state.cursor===0;document.getElementById('next').disabled=!rows.length||state.cursor>=rows.length-1;save(rows)}
function save(rows=filtered()){const id=rows[state.cursor]?.candidateId||'';localStorage.setItem('specHarvester.reviewQueue',id);const url=new URL(location);url.searchParams.set('cursor',id);history.replaceState(null,'',url)}
function summary(payload){const target=document.getElementById('summary');const metrics=[['Candidates',payload.candidateCount],['Ready',payload.readyCount],['Warnings',payload.warningCount],['Corrected',payload.correctedCount],['Preflight passed',payload.preflightPassedCount]];metrics.forEach(([label,count])=>{const node=document.createElement('div');node.className='metric';const b=document.createElement('b');setText(b,count);const p=document.createElement('span');setText(p,label);node.append(b,p);target.append(node)})}
fetch('catalog.json').then(response=>response.json()).then(payload=>{state.items=payload.items;summary({candidateCount:state.items.length,readyCount:state.items.filter(x=>x.readiness==='ready_for_author_review').length,warningCount:state.items.filter(x=>x.warningCount>0).length,correctedCount:state.items.filter(x=>x.corrected).length,preflightPassedCount:state.items.filter(x=>x.preflightStatus==='passed').length});selectOptions('readiness',new Set(state.items.map(x=>x.readiness)));selectOptions('ecosystem',new Set(state.items.map(x=>x.ecosystem)));selectOptions('shape',new Set(state.items.map(x=>x.packageShape)));selectOptions('preflight',new Set(state.items.map(x=>x.preflightStatus)));selectOptions('review-state',new Set(state.items.map(x=>x.reviewState)));option(document.getElementById('warnings'),'All','');option(document.getElementById('warnings'),'Has warnings','has_warnings');option(document.getElementById('warnings'),'No warnings','no_warnings');option(document.getElementById('corrected'),'All','');option(document.getElementById('corrected'),'Corrected','true');option(document.getElementById('corrected'),'Original','false');const retained=new URL(location).searchParams.get('cursor')||localStorage.getItem('specHarvester.reviewQueue');const retainedQueue=filtered();const index=retainedQueue.findIndex(x=>x.candidateId===retained);if(index>=0)state.cursor=index;fields.concat(['sort']).forEach(id=>document.getElementById(id).addEventListener('input',()=>{state.cursor=0;render()}));document.getElementById('previous').addEventListener('click',()=>{state.cursor--;render()});document.getElementById('next').addEventListener('click',()=>{state.cursor++;render()});render()}).catch(error=>{setText(document.body,`Cannot load local review catalog: ${error.message}`)});"""
