import argparse
from typing import List, Optional

from _pytest.capture import CaptureFixture

from nervosum.cli.nervosum_parser import generate_parser


def get_actual_actions(
    y: Optional[List[argparse.Action]],
) -> List[argparse.Action]:
    if y is not None:
        return list(
            filter(lambda x: not isinstance(x, argparse._HelpAction), y)
        )

    return []


def test_nervosum_parser_command_help(capsys: CaptureFixture) -> None:
    p = generate_parser()
    p.print_help()
    captured = capsys.readouterr()
    for x in ["build", "run", "ls"]:
        assert x in captured.out

    assert len(p._actions) == 2


def test_nervosum_parser_build_args() -> None:
    p = generate_parser()
    actions = p._actions[1]
    assert actions
    assert isinstance(actions.choices, dict)
    build_actions = actions.choices["build"]._actions
    arguments = [x.dest for x in get_actual_actions(build_actions)]
    assert "c" in arguments
    assert "dir" in arguments


def test_nervosum_parser_run_args() -> None:
    p = generate_parser()
    actions = p._actions[1]
    assert actions
    assert isinstance(actions.choices, dict)
    run_actions = actions.choices["run"]._actions
    arguments = [x.dest for x in get_actual_actions(run_actions)]
    assert "tag" in arguments
    assert "name" in arguments


def test_nervosum_parser_ls_args() -> None:
    p = generate_parser()
    actions = p._actions[1]
    assert actions
    assert isinstance(actions.choices, dict)
    ls_actions = actions.choices["ls"]._actions
    arguments = [x.dest for x in get_actual_actions(ls_actions)]
    assert "filter" in arguments
