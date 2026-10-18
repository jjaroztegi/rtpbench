import pytest

from rtpbench import cases, cli
from rtpbench.bench import PROFILES, TARGETS


def test_no_arguments_list_the_commands_and_help_the_valid_names(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as e:
        cli.main([])
    assert e.value.code == 2
    listing = capsys.readouterr().out
    for command in ("calibrate", "cases", "target", "report", "analyze", "index"):
        assert f"    {command} " in listing
    assert "    agent " not in listing  # run inside containers, not by hand

    with pytest.raises(SystemExit):
        cli.main(["target", "--help"])
    text = " ".join(capsys.readouterr().out.split())
    for name in [*PROFILES, *cases.CASES, *TARGETS]:
        assert f" {name}," in text or f" {name} " in text
