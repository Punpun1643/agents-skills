#!/usr/bin/env python3
"""Render a cognitive-map Markdown document as a self-contained interactive page."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


KIND_PATTERN = re.compile(r"\b(CORE|BRANCH|ADVANCED|OPTIONAL)\b", re.IGNORECASE)
FENCE_PATTERN = re.compile(r"^```\s*([\w+-]*)\s*$")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
NODE_PATTERN = re.compile(
    r"\b([A-Za-z][\w-]*)\s*(?:"
    r"\[\s*\"([^\"]+)\"\s*\]|"
    r"\[\s*([^\]]+)\s*\]|"
    r"\(\s*\"([^\"]+)\"\s*\)|"
    r"\(\s*([^\)]+)\s*\))"
)


def slugify(value: str) -> str:
    value = re.sub(r"\*\*|__|`", "", value)
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE).strip().lower()
    return re.sub(r"[-\s]+", "-", value) or "section"


def unique_slug(value: str, used: set[str]) -> str:
    base = slugify(value)
    candidate = base
    index = 2
    while candidate in used:
        candidate = f"{base}-{index}"
        index += 1
    used.add(candidate)
    return candidate


def plain_text(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", value)
    return re.sub(r"[*_`]", "", value).strip()


def inline_markup(value: str) -> str:
    escaped = html.escape(value, quote=False)

    def link(match: re.Match[str]) -> str:
        label = match.group(1)
        url = html.unescape(match.group(2)).strip()
        safe_url = "#" if re.match(r"(?i)\s*(javascript|data):", url) else url
        return f'<a href="{html.escape(safe_url, quote=True)}">{label}</a>'

    escaped = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", link, escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    return escaped


def render_markdown(markdown: str) -> tuple[str, list[dict[str, object]]]:
    lines = markdown.splitlines()
    output: list[str] = []
    headings: list[dict[str, object]] = []
    used_slugs: set[str] = set()
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        fence = FENCE_PATTERN.match(stripped)
        if fence:
            language = fence.group(1).lower()
            code: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code.append(lines[index])
                index += 1
            index += 1
            if language == "mermaid":
                output.append(
                    '<div class="graph-callout"><span>Interactive relationship map</span>'
                    '<button type="button" data-open-graph>Open graph →</button></div>'
                )
            else:
                class_name = f' class="language-{html.escape(language)}"' if language else ""
                output.append(
                    f"<pre><code{class_name}>{html.escape(chr(10).join(code))}</code></pre>"
                )
            continue

        heading = HEADING_PATTERN.match(line)
        if heading:
            level = len(heading.group(1))
            raw_title = heading.group(2)
            title = plain_text(raw_title)
            anchor = unique_slug(title, used_slugs)
            kind_match = KIND_PATTERN.search(title)
            kind = kind_match.group(1).upper() if kind_match else ""
            headings.append({"level": level, "title": title, "anchor": anchor, "kind": kind})
            if level > 1:
                output.append(
                    f'<h{level} id="{anchor}" data-heading data-kind="{kind}">'
                    f'{inline_markup(raw_title)}<a class="anchor" href="#{anchor}" '
                    f'aria-label="Link to {html.escape(title, quote=True)}">#</a></h{level}>'
                )
            index += 1
            continue

        if not stripped:
            index += 1
            continue

        if stripped in {"---", "***", "___"}:
            output.append("<hr>")
            index += 1
            continue

        if stripped.startswith(">"):
            quote: list[str] = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote.append(lines[index].strip()[1:].strip())
                index += 1
            output.append(f"<blockquote>{inline_markup(' '.join(quote))}</blockquote>")
            continue

        unordered = re.match(r"^\s*[-*+]\s+(.+)$", line)
        if unordered:
            items: list[str] = []
            while index < len(lines):
                item = re.match(r"^\s*[-*+]\s+(.+)$", lines[index])
                if not item:
                    break
                items.append(f"<li>{inline_markup(item.group(1))}</li>")
                index += 1
            output.append(f"<ul>{''.join(items)}</ul>")
            continue

        ordered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if ordered:
            items = []
            while index < len(lines):
                item = re.match(r"^\s*\d+[.)]\s+(.+)$", lines[index])
                if not item:
                    break
                items.append(f"<li>{inline_markup(item.group(1))}</li>")
                index += 1
            output.append(f"<ol>{''.join(items)}</ol>")
            continue

        paragraph = [stripped]
        index += 1
        while index < len(lines):
            candidate = lines[index]
            candidate_stripped = candidate.strip()
            if not candidate_stripped:
                break
            if (
                HEADING_PATTERN.match(candidate)
                or FENCE_PATTERN.match(candidate_stripped)
                or candidate_stripped.startswith(">")
                or re.match(r"^\s*[-*+]\s+", candidate)
                or re.match(r"^\s*\d+[.)]\s+", candidate)
                or candidate_stripped in {"---", "***", "___"}
            ):
                break
            paragraph.append(candidate_stripped)
            index += 1
        output.append(f"<p>{inline_markup(' '.join(paragraph))}</p>")

    return "\n".join(output), headings


def mermaid_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    in_mermaid = False
    for line in markdown.splitlines():
        fence = FENCE_PATTERN.match(line.strip())
        if fence:
            if in_mermaid:
                blocks.append("\n".join(current))
                current = []
                in_mermaid = False
            elif fence.group(1).lower() == "mermaid":
                in_mermaid = True
            continue
        if in_mermaid:
            current.append(line)
    return blocks


def normalize(value: str) -> str:
    value = KIND_PATTERN.sub("", value)
    value = re.sub(r"^\s*\d+[.)]?\s*", "", value)
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def parse_graph(markdown: str, headings: list[dict[str, object]]) -> dict[str, object]:
    nodes: dict[str, dict[str, str]] = {}
    edges: list[dict[str, str]] = []

    for block in mermaid_blocks(markdown):
        for raw_line in block.splitlines():
            line = raw_line.strip().rstrip(";")
            if not line or line.startswith(("flowchart", "graph", "%%", "classDef", "class ", "style ")):
                continue
            for match in NODE_PATTERN.finditer(line):
                label = next((group for group in match.groups()[1:] if group), match.group(1))
                nodes[match.group(1)] = {"id": match.group(1), "label": label.strip().strip('"')}

            simplified = NODE_PATTERN.sub(lambda item: item.group(1), line)
            edge_match = re.search(
                r"\b([A-Za-z][\w-]*)\s*--+>\s*(?:\|([^|]+)\|\s*)?([A-Za-z][\w-]*)\b",
                simplified,
            )
            if not edge_match:
                edge_match = re.search(
                    r"\b([A-Za-z][\w-]*)\s*--\s*([^>-]+?)\s*-->\s*([A-Za-z][\w-]*)\b",
                    simplified,
                )
            if edge_match:
                source, label, target = edge_match.groups()
                nodes.setdefault(source, {"id": source, "label": source})
                nodes.setdefault(target, {"id": target, "label": target})
                edges.append({"from": source, "to": target, "label": (label or "relates to").strip()})

    concept_headings = [heading for heading in headings if int(heading["level"]) == 3]
    for node in nodes.values():
        node_normalized = normalize(node["label"])
        best: dict[str, object] | None = None
        best_score = 0
        for heading in concept_headings:
            heading_normalized = normalize(str(heading["title"]))
            if not node_normalized or not heading_normalized:
                continue
            if node_normalized == heading_normalized:
                score = 3
            elif node_normalized in heading_normalized or heading_normalized in node_normalized:
                score = 2
            else:
                score = 0
            if score > best_score:
                best = heading
                best_score = score
        node["anchor"] = str(best["anchor"]) if best else ""
        node["kind"] = str(best["kind"]) if best and best["kind"] else "CONCEPT"

    indegree = {node_id: 0 for node_id in nodes}
    outgoing: dict[str, list[str]] = {node_id: [] for node_id in nodes}
    for edge in edges:
        outgoing[edge["from"]].append(edge["to"])
        indegree[edge["to"]] += 1

    roots = [node_id for node_id, count in indegree.items() if count == 0] or list(nodes)[:1]
    ranks = {node_id: 0 for node_id in nodes}
    queue = list(roots)
    visits = 0
    while queue and visits < max(1, len(nodes) * len(nodes)):
        source = queue.pop(0)
        visits += 1
        for target in outgoing[source]:
            proposed = min(ranks[source] + 1, len(nodes))
            if proposed > ranks[target]:
                ranks[target] = proposed
                queue.append(target)

    grouped: dict[int, list[str]] = {}
    for node_id, rank in ranks.items():
        grouped.setdefault(rank, []).append(node_id)
    max_rank = max(grouped, default=0)
    canvas_height = max(680, (max_rank + 2) * 170)
    for rank, node_ids in grouped.items():
        for position, node_id in enumerate(node_ids):
            nodes[node_id]["x"] = str(round(1100 * (position + 1) / (len(node_ids) + 1) + 50))
            nodes[node_id]["y"] = str(100 + rank * 160)

    return {
        "nodes": list(nodes.values()),
        "edges": edges,
        "width": 1200,
        "height": canvas_height,
    }


PAGE_TEMPLATE = r'''<!doctype html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <title>__TITLE__ · Cognitive Map</title>
  <style>
    :root {
      --bg: #111a27; --sidebar: #182538; --surface: #1d2b40; --surface-2: #243650;
      --border: #35516e; --text: #d9e1eb; --muted: #91a0b4; --accent: #69d7df;
      --accent-2: #8bb5ff; --core: #a8c97f; --branch: #65b8f1; --advanced: #c49be8;
      --optional: #e7a25e; --shadow: 0 18px 50px rgba(0,0,0,.28); --serif: Georgia, 'Times New Roman', serif;
    }
    html[data-theme="light"] {
      --bg: #f4f0e7; --sidebar: #e8e2d5; --surface: #fffdf8; --surface-2: #eee8dc;
      --border: #c9bead; --text: #28313c; --muted: #66717e; --accent: #087d85;
      --accent-2: #346bb3; --core: #64843e; --branch: #287eb0; --advanced: #8356a7;
      --optional: #a85f1c; --shadow: 0 18px 45px rgba(50,41,27,.14);
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body { margin: 0; background: var(--bg); color: var(--text); font: 16px/1.65 Inter, ui-sans-serif, system-ui, -apple-system, sans-serif; }
    button, input { font: inherit; }
    button { color: inherit; }
    a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 3px; }
    .app { min-height: 100vh; display: grid; grid-template-columns: 300px minmax(0,1fr); }
    .sidebar { position: fixed; inset: 0 auto 0 0; width: 300px; padding: 24px 18px; background: var(--sidebar); border-right: 1px solid var(--border); overflow: auto; z-index: 20; }
    .brand { display: flex; align-items: center; gap: 11px; margin: 0 8px 22px; font-weight: 750; letter-spacing: -.02em; }
    .brand-mark { display: grid; place-items: center; width: 34px; height: 34px; border: 1px solid var(--border); border-radius: 10px; color: var(--accent); background: var(--surface); }
    .brand small { display: block; color: var(--muted); font-size: 11px; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; }
    .search { position: relative; margin-bottom: 22px; }
    .search input { width: 100%; padding: 11px 42px 11px 38px; color: var(--text); background: var(--bg); border: 1px solid var(--border); border-radius: 12px; outline: none; }
    .search input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 18%, transparent); }
    .search-icon { position: absolute; left: 13px; top: 11px; color: var(--muted); }
    kbd { padding: 2px 6px; border: 1px solid var(--border); border-radius: 5px; color: var(--muted); background: var(--surface); font-size: 11px; }
    .search kbd { position: absolute; right: 10px; top: 10px; }
    .nav-label { margin: 18px 8px 8px; color: var(--muted); font-size: 11px; font-weight: 800; letter-spacing: .13em; text-transform: uppercase; }
    .nav-item { display: flex; width: 100%; align-items: center; gap: 8px; padding: 8px 10px; border: 0; border-radius: 8px; color: var(--muted); background: transparent; text-align: left; cursor: pointer; }
    .nav-item:hover, .nav-item.active { color: var(--text); background: var(--surface-2); }
    .nav-item.sub { padding-left: 24px; font-size: 14px; }
    .kind-dot { flex: 0 0 7px; width: 7px; height: 7px; border-radius: 50%; background: var(--border); }
    .kind-dot.CORE { background: var(--core); } .kind-dot.BRANCH { background: var(--branch); }
    .kind-dot.ADVANCED { background: var(--advanced); } .kind-dot.OPTIONAL { background: var(--optional); }
    .sidebar-footer { margin: 24px 8px 0; padding-top: 18px; border-top: 1px solid var(--border); color: var(--muted); font-size: 12px; }
    .main { grid-column: 2; min-width: 0; }
    .topbar { position: sticky; top: 0; height: 66px; display: flex; align-items: center; justify-content: space-between; padding: 0 30px; background: color-mix(in srgb, var(--bg) 88%, transparent); backdrop-filter: blur(18px); border-bottom: 1px solid var(--border); z-index: 15; }
    .crumb { min-width: 0; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .crumb strong { color: var(--text); }
    .toolbar { display: flex; gap: 8px; }
    .tool, .view-tab, .graph-tool { border: 1px solid var(--border); border-radius: 9px; background: var(--surface); cursor: pointer; }
    .tool { width: 38px; height: 38px; }
    .tool:hover, .view-tab:hover, .graph-tool:hover { border-color: var(--accent); color: var(--accent); }
    .view-tabs { display: flex; padding: 3px; border: 1px solid var(--border); border-radius: 11px; background: var(--surface); }
    .view-tab { padding: 6px 11px; border: 0; background: transparent; color: var(--muted); }
    .view-tab.active { color: var(--text); background: var(--surface-2); }
    .content { max-width: 920px; margin: 0 auto; padding: 64px 54px 120px; }
    .hero { margin-bottom: 50px; }
    .eyebrow { color: var(--accent); font-size: 12px; font-weight: 850; letter-spacing: .14em; text-transform: uppercase; }
    h1, h2, h3 { font-family: var(--serif); line-height: 1.2; letter-spacing: -.025em; }
    h1 { margin: 12px 0 14px; font-size: clamp(38px, 6vw, 62px); }
    .hero p { max-width: 700px; color: var(--muted); font-size: 18px; }
    article h2 { margin: 60px 0 22px; padding-bottom: 12px; border-bottom: 1px solid var(--border); font-size: 32px; scroll-margin-top: 88px; }
    article h3 { margin: 38px 0 14px; font-size: 23px; scroll-margin-top: 88px; }
    article h3[data-kind]::before { display: inline-block; margin-right: 9px; padding: 3px 7px; border: 1px solid var(--border); border-radius: 999px; color: var(--muted); font: 700 10px/1.3 ui-sans-serif, system-ui; letter-spacing: .08em; vertical-align: 4px; }
    article h3[data-kind="CORE"]::before { content: 'CORE'; color: var(--core); }
    article h3[data-kind="BRANCH"]::before { content: 'BRANCH'; color: var(--branch); }
    article h3[data-kind="ADVANCED"]::before { content: 'ADVANCED'; color: var(--advanced); }
    article h3[data-kind="OPTIONAL"]::before { content: 'OPTIONAL'; color: var(--optional); }
    article p, article li { color: color-mix(in srgb, var(--text) 88%, var(--muted)); }
    article li { margin: 7px 0; }
    article blockquote { margin: 24px 0; padding: 20px 24px; border: 1px solid var(--border); border-left: 4px solid var(--accent); border-radius: 0 12px 12px 0; background: var(--surface); font: 21px/1.55 var(--serif); }
    article pre { overflow: auto; padding: 20px; border: 1px solid var(--border); border-radius: 12px; background: var(--surface); }
    article code { padding: 2px 6px; border-radius: 5px; background: var(--surface-2); font: .9em ui-monospace, SFMono-Regular, Menlo, monospace; }
    article pre code { padding: 0; background: transparent; }
    .anchor { margin-left: 8px; opacity: 0; font-family: ui-sans-serif, system-ui; font-size: .6em; text-decoration: none; }
    h2:hover .anchor, h3:hover .anchor, .anchor:focus { opacity: 1; }
    .graph-callout { display: flex; align-items: center; justify-content: space-between; gap: 20px; margin: 30px 0; padding: 22px 24px; border: 1px solid var(--border); border-radius: 14px; background: linear-gradient(135deg, var(--surface), color-mix(in srgb, var(--accent) 9%, var(--surface))); }
    .graph-callout button { border: 0; color: var(--accent); background: transparent; cursor: pointer; font-weight: 750; }
    .graph-view { display: none; height: calc(100vh - 66px); overflow: hidden; }
    body[data-view="graph"] .reader-view { display: none; } body[data-view="graph"] .graph-view { display: grid; grid-template-columns: minmax(0,1fr) 330px; }
    .graph-canvas { position: relative; min-width: 0; overflow: auto; background-image: radial-gradient(color-mix(in srgb, var(--border) 40%, transparent) 1px, transparent 1px); background-size: 24px 24px; }
    .graph-controls { position: sticky; top: 16px; left: 16px; display: inline-flex; gap: 6px; margin: 16px; padding: 6px; border: 1px solid var(--border); border-radius: 11px; background: var(--surface); box-shadow: var(--shadow); z-index: 3; }
    .graph-tool { min-width: 34px; height: 34px; }
    #graph { display: block; min-width: 900px; width: 100%; height: auto; }
    .edge-line { stroke: color-mix(in srgb, var(--border) 80%, transparent); stroke-width: 2; marker-end: url(#arrow); transition: opacity .15s, stroke .15s; }
    .edge-label { fill: var(--muted); font-size: 11px; paint-order: stroke; stroke: var(--bg); stroke-width: 5px; stroke-linejoin: round; }
    .graph-node { cursor: pointer; outline: none; transition: opacity .15s; }
    .graph-node rect { fill: var(--surface); stroke: var(--border); stroke-width: 1.5; transition: fill .15s, stroke .15s; }
    .graph-node text { fill: var(--text); font-size: 13px; font-weight: 650; pointer-events: none; }
    .graph-node:hover rect, .graph-node:focus rect, .graph-node.selected rect { stroke: var(--accent); fill: var(--surface-2); stroke-width: 2.5; }
    .graph-node[data-kind="CORE"] rect { stroke: var(--core); } .graph-node[data-kind="BRANCH"] rect { stroke: var(--branch); }
    .graph-node[data-kind="ADVANCED"] rect { stroke: var(--advanced); } .graph-node[data-kind="OPTIONAL"] rect { stroke: var(--optional); }
    .graph-faded { opacity: .16; }
    .detail { overflow: auto; padding: 28px 24px; border-left: 1px solid var(--border); background: var(--sidebar); }
    .detail-empty { color: var(--muted); }
    .detail h2 { margin: 8px 0 12px; font-size: 30px; }
    .kind-chip { display: inline-block; padding: 3px 8px; border: 1px solid var(--border); border-radius: 999px; color: var(--accent); font-size: 11px; font-weight: 800; letter-spacing: .08em; }
    .relation-title { margin-top: 28px; color: var(--muted); font-size: 11px; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }
    .relation { width: 100%; margin: 5px 0; padding: 10px 12px; border: 1px solid var(--border); border-radius: 9px; color: var(--text); background: var(--surface); text-align: left; cursor: pointer; }
    .relation small { display: block; color: var(--accent); }
    .detail-action { display: block; width: 100%; margin-top: 12px; padding: 10px; border: 1px solid var(--accent); border-radius: 9px; color: var(--accent); background: transparent; text-align: center; text-decoration: none; cursor: pointer; }
    .detail-action.done { color: var(--core); border-color: var(--core); }
    .palette { position: fixed; inset: 0; display: none; place-items: start center; padding-top: 12vh; background: rgba(3,8,15,.72); backdrop-filter: blur(6px); z-index: 50; }
    .palette.open { display: grid; }
    .palette-box { width: min(700px, calc(100vw - 30px)); overflow: hidden; border: 1px solid var(--border); border-radius: 16px; background: var(--surface); box-shadow: var(--shadow); }
    .palette input { width: 100%; padding: 18px 20px; border: 0; border-bottom: 1px solid var(--border); color: var(--text); background: transparent; outline: none; font-size: 18px; }
    .results { max-height: 55vh; overflow: auto; padding: 8px; }
    .result { display: block; width: 100%; padding: 12px; border: 0; border-radius: 9px; color: var(--text); background: transparent; text-align: left; cursor: pointer; }
    .result:hover, .result.active { background: var(--surface-2); }
    .result small { display: block; color: var(--muted); }
    .empty-state { padding: 24px; color: var(--muted); text-align: center; }
    .mobile-menu { display: none; }
    .search-hidden { display: none !important; }
    .flash { animation: flash 1.3s ease; }
    @keyframes flash { 0%,100% { background: transparent; } 30% { background: color-mix(in srgb, var(--accent) 18%, transparent); } }
    @media (max-width: 880px) {
      .app { display: block; } .main { grid-column: auto; }
      .sidebar { transform: translateX(-101%); transition: transform .2s; box-shadow: var(--shadow); }
      body.sidebar-open .sidebar { transform: translateX(0); }
      .mobile-menu { display: inline-grid; place-items: center; }
      .topbar { padding: 0 14px; } .content { padding: 42px 24px 90px; }
      body[data-view="graph"] .graph-view { grid-template-columns: 1fr; overflow: auto; }
      .graph-view { height: auto; min-height: calc(100vh - 66px); }
      .graph-canvas { min-height: 65vh; } .detail { border-left: 0; border-top: 1px solid var(--border); }
      .crumb { max-width: 34vw; } .view-tab { padding: 6px 8px; }
    }
    @media (prefers-reduced-motion: reduce) { * { scroll-behavior: auto !important; transition: none !important; animation: none !important; } }
  </style>
</head>
<body data-view="content">
  <div class="app">
    <aside class="sidebar" aria-label="Map navigation">
      <div class="brand"><span class="brand-mark">◇</span><span>Cognitive Map<small>interactive notebook</small></span></div>
      <label class="search"><span class="search-icon">⌕</span><input id="sidebar-search" type="search" placeholder="Filter this map" aria-label="Filter this map"><kbd>⌘K</kbd></label>
      <div class="nav-label">Territory</div>
      <nav id="navigation"></nav>
      <div class="sidebar-footer"><a href="__SOURCE_FILE__">Open Markdown source</a><br><span id="progress-label">0 concepts understood</span></div>
    </aside>
    <main class="main">
      <header class="topbar">
        <button class="tool mobile-menu" id="menu-button" aria-label="Open navigation">☰</button>
        <div class="crumb">Map / <strong>__TITLE__</strong></div>
        <div class="toolbar">
          <div class="view-tabs" aria-label="View">
            <button class="view-tab active" data-view-button="content">Read</button>
            <button class="view-tab" data-view-button="graph">Graph</button>
          </div>
          <button class="tool" id="search-button" aria-label="Search" title="Search (⌘K)">⌕</button>
          <button class="tool" id="theme-button" aria-label="Toggle theme" title="Toggle theme">◐</button>
        </div>
      </header>
      <div class="reader-view">
        <div class="content">
          <header class="hero"><div class="eyebrow">Learning territory</div><h1>__TITLE__</h1><p>Explore the argument, follow dependencies, and mark concepts as they become clear.</p></header>
          <article id="article">__CONTENT__</article>
        </div>
      </div>
      <section class="graph-view" aria-label="Relationship graph">
        <div class="graph-canvas">
          <div class="graph-controls"><button class="graph-tool" data-zoom="in" aria-label="Zoom in">+</button><button class="graph-tool" data-zoom="out" aria-label="Zoom out">−</button><button class="graph-tool" data-zoom="reset">Reset</button></div>
          <svg id="graph" role="img" aria-label="Interactive concept dependency graph"></svg>
        </div>
        <aside class="detail" id="detail"><div class="detail-empty"><span class="kind-chip">RELATIONSHIPS</span><h2>Select a concept</h2><p>Choose a node to inspect what it depends on and what it unlocks.</p></div></aside>
      </section>
    </main>
  </div>
  <div class="palette" id="palette" role="dialog" aria-modal="true" aria-label="Search map">
    <div class="palette-box"><input id="palette-input" type="search" placeholder="Search concepts and sections…"><div class="results" id="results"></div></div>
  </div>
  <script>
    const headings = __HEADINGS__;
    const graphData = __GRAPH__;
    const title = __TITLE_JSON__;
    const understoodKey = `cognitive-map:${location.pathname}:understood`;
    const understood = new Set(JSON.parse(localStorage.getItem(understoodKey) || '[]'));
    const byId = new Map(graphData.nodes.map(node => [node.id, node]));
    const outgoing = new Map(graphData.nodes.map(node => [node.id, []]));
    const incoming = new Map(graphData.nodes.map(node => [node.id, []]));
    graphData.edges.forEach(edge => { outgoing.get(edge.from)?.push(edge); incoming.get(edge.to)?.push(edge); });
    resolveContentLinks();

    const navigation = document.querySelector('#navigation');
    headings.filter(item => item.level === 2 || item.level === 3).forEach(item => {
      const button = document.createElement('button');
      button.className = `nav-item ${item.level === 3 ? 'sub' : ''}`;
      button.dataset.anchor = item.anchor;
      button.dataset.search = item.title.toLowerCase();
      button.innerHTML = `<span class="kind-dot ${item.kind || ''}"></span><span>${escapeHtml(item.title.replace(/\s+—\s+(CORE|BRANCH|ADVANCED|OPTIONAL)$/i, ''))}</span>`;
      button.addEventListener('click', () => openSection(item.anchor));
      navigation.append(button);
    });

    function escapeHtml(value) { const node = document.createElement('span'); node.textContent = value; return node.innerHTML; }
    function setView(view) {
      document.body.dataset.view = view;
      document.querySelectorAll('[data-view-button]').forEach(button => button.classList.toggle('active', button.dataset.viewButton === view));
      if (view === 'graph') renderGraph();
      document.body.classList.remove('sidebar-open');
    }
    document.querySelectorAll('[data-view-button]').forEach(button => button.addEventListener('click', () => setView(button.dataset.viewButton)));
    document.querySelectorAll('[data-open-graph]').forEach(button => button.addEventListener('click', () => setView('graph')));

    function openSection(anchor) {
      setView('content');
      requestAnimationFrame(() => {
        const target = document.getElementById(anchor);
        if (!target) return;
        target.scrollIntoView({behavior: 'smooth', block: 'start'});
        target.classList.remove('flash'); void target.offsetWidth; target.classList.add('flash');
      });
    }

    const sidebarSearch = document.querySelector('#sidebar-search');
    sidebarSearch.addEventListener('input', () => {
      const query = sidebarSearch.value.trim().toLowerCase();
      document.querySelectorAll('.nav-item').forEach(item => item.classList.toggle('search-hidden', query && !item.dataset.search.includes(query)));
    });

    const palette = document.querySelector('#palette');
    const paletteInput = document.querySelector('#palette-input');
    const results = document.querySelector('#results');
    function searchableItems() {
      const sectionItems = headings.filter(item => item.level > 1).map(item => ({type:'Section', label:item.title, anchor:item.anchor}));
      const graphItems = graphData.nodes.map(node => ({type:node.kind || 'Concept', label:node.label, node:node.id}));
      const seen = new Set();
      return [...sectionItems, ...graphItems].filter(item => { const key = `${item.type}:${item.label}`; if (seen.has(key)) return false; seen.add(key); return true; });
    }
    function showResults() {
      const query = paletteInput.value.trim().toLowerCase();
      const matches = searchableItems().filter(item => !query || item.label.toLowerCase().includes(query)).slice(0, 12);
      results.innerHTML = matches.length ? '' : '<div class="empty-state">No matching territory</div>';
      matches.forEach((item, index) => {
        const button = document.createElement('button');
        button.className = `result ${index === 0 ? 'active' : ''}`;
        button.innerHTML = `${escapeHtml(item.label)}<small>${escapeHtml(item.type)}</small>`;
        button.addEventListener('click', () => { closePalette(); item.anchor ? openSection(item.anchor) : selectNode(item.node); });
        results.append(button);
      });
    }
    function openPalette() { palette.classList.add('open'); paletteInput.value = ''; showResults(); requestAnimationFrame(() => paletteInput.focus()); }
    function closePalette() { palette.classList.remove('open'); }
    paletteInput.addEventListener('input', showResults);
    paletteInput.addEventListener('keydown', event => {
      const choices = [...results.querySelectorAll('.result')];
      let active = choices.findIndex(item => item.classList.contains('active'));
      if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
        event.preventDefault(); choices[active]?.classList.remove('active');
        active = (active + (event.key === 'ArrowDown' ? 1 : -1) + choices.length) % choices.length;
        choices[active]?.classList.add('active'); choices[active]?.scrollIntoView({block:'nearest'});
      } else if (event.key === 'Enter') choices[Math.max(0, active)]?.click();
    });
    palette.addEventListener('click', event => { if (event.target === palette) closePalette(); });
    document.querySelector('#search-button').addEventListener('click', openPalette);
    document.querySelector('#menu-button').addEventListener('click', () => document.body.classList.toggle('sidebar-open'));

    function renderGraph() {
      const svg = document.querySelector('#graph');
      if (svg.dataset.rendered) return;
      svg.dataset.rendered = 'true';
      svg.setAttribute('viewBox', `0 0 ${graphData.width} ${graphData.height}`);
      svg.innerHTML = '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"></path></marker></defs><g id="graph-stage"></g>';
      const stage = svg.querySelector('#graph-stage');
      graphData.edges.forEach(edge => {
        const source = byId.get(edge.from), target = byId.get(edge.to); if (!source || !target) return;
        const group = document.createElementNS('http://www.w3.org/2000/svg', 'g'); group.dataset.edge = `${edge.from}:${edge.to}`;
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line'); line.classList.add('edge-line');
        line.setAttribute('x1', source.x); line.setAttribute('y1', Number(source.y) + 34); line.setAttribute('x2', target.x); line.setAttribute('y2', Number(target.y) - 34);
        const label = document.createElementNS('http://www.w3.org/2000/svg', 'text'); label.classList.add('edge-label'); label.setAttribute('text-anchor', 'middle');
        label.setAttribute('x', (Number(source.x) + Number(target.x)) / 2); label.setAttribute('y', (Number(source.y) + Number(target.y)) / 2 - 4); label.textContent = edge.label;
        group.append(line, label); stage.append(group);
      });
      graphData.nodes.forEach(node => {
        const group = document.createElementNS('http://www.w3.org/2000/svg', 'g'); group.classList.add('graph-node'); group.dataset.node = node.id; group.dataset.kind = node.kind || 'CONCEPT';
        group.setAttribute('transform', `translate(${node.x} ${node.y})`); group.setAttribute('tabindex', '0'); group.setAttribute('role', 'button'); group.setAttribute('aria-label', node.label);
        const lines = wrapLabel(node.label, 24);
        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect'); rect.setAttribute('x', '-92'); rect.setAttribute('y', String(-24 - (lines.length - 1) * 9)); rect.setAttribute('width', '184'); rect.setAttribute('height', String(48 + (lines.length - 1) * 18)); rect.setAttribute('rx', '13');
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text'); text.setAttribute('text-anchor', 'middle'); text.setAttribute('dominant-baseline', 'middle');
        lines.forEach((line, index) => { const span = document.createElementNS('http://www.w3.org/2000/svg', 'tspan'); span.setAttribute('x', '0'); span.setAttribute('dy', index === 0 ? String(-(lines.length - 1) * 8) : '18'); span.textContent = line; text.append(span); });
        group.append(rect, text); group.addEventListener('click', () => selectNode(node.id)); group.addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') selectNode(node.id); });
        group.addEventListener('mouseenter', () => highlightNeighbors(node.id)); group.addEventListener('mouseleave', clearHighlights); stage.append(group);
      });
    }
    function wrapLabel(label, max) { const words = label.split(/\s+/), lines = []; let current = ''; words.forEach(word => { if (current && `${current} ${word}`.length > max) { lines.push(current); current = word; } else current = current ? `${current} ${word}` : word; }); if (current) lines.push(current); return lines.slice(0,3); }
    function highlightNeighbors(nodeId) {
      const neighbors = new Set([nodeId]); outgoing.get(nodeId)?.forEach(edge => neighbors.add(edge.to)); incoming.get(nodeId)?.forEach(edge => neighbors.add(edge.from));
      document.querySelectorAll('.graph-node').forEach(node => node.classList.toggle('graph-faded', !neighbors.has(node.dataset.node)));
      document.querySelectorAll('[data-edge]').forEach(edge => { const [from,to] = edge.dataset.edge.split(':'); edge.classList.toggle('graph-faded', from !== nodeId && to !== nodeId); });
    }
    function clearHighlights() { document.querySelectorAll('.graph-faded').forEach(item => item.classList.remove('graph-faded')); }
    function matchWords(value) {
      const stop = new Set(['a','an','and','as','at','by','for','from','in','is','of','on','or','the','to','with','etc']);
      return value.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim().split(/\s+/).filter(word => word && !stop.has(word));
    }
    function resolveContentLinks() {
      const candidates = [...document.querySelectorAll('#article h2, #article h3, #article p, #article li, #article blockquote')];
      const fallback = document.querySelector('#cognitive-map') || document.querySelector('#article h2');
      graphData.nodes.forEach(node => {
        if (node.anchor && document.getElementById(node.anchor)) return;
        const labelCompact = node.label.toLowerCase().replace(/[^a-z0-9]+/g, '');
        const labelWords = matchWords(node.label);
        let best = null, bestScore = -Infinity;
        candidates.forEach(candidate => {
          const text = candidate.textContent || '', compact = text.toLowerCase().replace(/[^a-z0-9]+/g, '');
          const words = new Set(matchWords(text));
          const hits = labelWords.filter(word => words.has(word)).length;
          const exact = labelCompact.length > 3 && compact.includes(labelCompact);
          let score = exact ? 110 : (labelWords.length ? (hits / labelWords.length) * 72 : 0);
          if (/^H[23]$/.test(candidate.tagName)) score += 8;
          if (candidate.tagName === 'LI') score += 3;
          score -= Math.min(12, Math.max(0, matchWords(text).length - labelWords.length) / 12);
          if (score > bestScore) { best = candidate; bestScore = score; }
        });
        const target = bestScore >= 20 ? best : fallback;
        if (target) {
          if (!target.id) target.id = `concept-${node.id.toLowerCase()}`;
          node.anchor = target.id;
          node.contentMatch = bestScore;
        }
      });
    }
    function selectNode(nodeId) {
      setView('graph'); renderGraph(); const node = byId.get(nodeId); if (!node) return;
      document.querySelectorAll('.graph-node').forEach(item => item.classList.toggle('selected', item.dataset.node === nodeId));
      const inEdges = incoming.get(nodeId) || [], outEdges = outgoing.get(nodeId) || [];
      const detail = document.querySelector('#detail');
      detail.innerHTML = `<span class="kind-chip">${escapeHtml(node.kind || 'CONCEPT')}</span><h2>${escapeHtml(node.label)}</h2><p>${inEdges.length ? 'Builds on the concepts below.' : 'A starting point in this territory.'}</p>`;
      if (inEdges.length) detail.append(relationGroup('Depends on', inEdges, true));
      if (outEdges.length) detail.append(relationGroup('Unlocks / leads to', outEdges, false));
      if (node.anchor) { const jump = document.createElement('a'); jump.className = 'detail-action'; jump.href = `#${node.anchor}`; jump.textContent = 'Read this concept →'; jump.addEventListener('click', event => { event.preventDefault(); openSection(node.anchor); }); detail.append(jump); }
      const learned = document.createElement('button'); learned.className = `detail-action ${understood.has(nodeId) ? 'done' : ''}`; learned.textContent = understood.has(nodeId) ? '✓ Understood' : 'Mark as understood';
      learned.addEventListener('click', () => { understood.has(nodeId) ? understood.delete(nodeId) : understood.add(nodeId); localStorage.setItem(understoodKey, JSON.stringify([...understood])); learned.classList.toggle('done', understood.has(nodeId)); learned.textContent = understood.has(nodeId) ? '✓ Understood' : 'Mark as understood'; updateProgress(); }); detail.append(learned);
    }
    function relationGroup(label, edges, incomingDirection) {
      const wrapper = document.createElement('div'); wrapper.innerHTML = `<div class="relation-title">${escapeHtml(label)}</div>`;
      edges.forEach(edge => { const relatedId = incomingDirection ? edge.from : edge.to, related = byId.get(relatedId); const button = document.createElement('button'); button.className = 'relation'; button.innerHTML = `${escapeHtml(related?.label || relatedId)}<small>${escapeHtml(edge.label)}</small>`; button.addEventListener('click', () => selectNode(relatedId)); wrapper.append(button); }); return wrapper;
    }
    let zoom = 1;
    document.querySelectorAll('[data-zoom]').forEach(button => button.addEventListener('click', () => { zoom = button.dataset.zoom === 'in' ? Math.min(2, zoom + .2) : button.dataset.zoom === 'out' ? Math.max(.55, zoom - .2) : 1; const svg = document.querySelector('#graph'); const width = graphData.width / zoom, height = graphData.height / zoom; svg.setAttribute('viewBox', `${(graphData.width-width)/2} ${(graphData.height-height)/2} ${width} ${height}`); }));
    function updateProgress() { document.querySelector('#progress-label').textContent = `${understood.size} concept${understood.size === 1 ? '' : 's'} understood`; }
    updateProgress();

    const savedTheme = localStorage.getItem('cognitive-map-theme'); if (savedTheme) document.documentElement.dataset.theme = savedTheme;
    document.querySelector('#theme-button').addEventListener('click', () => { const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'; document.documentElement.dataset.theme = next; localStorage.setItem('cognitive-map-theme', next); });
    document.addEventListener('keydown', event => {
      const typing = /INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName || '');
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); openPalette(); }
      else if (event.key === '/' && !typing) { event.preventDefault(); openPalette(); }
      else if (event.key === 'Escape') { closePalette(); document.body.classList.remove('sidebar-open'); }
      else if (!typing && event.key.toLowerCase() === 'g') setView('content');
      else if (!typing && event.key.toLowerCase() === 'v') setView('graph');
    });
    const observer = new IntersectionObserver(entries => { entries.forEach(entry => { if (!entry.isIntersecting) return; document.querySelectorAll('.nav-item').forEach(item => item.classList.toggle('active', item.dataset.anchor === entry.target.id)); }); }, {rootMargin: '-15% 0px -75%'});
    document.querySelectorAll('[data-heading]').forEach(item => observer.observe(item));
  </script>
</body>
</html>
'''


def build_page(source: Path) -> str:
    markdown = source.read_text(encoding="utf-8")
    first_heading = next((HEADING_PATTERN.match(line) for line in markdown.splitlines() if HEADING_PATTERN.match(line)), None)
    title = plain_text(first_heading.group(2)) if first_heading else source.stem.replace("-", " ").title()
    content, headings = render_markdown(markdown)
    graph = parse_graph(markdown, headings)

    def json_for_script(value: object) -> str:
        return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c")

    return (
        PAGE_TEMPLATE.replace("__TITLE_JSON__", json_for_script(title))
        .replace("__TITLE__", html.escape(title))
        .replace("__SOURCE_FILE__", html.escape(source.name, quote=True))
        .replace("__CONTENT__", content)
        .replace("__HEADINGS__", json_for_script(headings))
        .replace("__GRAPH__", json_for_script(graph))
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Cognitive-map Markdown file")
    parser.add_argument("--output", "-o", type=Path, help="Output HTML path")
    args = parser.parse_args()
    source = args.input.resolve()
    if not source.is_file():
        parser.error(f"input file does not exist: {source}")
    output = args.output.resolve() if args.output else source.with_suffix(".html")
    if output == source:
        parser.error("input and output paths must differ")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_page(source), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
