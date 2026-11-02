import json
import re
import shutil
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
