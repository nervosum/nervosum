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


class BatchImageBuilder(ImageBuilder):
    mode = "batch"

    def copy_client_files(self) -> None:
        pass

    def generate_wrapper_files(self, config: Config) -> None:
        pass

    def build_image(self, config: Config) -> None:
        pass


class FlaskImageBuilder(ImageBuilder):
    mode = "http"

    def build_image(self, config: Config) -> None:
        logger.info("Building docker image")

        os.chdir(self.target_dir)
        client.images.build(
            path=".",
            labels={
                "owner": "nervosum",
                "mode": self.mode,
                "name": config.name.lower(),
                "tag": config.tag,
            },
            tag=[f"nervosum/{config.name.lower()}:{config.tag}"],
            quiet=False,
        )

    def generate_wrapper_files(self, config: Config) -> None:
        logger.info("Copying wrapper files")

        wrapper_requirements = render_template(
            self.mode, "wrapper-requirements.txt"
        )

        wrapper_file = render_template(
            self.mode,
            "wrapper.py.j2",
            model_module=config.interface.model_module,
            model_class=config.interface.model_class,
            input_schema=config.input_schema,
            output_schema=config.output_schema,
            metadata=None,
        )

        dockerfile = render_template(
            self.mode, "Dockerfile.j2", requirements_file=config.requirements,
        )

        write_to_file(self.target_dir, "wrapper.py", wrapper_file)
        write_to_file(
            self.target_dir, "wrapper_requirements.txt", wrapper_requirements
        )
        write_to_file(self.target_dir, "Dockerfile", dockerfile)

    def copy_client_files(self) -> None:
        logger.info("Copying client files")
        self.create_target_dir()
        self.copy_source_files_to_target_dir()

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


def write_to_file(target_dir: str, file_name: str, file_content: str):
    with open(os.path.join(target_dir, file_name), "w") as f:
        f.write(file_content)


def render_template(mode: str, file: str, **kwargs: Any) -> str:
    file = get_pkg_file(mode, file).decode("utf-8")
    if kwargs:
        file = Template(file).render(**kwargs)
    return file


def get_pkg_file(mode: str, file: str) -> bytes:
    file_path = os.path.join("/templates/", mode, file)
    content = pkgutil.get_data("nervosum", file_path)
    if content is not None:
        return content
    else:
        raise FileNotFoundError(
            f"Could not find template " f"file templates/{mode}/{file}"
        )
