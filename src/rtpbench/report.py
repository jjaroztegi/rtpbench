"""Static HTML report of a case run: one table per target, then a timeline per call with the
SIP messages, speech and RTP of both sides on one time axis (all from the caller's capture)."""

import json
from html import escape
from pathlib import Path
from typing import Any

from rtpbench import analyze, cases, clock, sip, speechcal

W, LEFT, RIGHT = 1000, 118, 16  # SVG width, label column, right margin
LANE, AXIS = 26, 28
RTP_GAP_NS = 100_000_000  # RTP silent this long: a gap in the lane

CSS = """
:root { color-scheme: light dark; --surface: #fcfcfb; --page: #f9f9f7; --ink: #0b0b0b;
  --ink2: #52514e; --muted: #898781; --grid: #e1e0d9; --axis: #c3c2b7;
  --border: rgba(11,11,11,.10); --caller: #2a78d6; --agent: #eb6834;
  --pass: #0ca30c; --fail: #d03b3b; --inconclusive: #fab219; }
@media (prefers-color-scheme: dark) { :root { --surface: #1a1a19; --page: #0d0d0d;
  --ink: #f0efec; --ink2: #c3c2b7; --grid: #2c2c2a; --axis: #383835;
  --border: rgba(255,255,255,.10); --caller: #3987e5; --agent: #d95926; } }
body { margin: 0 auto; max-width: 1100px; padding: 24px 16px 48px; background: var(--page);
  color: var(--ink); font: 14px/1.45 system-ui, -apple-system, "Segoe UI", sans-serif; }
h1 { font-size: 20px; margin: 0 0 4px; } h2 { font-size: 17px; margin: 32px 0 8px; }
h3 { font-size: 15px; margin: 28px 0 6px; } .meta, .note { color: var(--ink2); margin: 0 0 12px; }
.scroll { overflow-x: auto; border: 1px solid var(--border); border-radius: 6px;
  background: var(--surface); }
table { border-collapse: collapse; width: 100%; min-width: 640px; }
th, td { text-align: left; vertical-align: top; padding: 7px 10px;
  border-bottom: 1px solid var(--grid); }
th { color: var(--ink2); font-weight: 600; font-size: 13px; }
tr:last-child td { border-bottom: 0; }
td.t { min-width: 330px; } .n { font-variant-numeric: tabular-nums; white-space: nowrap; }
.v { white-space: nowrap; }
.icon { font-weight: 700; } .pass .icon { color: var(--pass); }
.fail .icon { color: var(--fail); } .inconclusive .icon { color: var(--inconclusive); }
a { color: inherit; } svg { display: block; width: 100%; min-width: 720px; height: auto; }
svg text { font: 11px system-ui, -apple-system, "Segoe UI", sans-serif; fill: var(--ink2); }
svg .lane { fill: var(--ink2); font-size: 12px; } svg .grid { stroke: var(--grid); }
svg .tick { fill: var(--muted); } svg .caller { fill: var(--caller); stroke: var(--caller); }
svg .agent { fill: var(--agent); stroke: var(--agent); }
svg .hit { fill: transparent; stroke: none; }
.legend { display: flex; gap: 16px; color: var(--ink2); margin: 8px 0; }
.legend i { display: inline-block; width: 12px; height: 12px; border-radius: 2px;
  vertical-align: -1px; margin-right: 6px; }
details { margin: 8px 0 0; } summary { cursor: pointer; color: var(--ink2); }
"""
ICON = {"pass": "✓", "fail": "✗", "inconclusive": "?"}


def _verdict(v: str) -> str:
    return f'<span class="v {v}"><span class="icon" aria-hidden="true">{ICON[v]}</span> {v}</span>'


def _id(run: str) -> str:
    return run.replace("/", "-")


def _group_verdict(recs: list[dict[str, Any]]) -> str:
    """The verdict, with how many repeats gave it, or the mix when it flips."""
    text = cases.verdicts(recs)
    if text.startswith("flips"):
        icon = '<span class="icon" aria-hidden="true">↯</span>'
        return f'<span class="v inconclusive">{icon} {escape(text)}</span>'
    count = text.removeprefix(recs[0]["verdict"])
    return _verdict(recs[0]["verdict"]) + (
        f'<span class="n">{escape(count)}</span>' if count else ""
    )


def _table(groups: list[list[dict[str, Any]]]) -> str:
    """One profile's cases, repeats grouped."""
    reference = groups[0][0]["behaviour"] is not None
    head = ["case", "agent", "expected"] if reference else ["case"]
    head += ["result", "timings, ms (true value within the error bar)", "failed checks"]
    head += ["measured &minus; truth, ms"] if reference else []
    rows = []
    for recs in groups:
        rec = recs[0]
        cells = [f'<a href="#{_id(rec["run"])}">{escape(rec["case"])}</a>']
        if reference:
            cells += [escape(rec["behaviour"]), cases.expected(rec["behaviour"]) or ""]
        timings = "<br>".join(
            f'{escape(n)}: <span class="n">{escape(v)}</span>' for n, v in cases.timings(recs)
        )
        failed = "<br>".join(escape(f) for f in cases.failures(recs))
        cells += [_group_verdict(recs), timings or "-", failed or "-"]
        if reference:
            cells.append(escape(", ".join(cases.errors(recs))) or "-")
        timing = 4 if reference else 2
        rows.append(
            "<tr>"
            + "".join(
                f"<td{' class=t' if i == timing else ''}>{c}</td>" for i, c in enumerate(cells)
            )
            + "</tr>"
        )
    th = "".join(f"<th>{h}</th>" for h in head)
    return f'<div class="scroll"><table><tr>{th}</tr>{"".join(rows)}</table></div>'


def _runs(times: list[int]) -> list[tuple[int, int]]:
    """Packet arrival times as [first, last] runs split at gaps over RTP_GAP_NS."""
    out: list[list[int]] = []
    for t in times:
        if out and t - out[-1][1] <= RTP_GAP_NS:
            out[-1][1] = t
        else:
            out.append([t, t])
    return [(a, b) for a, b in out]


def _said(w: cases.Wire) -> list[tuple[int, int]]:
    """The caller's labelled speech, as captured."""
    pkts = [(t, p) for t, p in w.up if p.pt == w.log.get("pt")]
    if not pkts:
        return []
    st, s0 = analyze.stream(pkts, w.log["pt"]), w.log["seq0"]
    out = []
    for line in w.log.get("said", []):
        spans = [(st.index(s0, a), st.index(s0, b)) for a, b in line["speech"]]
        if edges := speechcal._truth(st, spans):
            out.append(edges)
    return out


def _label(m: sip.Message) -> str:
    return m.first.split()[1] + " " + m.cseq_method if m.status else m.method


def timeline(w: cases.Wire) -> str:
    """SVG lanes: SIP, speech and RTP for each side, on one time axis from the first message."""
    if not w.msgs:
        return '<p class="note">No SIP messages of this call in the capture.</p>'
    audio = [t for t, p in w.down if p.pt == w.log.get("pt")]
    sent = [t for t, p in w.up if p.pt == w.log.get("pt")]
    events = [t for t, p in w.up if p.pt != w.log.get("pt")]
    t0 = w.msgs[0][0]
    end = max([w.msgs[-1][0], *audio[-1:], *sent[-1:]])
    span = max(end - t0, 1_000_000_000)
    plot = W - LEFT - RIGHT

    def x(t: int) -> float:
        return LEFT + plot * (t - t0) / span

    lanes = [
        ("caller SIP", "caller"),
        ("caller speech", "caller"),
        ("caller RTP", "caller"),
        ("agent SIP", "agent"),
        ("agent speech", "agent"),
        ("agent RTP", "agent"),
    ]
    height = LANE * len(lanes) + AXIS + 8
    out = [f'<svg viewBox="0 0 {W} {height}" role="img" aria-label="call timeline">']
    step = next(s for s in (0.5, 1, 2, 5, 10, 15, 30, 60) if span / 1e9 / s <= 12)
    k = 0
    while (sec := k * step) <= span / 1e9:
        gx = x(t0 + round(sec * 1e9))
        out.append(f'<line class="grid" x1="{gx:.1f}" x2="{gx:.1f}" y1="0" y2="{LANE * 6}"/>')
        out.append(
            f'<text class="tick" x="{gx:.1f}" y="{LANE * 6 + 16}" text-anchor="middle">'
            f"{sec:g} s</text>"
        )
        k += 1
    for i, (name, _) in enumerate(lanes):
        out.append(f'<text class="lane" x="0" y="{i * LANE + 17}">{name}</text>')

    def bar(lane: int, side: str, a: int, b: int, h: int, tip: str) -> None:
        y = lane * LANE + (LANE - h) / 2
        x0, x1 = x(a), max(x(b), x(a) + 2)
        out.append(
            f'<rect class="{side}" x="{x0:.1f}" y="{y:.1f}" width="{x1 - x0:.1f}" height="{h}" '
            f'rx="2"><title>{escape(tip)}</title></rect>'
        )

    def secs(t: int) -> str:
        return f"{(t - t0) / 1e9:.3f} s"

    for a, b in _said(w):
        bar(1, "caller", a, b, 12, f"caller speech {secs(a)} to {secs(b)} (labelled)")
    for a, b in w.speech:
        bar(4, "agent", a, b, 12, f"agent speech {secs(a)} to {secs(b)} (webrtcvad)")
    for lane, side, times in ((2, "caller", sent), (5, "agent", audio)):
        for a, b in _runs(times):
            bar(lane, side, a, b, 4, f"{side} RTP {secs(a)} to {secs(b)}")
    for a, b in _runs(events):
        bar(2, "caller", a, b, 14, f"telephone-event {secs(a)} to {secs(b)}")
    label_end = {True: 0.0, False: 0.0}  # where each SIP lane's last label ends
    for t, by_caller, m in w.msgs:
        lane, side = (0, "caller") if by_caller else (3, "agent")
        px, y = x(t), lane * LANE
        tip = f"{secs(t)} {'→' if by_caller else '←'} {m.first} ({m.get('cseq')})"
        out.append(
            f'<line class="{side}" x1="{px:.1f}" x2="{px:.1f}" y1="{y + 14}" y2="{y + 24}" '
            f'stroke-width="2"/><rect class="hit" x="{px - 4:.1f}" y="{y}" width="8" '
            f'height="{LANE}"><title>{escape(tip)}</title></rect>'
        )
        text = _label(m)
        wide = len(text) * 7.0  # 11px text, generous
        right = px + 3 + wide > W  # near the end: put it left of the tick
        lo, hi = (px - 3 - wide, px) if right else (px + 3, px + 3 + wide)
        if lo > label_end[by_caller] + 6:  # label only where it fits
            tx, anchor = (px - 3, "end") if right else (px + 3, "start")
            out.append(
                f'<text x="{tx:.1f}" y="{y + 12}" text-anchor="{anchor}">{escape(text)}</text>'
            )
            label_end[by_caller] = hi
    out.append("</svg>")
    return "".join(out)


def _messages(w: cases.Wire) -> str:
    if not w.msgs:
        return ""
    t0 = w.msgs[0][0]
    rows = "".join(
        f'<tr><td class="n">{(t - t0) / 1e9:.3f}</td>'
        f"<td>{'caller → agent' if c else 'agent → caller'}</td><td>{escape(m.first)}</td>"
        f"<td>{escape(m.get('cseq'))}</td></tr>"
        for t, c, m in w.msgs
    )
    head = "<tr><th>s</th><th>direction</th><th>message</th><th>CSeq</th></tr>"
    return (
        f"<details><summary>SIP messages ({len(w.msgs)})</summary>"
        f'<div class="scroll"><table>{head}{rows}</table></div></details>'
    )


def _markdown(md: str) -> str:
    """A pooled summary (paragraphs and pipe tables, as `analyze._table` writes them)."""
    out: list[str] = []
    rows: list[list[str]] = []

    def flush() -> None:
        if rows:
            th = "".join(f"<th>{escape(c)}</th>" for c in rows[0])
            trs = "".join(
                "<tr>" + "".join(f'<td class="n">{escape(c)}</td>' for c in r) + "</tr>"
                for r in rows[1:]
            )
            out.append(f'<div class="scroll"><table><tr>{th}</tr>{trs}</table></div>')
            rows.clear()

    for line in md.splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not all(set(c) <= set("-: ") for c in cells):  # the --- separator
                rows.append(cells)
        else:
            flush()
            if line.strip():
                out.append(f'<p class="note">{escape(line)}</p>')
    flush()
    return "".join(out)


def render(out: Path, sections: list[tuple[str, str]] | None = None) -> str:
    """The report for a results directory written by `rtpbench cases` or `rtpbench target`:
    per profile, the cases with their repeats grouped; `sections` (title, markdown: turn latency
    and barge-in against a target); then a timeline for the first repeat of each case, and for
    every repeat whose verdict differs from it."""
    from rtpbench.bench import PROFILES

    records = json.loads((out / "results.json").read_text())
    conds = json.loads((out / "conditions.json").read_text())
    target = conds.get("target", "reference agent")
    bars = {cases.Bar(*t["bar"]) for r in records for t in r["timings"]}
    meta = ", ".join(
        f"{k} {str(conds[k]).removeprefix('Python ')}"
        for k in ("date", "commit", "runs", "kernel", "python")
        if k in conds
    )
    by_profile: dict[str, list[list[dict[str, Any]]]] = {}
    for (profile, _, _), recs in cases.groups(records).items():
        by_profile.setdefault(profile, []).append(recs)
    parts = [
        f"<h1>rtpbench conformance cases: {escape(target)}</h1>",
        f'<p class="meta">{escape(meta)}</p>',
    ]
    for profile, groups in by_profile.items():
        netem = PROFILES.get(profile, "")
        parts += [
            f"<h2>{escape(target)}, {escape(profile)}</h2>",
            f'<p class="note">netem per direction: <code>{escape(netem or "none")}</code></p>',
            _table(groups),
        ]
    parts += [
        '<p class="note">True value = measured &minus; error; the error lies within:</p><ul>',
        *(f"<li>[{b.lo:+.1f}, {b.hi:+.1f}] ms: {escape(b.source)}</li>" for b in sorted(bars)),
        "</ul>",
        f'<p class="note">{escape(clock.note(conds.get("clock_steps", [])))}</p>',
    ]
    for title, md in sections or []:
        parts += [f"<h2>{escape(title)}, {escape(target)}</h2>", _markdown(md)]
    parts += [
        "<h2>Calls</h2>",
        '<div class="legend"><span><i style="background:var(--caller)"></i>caller</span>'
        '<span><i style="background:var(--agent)"></i>agent</span>'
        "<span>tall bars: speech · thin: RTP flowing · ticks: SIP (hover for detail)</span></div>",
    ]
    for groups in by_profile.values():
        for recs in groups:
            for rec in [recs[0], *(r for r in recs[1:] if r["verdict"] != recs[0]["verdict"])]:
                w = cases.load(out / rec["run"], rec["profile"])
                title = " · ".join(
                    x
                    for x in (rec["case"], rec["behaviour"], rec["profile"], f"run {rec['repeat']}")
                    if x
                )
                parts += [
                    f'<h3 id="{_id(rec["run"])}">{escape(title)} {_verdict(rec["verdict"])}</h3>',
                    f'<div class="scroll">{timeline(w)}</div>',
                    _messages(w),
                ]
    body = "\n".join(parts)
    return (
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>rtpbench cases: {escape(target)}</title><style>{CSS}</style>"
        f"<body>{body}</body></html>\n"
    )
