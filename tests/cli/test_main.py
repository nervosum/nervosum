import argparse
from unittest import mock
from unittest.mock import MagicMock

from pytest import MonkeyPatch

from nervosum.cli import nervosum_parser
from nervosum.cli.main import main


@mock.patch("nervosum.core.list.execute")
def test_main(mocked_core_module: MagicMock, monkeypatch: MonkeyPatch) -> None:

    args = argparse.Namespace(
        cmd="ls", filter=None, nervosum_module="nervosum.core.list"
    )
    monkeypatch.setattr(
        nervosum_parser, "parse_args", lambda: args,
    )
    main()
    mocked_core_module.assert_called_once_with(args)
