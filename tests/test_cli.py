import shutil
import subprocess
import wave
from pathlib import Path

import pytest

from rtpbench import bench, cases, cli
from rtpbench.bench import PROFILES, TARGETS


def test_no_arguments_list_the_commands_and_help_the_valid_names(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as e:
        cli.main([])
    assert e.value.code == 2
    listing = capsys.readouterr().out
    for command in ("calibrate", "cases", "target", "report", "check", "analyze", "index"):
        assert f"    {command} " in listing
    assert "    agent " not in listing  # run inside containers, not by hand

    with pytest.raises(SystemExit):
        cli.main(["target", "--help"])
    text = " ".join(capsys.readouterr().out.split())
    for name in [*PROFILES, *cases.CASES, *TARGETS]:
        assert f" {name}," in text or f" {name} " in text


@pytest.mark.parametrize(
    ("argv", "error"),
    [
        (["sip:agent@203.0.113.7", "--mock"], "--mock, --carrier"),
        (["sip:agent:secret@203.0.113.7"], "password"),
        (["sip:agent@127.0.0.1"], "own address"),
        (["sip:agent@203.0.113.7", "--advertise", "40000"], "HOST:PORT"),
        (["sip:agent@203.0.113.7", "--advertise", "198.51.100.1:65530"], "PORT 1-65528"),
        (["livekit", "--network", "n"], "with a URI only"),
    ],
)
def test_target_refuses(argv: list[str], error: str, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        cli.main(["target", *argv])
    assert error in capsys.readouterr().err


def test_engine_settings_are_recorded_as_compose_resolves_them(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AVA_EGRESS_PACER", "")  # ${AVA_EGRESS_PACER:-true}: the default
    monkeypatch.setenv("OPENAI_REASONING_EFFORT", "")  # ${OPENAI_REASONING_EFFORT-low}: empty
    assert bench._engine(TARGETS["ava"][1])["AVA_EGRESS_PACER"] == "true"
    assert bench._engine(TARGETS["aivc"][1])["OPENAI_REASONING_EFFORT"] == ""


@pytest.mark.parametrize(
    ("result", "says"),
    [
        (FileNotFoundError(), "no docker command"),
        (subprocess.TimeoutExpired([], 30), "answered in 30 s"),
        (
            (1, "The command 'docker' could not be found in this WSL 2 distro.", ""),
            "WSL integration",
        ),
        ((1, "", "Cannot connect to the Docker daemon. Is it running?"), "Cannot connect"),
        ((0, "27.5.1", ""), "the server is 27.5.1"),
        ((0, "29.9.1", ""), None),
    ],
)
def test_docker_preflight_names_the_cause(
    result: Exception | tuple[int, str, str], says: str | None, monkeypatch: pytest.MonkeyPatch
) -> None:
    def run(*a: object, **k: object) -> subprocess.CompletedProcess[str]:
        if isinstance(result, Exception):
            raise result
        code, out, err = result
        return subprocess.CompletedProcess([], code, out + "\n", err)

    monkeypatch.setattr(subprocess, "run", run)
    if says is None:
        bench.docker()
        return
    with pytest.raises(SystemExit) as e:
        bench.docker()
    assert says in str(e.value)


def test_target_lists_every_unusable_line_before_it_starts(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    shutil.copy(bench.LINES / "turn-00.wav", tmp_path)
    (tmp_path / "prompt.wav").write_text("not audio")
    (tmp_path / "prompt-00.wav").mkdir()
    with wave.open(str(tmp_path / "turn-01.wav"), "wb") as w:
        w.setparams((1, 2, 8000, 0, "NONE", "not compressed"))
        w.writeframes(bytes(16000))  # silence
    only = "greeting,refer,latency,barge-in"
    with pytest.raises(SystemExit):
        cli.main(["target", "sip:agent@203.0.113.7", "--lines", str(tmp_path), "--only", only])
    err = capsys.readouterr().err
    for problem in (
        "prompt.wav: not 8 kHz mono 16-bit PCM",
        "no transfer.wav",
        "turn-01.wav: no speech",
        "prompt-00.wav: Is a directory",
        "no interrupt-*.wav",
    ):
        assert f"\n  {problem}" in err
    assert "turn-00.wav" not in err
