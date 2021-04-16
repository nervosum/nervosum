import json
import logging
import os
import pkgutil
from pathlib import Path
from shutil import copyfile, copytree, rmtree
from typing import Any, Union

from jinja2 import Template

logger = logging.getLogger(__name__)


def create_dir(dir: Union[str, Path], mode: str = "overwrite"):
    if os.path.exists(dir) and mode == "overwrite":
        rmtree(dir)
        os.mkdir(dir)
    elif os.path.exists(dir) and mode == "skip":
        pass
    elif os.path.exists(dir) and mode == "fail":
        raise FileExistsError(f"{dir} already exists")
    else:
        os.mkdir(dir)


def copy_contents_to_target_dir(
    source_dir: Union[str, Path], target_dir: Union[str, Path]
):
    for file_or_folder in os.listdir(source_dir):
        copy(file_or_folder, target_dir)


def copy(file_or_folder: Union[str, Path], target_dir: Union[str, Path]):
    target_location = os.path.join(target_dir, file_or_folder)
    if os.path.isdir(file_or_folder):
        copytree(file_or_folder, target_location)
    else:
        copyfile(file_or_folder, target_location)


def write_to_file(file_name: str, file_content: str):
    with open(file_name, "w") as f:
        f.write(file_content)


def render_template(mode: str, file: str, **kwargs: Any) -> str:
    file = get_pkg_file(mode, file).decode("utf-8")
    if kwargs:
        file = Template(file).render(**kwargs)
    return file


def get_pkg_file(mode: str, file: str) -> bytes:
    file_path = os.path.join("templates", mode, file)
    content = pkgutil.get_data("nervosum", file_path)
    if content is not None:
        return content
    else:
        raise FileNotFoundError(
            f"Could not find template " f"file templates/{mode}/{file}"
        )


def print_build_stream(build_stream) -> None:
    for msg in build_stream:
        msgs = msg.decode("utf8").split("\r\n")
        for line in msgs:
            if line:
                line_dict = json.loads(line)
                if "stream" in line_dict:
                    print(line_dict["stream"], end="")


def print_container_stream(container_stream) -> None:
    for msg in container_stream:
        print(msg.decode("utf-8"), end="")
