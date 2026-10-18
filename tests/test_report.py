import json
from pathlib import Path
from typing import Any

from rtpbench import report


def _set(d: Path, conds: dict[str, Any], recs: list[tuple[str, str | None, str]]) -> None:
    d.mkdir(parents=True)
    (d / "conditions.json").write_text(json.dumps({"date": "2026-10-17T20:36:20", **conds}))
    (d / "results.json").write_text(
        json.dumps(
            [
                {
                    "profile": "clean",
                    "repeat": i + 1,
                    "case": c,
                    "behaviour": b,
                    "verdict": v,
                    "run": f"clean/{i + 1:02}/{c}" + (f"-{b}" if b else ""),
                }
                for i, (c, b, v) in enumerate(recs)
            ]
        )
    )


def test_index(tmp_path: Path) -> None:
    runs = {"profiles": ["clean"], "runs": 2}
    _set(tmp_path / "pub/ref", runs, [("greeting", "good", "pass"), ("greeting", "bad", "fail")])
    _set(
        tmp_path / "pub/tgt",
        runs | {"target": "livekit"},
        [("greeting", None, "pass"), ("greeting", None, "fail"), ("hold", None, "fail")],
    )
    _set(tmp_path / "pub/uri", {"target": "sip:agent@host"}, [("bye", None, "pass")])
    (tmp_path / "pub/cal").mkdir()
    (tmp_path / "pub/cal/summary.md").write_text("")
    html = report.index(tmp_path)
    assert html.index("pub/ref/report.html") < html.index("pub/tgt/report.html")  # reference first
    assert 'href="pub/ref/report.html#clean-01-greeting-good"' in html
    assert '<span class="n">2/2</span>' in html  # both reference calls gave the expected verdict
    assert "flips: pass 1, fail 1" in html
    assert "<td>hold</td><td>-</td>" in html  # not run on the reference
    assert 'href="pub/cal/summary.md"' in html
    html = report.index(tmp_path, "/blob/abc/results/")
    assert 'href="/blob/abc/results/pub/cal/summary.md"' in html
    assert 'href="pub/ref/report.html"' in html  # only Markdown moves
