import argparse
from typing import Callable, Optional

import pytest

from nervosum.cli.nervosum_parser import parse_args


def test_nervosum_parser_invalid_command() -> None:
    with pytest.raises(SystemExit):
        parse_args(["invalid"])


@pytest.fixture
def run() -> Callable:
    def create_run_namespace(
        name: Optional[str] = None, tag: Optional[str] = None
    ) -> argparse.Namespace:
        return argparse.Namespace(
            cmd="run", name=name, nervosum_module="nervosum.core.run", tag=tag
        )

    return create_run_namespace


@pytest.mark.parametrize(
    ["tag", "tag_value", "name", "name_value"],
    [
        (None, None, None, None),
        ("-t", "a_tag", "-n", "a_name"),
        ("--tag", "a_tag", "--name", "a_name"),
    ],
)
def test_nervosum_parser_input_run(
    tag: str, tag_value: str, name: str, name_value: str, run: Callable,
):
    expected = run(name=name_value, tag=tag_value)
    args = ["run"]
    if tag and tag_value:
        args += [tag, tag_value]
    if name and name_value:
        args += [name, name_value]
    assert expected == parse_args(args)


def test_nervosum_parser_input_ls_no_inputs() -> None:
    expected = argparse.Namespace(
        cmd="ls", filter=None, nervosum_module="nervosum.core.list"
    )

    assert expected == parse_args(["ls"])


def test_nervosum_parser_input_ls_filter() -> None:
    expected = argparse.Namespace(
        cmd="ls",
        filter=["key==value", "key2==value2"],
        nervosum_module="nervosum.core.list",
    )

    assert expected == parse_args(
        ["ls", "-f", "key==value", "--filter", "key2==value2"]
    )


def test_nervosum_parser_input_build_no_input() -> None:
    with pytest.raises(SystemExit):
        parse_args(["build"])


def test_nervosum_parser_input_build_dir() -> None:
    expected = argparse.Namespace(
        cmd="build",
        c="nervosum.yaml",
        dir=".",
        nervosum_module="nervosum.core.build",
    )

    assert expected == parse_args(["build", "."])


def test_nervosum_parser_input_build_config() -> None:
    expected = argparse.Namespace(
        cmd="build", c="a_file", dir=".", nervosum_module="nervosum.core.build"
    )

    assert expected == parse_args(["build", ".", "-c", "a_file"])


def test_nervosum_parser_input_build_config_overwrite() -> None:
    expected = argparse.Namespace(
        cmd="build", c="a_file", dir=".", nervosum_module="nervosum.core.build"
    )

    assert expected == parse_args(
        ["build", ".", "-c", "b_file", "-c", "a_file"]
    )
