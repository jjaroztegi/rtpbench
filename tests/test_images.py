import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from rtpbench import ROOT, bench
from rtpbench.bench import TARGETS, Stack


@pytest.fixture
def root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A copy of the checkout's stack files and package, which bench reads instead."""
    root = tmp_path / "root"
    root.mkdir()
    for name in ("compose.yaml", "Dockerfile"):
        shutil.copyfile(ROOT / name, root / name)
    for name in ("corpus", "uri", "mock", "carrier", "targets", "src"):
        shutil.copytree(ROOT / name, root / name)
    monkeypatch.setattr(bench, "ROOT", root)
    monkeypatch.setattr(bench, "PACKAGE", root / "src" / "rtpbench")
    for k in ("OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY"):
        monkeypatch.setenv(k, "-")
    return root


def builds(root: Path, target: str | None) -> dict[str, str]:
    return Stack(root / "out", target, carrier="agent").builds()


@pytest.mark.parametrize("target", [None, *TARGETS])
def test_compose_tags_each_built_image_with_the_hash_of_its_build(
    root: Path, target: str | None
) -> None:
    stack = Stack(root / "out", target, carrier="agent")
    built = stack.builds()
    services = json.loads(stack.compose("config", "--format", "json"))["services"]
    assert built == {name: s["image"] for name, s in services.items() if "build" in s}
    assert built["router"] == f"{bench.REGISTRY}/{bench._image_tag()}"
    for name, image in built.items():
        if name != "router":  # its own content hash
            assert re.fullmatch(r"[^:]+:[^:]+-[0-9a-f]{12}", image), image


def test_editing_a_build_changes_its_image_s_tag_and_an_unrelated_file_none(root: Path) -> None:
    before = builds(root, "ava")
    agent = root / "targets" / "livekit" / "agent.py"  # not in this stack
    agent.write_text(agent.read_text() + "# edited\n")
    assert builds(root, "ava") == before

    compose = root / "targets" / "ava" / "compose.yaml"
    old = "ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1"  # the engine's dockerfile_inline
    assert old in compose.read_text()
    compose.write_text(compose.read_text().replace(old, "ENV PYTHONUNBUFFERED=1"))
    after = builds(root, "ava")
    assert after["engine"] != before["engine"]
    assert after["engine"].startswith(before["engine"].rpartition("-")[0] + "-")  # pin kept
    for name in ("router", "carrier-media", "carrier-sip"):
        assert after[name] == before[name]

    constraints = root / "targets" / "ava" / "constraints.txt"  # the engine's pins context
    constraints.write_text(constraints.read_text() + "\n")
    assert builds(root, "ava")["engine"] != after["engine"]


@pytest.mark.parametrize(
    ("target", "service"), [("aivc", "engine"), ("ava", "engine"), ("livekit", "sip")]
)
def test_a_target_built_from_a_checkout_is_tagged_by_its_commit_and_files(
    root: Path, tmp_path: Path, target: str, service: str
) -> None:
    src = tmp_path / "checkout"
    src.mkdir()
    (src / "main.py").write_text("print('hi')\n")
    (src / ".gitignore").write_text(".venv/\n")
    git = ["git", "-C", str(src), "-c", "user.name=t", "-c", "user.email=t@t"]
    for cmd in (["init", "-q"], ["add", "."], ["commit", "-qm", "x"]):
        subprocess.run([*git, *cmd], check=True)
    out = src / "results" / "run"  # a run's results inside the checkout: no part of it
    out.mkdir(parents=True)

    def files(stack: Stack) -> list[Path]:
        return [f for f in (stack.source or Path()).rglob("*") if f.is_file()]

    def tag() -> str:
        stack = Stack(out, target, carrier="agent", source=src)
        try:
            copied = {f.relative_to(stack.source or "").as_posix() for f in files(stack)}
            assert copied == {".gitignore", "main.py"}  # not .git, .venv or the results
            return stack.builds()[service]
        finally:
            shutil.rmtree(stack.source or "")

    pinned = builds(root, target).get(service, "")
    clean = tag()
    commit = bench.checkout(src, out)
    assert re.fullmatch(rf".+:{commit['commit'][:7]}-[0-9a-f]{{12}}", clean), clean
    assert clean != pinned
    (out / "caller.pcap").write_bytes(b"x")
    (src / ".venv").mkdir()
    (src / ".venv" / "lib.py").write_text("ignored\n")
    assert tag() == clean
    assert bench.checkout(src, out)["dirty"] is False
    assert bench.checkout(src)["dirty"] is True  # the results are untracked files to git

    (src / "__pycache__").mkdir()
    (src / "__pycache__" / "main.pyc").write_bytes(b"x")
    subprocess.run([*git, "add", "-f", "__pycache__"], check=True)  # tracked: still left out
    assert tag() == clean
    subprocess.run([*git, "rm", "-rq", "--cached", "__pycache__"], check=True)
    shutil.rmtree(src / "__pycache__")
    (out / "a.txt").write_text("a\n")  # a rename within the results: two fields, both aside
    subprocess.run([*git, "add", "-f", str(out / "a.txt")], check=True)
    subprocess.run([*git, "commit", "-qm", "results"], check=True)
    subprocess.run([*git, "mv", str(out / "a.txt"), str(out / "b.txt")], check=True)
    assert bench.checkout(src, out)["dirty"] is False

    (src / "main.py").write_text("print('changed')\n")  # uncommitted: same commit, new files
    assert bench.checkout(src, out)["dirty"] is True
    assert tag() != clean
    with pytest.raises(ValueError, match="not a git checkout"):
        bench.checkout(tmp_path)
