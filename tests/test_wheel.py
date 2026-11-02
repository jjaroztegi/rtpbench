import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

from rtpbench import bench


def test_an_installed_rtpbench_finds_its_stacks_and_tags_the_images_as_a_checkout_does(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "-")  # read by compose for the ava stack
    root = Path(bench.__file__).parents[2]
    subprocess.run(["uv", "build", "--wheel", "-q", "-o", tmp_path, root], check=True)
    [wheel] = tmp_path.glob("rtpbench-*.whl")
    site = tmp_path / "site"
    zipfile.ZipFile(wheel).extractall(site)
    probe = (
        "from rtpbench import bench, speech; "
        "assert bench.ROOT == bench.PACKAGE, bench.ROOT; "
        "files = ['compose.yaml', 'Dockerfile', '.dockerignore', 'uri/network.yaml', "
        "'mock/compose.yaml', 'carrier/compose.yaml', 'carrier/opensips.cfg', "
        "*(f'targets/{t}/compose.yaml' for t in bench.TARGETS)]; "
        "assert all((bench.ROOT / f).is_file() for f in files); "
        "assert any(bench.LINES.glob('*.wav')) and speech.clips('tts-'); "
        "import json, pathlib; "
        "stack = bench.Stack(pathlib.Path('out').resolve(), 'ava', carrier='agent'); "
        "print(json.dumps(stack.builds()))"
    )
    env = os.environ | {"PYTHONPATH": str(site)}  # ahead of this checkout's editable install
    res = subprocess.run(
        [sys.executable, "-c", probe], env=env, cwd=tmp_path, capture_output=True, text=True
    )
    assert res.returncode == 0, res.stderr
    stack = bench.Stack(tmp_path / "out", "ava", carrier="agent")
    assert json.loads(res.stdout) == stack.builds()  # rtpbench's own and the target's
