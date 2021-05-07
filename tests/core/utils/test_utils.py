import os
from shutil import rmtree

import pytest

from nervosum.core import utils


def test_create_target_dir(tmp_path) -> None:
    d = tmp_path / "sub"
    utils.create_dir(d, mode="overwrite")
    assert d.exists()
    rmtree(str(d))
    utils.create_dir(d, mode="skip")
    assert d.exists()
    rmtree(str(d))
    utils.create_dir(d, mode="fail")
    assert d.exists()


def test_create_target_dir_exists(tmp_path) -> None:
    d = tmp_path / "sub"
    d.mkdir()
    file = d / "file"
    file.write_text("content")
    with pytest.raises(FileExistsError):
        utils.create_dir(d, mode="fail")

    utils.create_dir(d, mode="skip")
    assert len(os.listdir(str(d))) == 1

    utils.create_dir(d, mode="overwrite")
    assert len(os.listdir(str(d))) == 0
