import logging
import os
import pkgutil
from abc import ABC, abstractmethod
from shutil import copyfile, copytree, rmtree
from typing import Any

import docker
from jinja2 import Template

from nervosum.config import Config

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel("DEBUG")

client = docker.from_env()


class ImageBuilder(ABC):
    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = source_dir
        self.target_dir = target_dir

    @abstractmethod
    def copy_client_files(self) -> None:
        pass

    @abstractmethod
    def generate_wrapper_files(self, config: Config) -> None:
        pass

    @abstractmethod
    def build_image(self, config: Config) -> None:
        pass

    def copy_source_files_to_target_dir(self):
        for file_or_folder in os.listdir(self.source_dir):
            self.copy(file_or_folder)

    def copy(self, file_or_folder):
        target_location = os.path.join(self.target_dir, file_or_folder)
        if os.path.isdir(file_or_folder):
            copytree(file_or_folder, target_location)
        else:
            copyfile(file_or_folder, target_location)

    def create_target_dir(self):
        if os.path.exists(self.target_dir):
            rmtree(self.target_dir)
            os.mkdir(self.target_dir)
        else:
            os.mkdir(self.target_dir)

    def write_to_file(self, file_name: str, file_content: str):
        with open(os.path.join(self.target_dir, file_name), "w") as f:
            f.write(file_content)

    def render_template(self, mode: str, file: str, **kwargs: Any) -> str:
        file = self.get_pkg_file(mode, file).decode("utf-8")
        if kwargs:
            file = Template(file).render(**kwargs)
        return file

    @staticmethod
    def get_pkg_file(mode: str, file: str) -> bytes:
        file_path = os.path.join("/templates/", mode, file)
        content = pkgutil.get_data("nervosum", file_path)
        if content is not None:
            return content
        else:
            raise FileNotFoundError(
                f"Could not find template " f"file templates/{mode}/{file}"
            )
