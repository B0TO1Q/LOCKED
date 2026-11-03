"""Builds index.html from pages.json. Run after build_locked.py and the SVG export (see README)."""
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
pages = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages.json")))

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>LOCKED</title>
<meta name="description" content="Printable shooting targets, DOPE cards, data book pages and agency-style qualification targets. US Letter, true scale.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;800&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap">
<style>
/* Layout: range-bag catalog. Sticky command bar, filter rail, card grid of true-scale sheets. */
:root {
  --bg: #F1F0EC; --panel: #FFFFFF; --ink: #1D1F1C; --muted: #6B6E66; --line: #D8D7D0;
  --accent: #E8541A; --accent-ink: #FFFFFF; --olive: #5B6142; --chip: #E6E4DD;
  --display: "Barlow Condensed", "Arial Narrow", Impact, sans-serif;
  --body: "Barlow", "Helvetica Neue", Arial, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, Menlo, Consolas, monospace;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root { --bg: #161815; --panel: #20231F; --ink: #ECEBE6; --muted: #9DA096; --line: #343831; --chip: #2B2F29; color-scheme: dark; }
}
* { box-sizing: border-box; }
html, body { margin: 0; }
body { background: var(--bg); color: var(--ink); font: 15px/1.5 var(--body); }
a { color: inherit; }
.wrap { max-width: 1240px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }

header.hero { background: #1D1F1C; color: #ECEBE6; }
header.hero .wrap { padding-block: 40px 28px; display: grid; grid-template-columns: 1fr auto; gap: 24px; align-items: end; }
.wordmark { font: 800 clamp(56px, 11vw, 120px)/0.85 var(--display); letter-spacing: 0.02em; margin: 0; display: flex; align-items: center; gap: 0.12em; }
.wordmark .o { width: 0.72em; height: 0.72em; border-radius: 50%; border: 0.11em solid var(--accent); position: relative; display: inline-block; }
.wordmark .o::after { content: ""; position: absolute; inset: 22%; border-radius: 50%; background: var(--accent); }
.tag { margin: 14px 0 0; color: #B9BBB2; max-width: 60ch; }
.stats { display: flex; gap: 22px; font: 500 12px/1.2 var(--mono); color: #9DA096; text-transform: uppercase; letter-spacing: 0.06em; }
.stats b { display: block; color: #ECEBE6; font: 800 30px/1 var(--display); }

.bar { position: sticky; top: 0; z-index: 5; background: var(--panel); border-bottom: 1px solid var(--line); }
.bar .wrap { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; padding-block: 10px; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; flex: 1 1 auto; min-width: 0; }
.chip { border: 0; background: var(--chip); color: var(--ink); font: 600 13px var(--body); padding: 7px 12px; border-radius: 999px; cursor: pointer; }
.chip[aria-pressed="true"] { background: var(--ink); color: var(--bg); }
.search { flex: 0 1 220px; min-width: 140px; border: 1px solid var(--line); background: var(--bg); color: var(--ink); font: 14px var(--body); padding: 7px 11px; border-radius: 8px; }
.btn { border: 0; cursor: pointer; font: 600 14px var(--body); padding: 9px 14px; border-radius: 8px; background: var(--chip); color: var(--ink); text-decoration: none; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; }
.btn.primary { background: var(--accent); color: var(--accent-ink); }
.btn:focus-visible, .chip:focus-visible, .search:focus-visible, .card input:focus-visible + span { outline: 2px solid var(--accent); outline-offset: 2px; }

.tips { margin: 20px 0 6px; padding: 12px 16px; border-left: 4px solid var(--accent); background: var(--panel); font-size: 14px; }
.tips strong { font-family: var(--mono); font-size: 12px; letter-spacing: 0.05em; }

section.group { margin: 30px 0 10px; }
section.group h2 { font: 800 30px/1 var(--display); letter-spacing: 0.03em; text-transform: uppercase; margin: 0 0 4px; display: flex; gap: 12px; align-items: baseline; }
section.group h2 small { font: 500 12px var(--mono); color: var(--muted); letter-spacing: 0.05em; }
section.group > p { margin: 0 0 14px; color: var(--muted); max-width: 70ch; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: 16px; align-items: start; }

.card { background: var(--panel); border: 1px solid var(--line); border-radius: 10px; overflow: hidden; display: flex; flex-direction: column; min-width: 0; }
.card.sel { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent) inset; }
.thumb { aspect-ratio: 8.5 / 11; max-width: 100%; background: #fff; border-bottom: 1px solid var(--line); display: block; cursor: zoom-in; padding: 0; border-top: 0; border-left: 0; border-right: 0; width: 100%; }
.thumb img { width: 100%; height: 100%; display: block; }
.meta { padding: 10px 12px 12px; display: flex; flex-direction: column; gap: 4px; flex: 1; min-width: 0; }
.code { font: 700 11px var(--mono); color: var(--accent); letter-spacing: 0.05em; }
.title { font: 600 16px/1.2 var(--body); margin: 0; text-wrap: balance; }
.desc { font-size: 13px; color: var(--muted); margin: 0; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
.drills { font-size: 13px; border-top: 1px solid var(--line); padding-top: 6px; margin-top: 4px; }
.drills summary { cursor: pointer; font: 700 12px var(--mono); color: var(--accent); letter-spacing: 0.04em; text-transform: uppercase; }
.drills ol { margin: 8px 0 0; padding-left: 18px; display: grid; gap: 8px; }
.drills li b { display: block; font-weight: 600; }
.drills .setup { display: block; font: 500 11px var(--mono); color: var(--muted); margin: 1px 0 2px; }
.drills .dref { margin: 8px 0 0; font-size: 12px; color: var(--muted); }
.actions { display: flex; gap: 8px; align-items: center; margin-top: auto; padding-top: 8px; }
.actions .btn { padding: 6px 11px; font-size: 13px; }
.pick { margin-left: auto; display: inline-flex; gap: 6px; align-items: center; font-size: 13px; cursor: pointer; user-select: none; }
.pick input { width: 17px; height: 17px; accent-color: var(--accent); }
.empty { color: var(--muted); padding: 30px 0; }

.tray { position: fixed; left: 50%; transform: translateX(-50%); bottom: calc(16px + env(safe-area-inset-bottom, 0px)); z-index: 9; background: #1D1F1C; color: #ECEBE6; border-radius: 12px; padding: 10px 10px 10px 16px; display: flex; gap: 10px; align-items: center; box-shadow: 0 8px 30px rgba(0,0,0,.3); max-width: calc(100% - 32px); }
.tray[hidden] { display: none; }
.tray .n { font: 700 13px var(--mono); }
.tray .btn { background: #343831; color: #ECEBE6; }
.tray .btn.primary { background: var(--accent); }

dialog { border: 0; padding: 0; background: transparent; max-width: 96vw; max-height: 96vh; }
dialog::backdrop { background: rgba(10,10,10,.8); }
dialog .viewer { background: #fff; width: min(92vw, 70vh); aspect-ratio: 8.5/11; }
dialog img { width: 100%; height: 100%; display: block; }
dialog .vbar { display: flex; gap: 8px; justify-content: flex-end; padding-top: 8px; }

footer { color: var(--muted); font-size: 13px; padding-block: 40px 90px; border-top: 1px solid var(--line); margin-top: 40px; }
footer .wrap { display: grid; gap: 8px; }

#print-root { display: none; }
@page { size: letter; margin: 0; }
@media print {
  body { background: #fff; }
  .app, dialog { display: none !important; }
  #print-root { display: block; }
  #print-root img { display: block; width: 8.5in; height: 11in; page-break-after: always; break-after: page; }
  #print-root img:last-child { page-break-after: auto; break-after: auto; }
}
@media (max-width: 640px) {
  .bar { position: static; }
  header.hero .wrap { grid-template-columns: 1fr; }
  .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
  .desc { display: none; }
  .actions { flex-wrap: wrap; }
}
@media (prefers-reduced-motion: no-preference) { .card { transition: border-color .15s, box-shadow .15s; } }
</style>
</head>
<body>
<div class="app">
<header class="hero">
  <div class="wrap">
    <div>
      <h1 class="wordmark">L<span class="o" aria-hidden="true"></span>CKED</h1>
      <p class="tag">Printable targets, DOPE cards, data book pages and agency-style qualification targets. Every sheet is US Letter and prints at true scale.</p>
    </div>
    <div class="stats" id="stats"></div>
  </div>
</header>

<div class="bar">
  <div class="wrap">
    <div class="chips" id="chips" role="group" aria-label="Filter by section"></div>
    <input class="search" id="q" type="search" placeholder="Search targets or drills" aria-label="Search targets">
    <a class="btn" href="LOCKED.pdf">Full PDF</a>
    <button class="btn primary" id="print-all" type="button">Print all</button>
  </div>
</div>

<main class="wrap">
  <div class="tips"><strong>PRINT AT 100%.</strong> In the print dialog set Scale to 100% or Actual Size and Margins to None, then measure the 1-inch bar at the bottom of the first sheet. Tick several cards to print them as one batch.</div>
  <div id="groups"></div>
</main>

<footer>
  <div class="wrap">
    <div>Agency and military pages are training replicas with approximate proportions. For an official qualification, shoot the target your agency or unit issues.</div>
    <div>Ballistic tables, zero distances and range estimates are starting points. Confirm everything on paper with your own rifle and ammo.</div>
  </div>
</footer>

<div class="tray" id="tray" hidden>
  <span class="n" id="tray-n">0 selected</span>
  <button class="btn" id="clear" type="button">Clear</button>
  <button class="btn primary" id="print-sel" type="button">Print selected</button>
</div>

<dialog id="viewer">
  <div class="viewer"><img id="viewer-img" alt=""></div>
  <div class="vbar">
    <button class="btn primary" id="viewer-print" type="button">Print this</button>
    <a class="btn" id="viewer-open" href="#" target="_blank" rel="noopener">Open full size</a>
    <button class="btn" id="viewer-close" type="button">Close</button>
  </div>
</dialog>
</div>

<div id="print-root" aria-hidden="true"></div>

<script>
const PAGES = __PAGES__;
const SECTIONS = {
  "Targets": "Sight-in, precision, pistol drills and games.",
  "Shooter Tools": "DOPE cards, angular reference, wind, round count and checklist.",
  "Field Kit": "Data book, range card, range estimation and fundamentals for rifle work.",
  "Agency & Military": "Q-style, police silhouette, E- and F-type, scaled-distance and practical competition replicas, plus the FBI pistol qualification card.",
  "Drill Book": "Three drills for every target, with distance, round count and par time. Print these and tick off each drill as you run it clean."
};
const order = Object.keys(SECTIONS);
const selected = new Set();
let filter = "All", query = "";

const $ = s => document.querySelector(s);
const svgOf = p => "svg/" + p.code + ".svg";

$("#stats").innerHTML = `<div><b>${PAGES.length}</b>sheets</div><div><b>${order.length}</b>sections</div><div><b>1:1</b>scale</div>`;

const chips = $("#chips");
["All", ...order].forEach(name => {
  const b = document.createElement("button");
  b.className = "chip"; b.type = "button"; b.textContent = name;
  b.setAttribute("aria-pressed", name === filter);
  b.addEventListener("click", () => { filter = name; chips.querySelectorAll(".chip").forEach(c => c.setAttribute("aria-pressed", c.textContent === name)); render(); });
  chips.appendChild(b);
});
$("#q").addEventListener("input", e => { query = e.target.value.trim().toLowerCase(); render(); });

function card(p) {
  const el = document.createElement("article");
  el.className = "card" + (selected.has(p.code) ? " sel" : "");
  el.innerHTML = `
    <button class="thumb" type="button" aria-label="Preview ${p.title}"><img loading="lazy" src="${svgOf(p)}" alt="${p.title} preview"></button>
    <div class="meta">
      <span class="code">${p.code} · PAGE ${p.page}</span>
      <h3 class="title">${p.title}</h3>
      <p class="desc">${p.desc}</p>
      ${p.drills && p.drills.length ? `<details class="drills"><summary>${p.drills.length} drills</summary><ol>${p.drills.map(d => `<li><b>${d[0]}</b><span class="setup">${d[1]}</span>${d[2]}</li>`).join("")}</ol><p class="dref">Printable on Drill Book page ${p.drillPage}</p></details>` : ""}
      <div class="actions">
        <button class="btn primary" type="button" data-print>Print</button>
        <label class="pick"><input type="checkbox" id="pick-${p.code}" ${selected.has(p.code) ? "checked" : ""}><span>Batch</span></label>
      </div>
    </div>`;
  el.querySelector(".thumb").addEventListener("click", () => openViewer(p));
  el.querySelector("[data-print]").addEventListener("click", () => printSheets([p]));
  el.querySelector("input").addEventListener("change", e => {
    e.target.checked ? selected.add(p.code) : selected.delete(p.code);
    el.classList.toggle("sel", e.target.checked); updateTray();
  });
  return el;
}

function render() {
  const root = $("#groups"); root.innerHTML = "";
  let shown = 0;
  order.forEach(sec => {
    if (filter !== "All" && filter !== sec) return;
    const items = PAGES.filter(p => p.section === sec && (!query || (p.title + " " + p.desc + " " + p.code + " " + (p.drills || []).map(d => d.join(" ")).join(" ")).toLowerCase().includes(query)));
    if (!items.length) return;
    shown += items.length;
    const s = document.createElement("section"); s.className = "group";
    s.innerHTML = `<h2>${sec} <small>${items.length} SHEETS</small></h2><p>${SECTIONS[sec]}</p>`;
    const g = document.createElement("div"); g.className = "grid";
    items.forEach(p => g.appendChild(card(p)));
    s.appendChild(g); root.appendChild(s);
  });
  if (!shown) root.innerHTML = `<p class="empty">Nothing matches "${query}". Try a code like T-17 or a word like zero.</p>`;
}

function updateTray() {
  $("#tray").hidden = selected.size === 0;
  $("#tray-n").textContent = selected.size + " selected";
}
$("#clear").addEventListener("click", () => { selected.clear(); render(); updateTray(); });
$("#print-sel").addEventListener("click", () => printSheets(PAGES.filter(p => selected.has(p.code))));
$("#print-all").addEventListener("click", () => printSheets(PAGES));

async function printSheets(list) {
  const root = $("#print-root"); root.innerHTML = "";
  const imgs = list.map(p => { const i = new Image(); i.src = svgOf(p); i.alt = p.title; root.appendChild(i); return i; });
  await Promise.all(imgs.map(i => i.decode ? i.decode().catch(() => {}) : Promise.resolve()));
  window.print();
}
window.addEventListener("afterprint", () => { $("#print-root").innerHTML = ""; });

const dlg = $("#viewer"); let current = null;
function openViewer(p) {
  current = p;
  $("#viewer-img").src = svgOf(p); $("#viewer-img").alt = p.title;
  $("#viewer-open").href = svgOf(p);
  dlg.showModal();
}
$("#viewer-close").addEventListener("click", () => dlg.close());
$("#viewer-print").addEventListener("click", () => { dlg.close(); printSheets([current]); });
dlg.addEventListener("click", e => { if (e.target === dlg) dlg.close(); });

render();
</script>
</body>
</html>
"""

html = TEMPLATE.replace("__PAGES__", json.dumps(pages))
with open(os.path.join(ROOT, "index.html"), "w") as f:
    f.write(html)
print("index.html written,", len(pages), "sheets")
