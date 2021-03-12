import logging
import os
import pkgutil
import re
from abc import ABC, abstractmethod
from shutil import copyfile, copytree, rmtree
from typing import Any, Dict

import docker
from jinja2 import Template

client = docker.from_env()

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel("DEBUG")


class ImageBuilder(ABC):
    def __init__(self, args: Dict[str, Any], config: Dict[str, Any], td: str):
        self.tempdir = td
        self.args = args
        self.config = config

    @abstractmethod
    def copy_client_files(self) -> None:
        pass

    @abstractmethod
    def copy_wrapper_files(self) -> None:
        pass

    @abstractmethod
    def build_image(self) -> None:
        pass


class Director:
    """
    The Director is only responsible for executing the building steps in a
    particular sequence. It is helpful when producing products according to a
    specific order or configuration. Strictly speaking, the Director class is
    optional, since the client can control builders directly.
    """

    # _builder: ImageBuilder = None

    def __init__(self) -> None:
        pass

    @property
    def builder(self) -> ImageBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: ImageBuilder) -> None:
        """
        The Director works with any builder instance that the client code
        passes to it. This way, the client code may alter the final type of
        the newly assembled product.

        Args:
            builder: Set an ImageBuilder instance
        """
        self._builder = builder

    def setup_builder(self, args, config, td):
        if config["mode"] == "batch":
            self.builder = BatchImageBuilder(args, config, td)
        elif config["mode"] == "http":
            self.builder = FlaskImageBuilder(args, config, td)

    """
    The Director can construct several product variations using the same
    building steps.
    """

    def build_image(self) -> None:
        self.builder.copy_client_files()
        self.builder.copy_wrapper_files()
        self.builder.build_image()


class BatchImageBuilder(ImageBuilder):
    pass


class FlaskImageBuilder(ImageBuilder):
    def build_image(self):
        logger.info("Building docker image")
        os.chdir(self.tempdir)
        client.images.build(
            path=".",
            labels={
                "owner": "nervosum",
                "mode": self.config["mode"],
                "name": self.config["name"].lower(),
                "tag": self.config["tag"].lower(),
            },
            tag=[
                f'nervosum/{self.config["name"].lower()}:{self.config["tag"]}'
            ],
            quiet=False,
        )

    def copy_wrapper_files(self):
        logger.info("Copying wrapper files")

        wrapper_requirements = render_template(
            self.config["mode"], "wrapper-requirements.txt"
        )

        m = re.search(
            r"(?P<module>.*).(?P<extension>py)$",
            self.config["interface"]["file"],
        ).groupdict()
        model_module = m["module"].replace("/", ".")
        # interface = src/model.py  ==> src.model

        wrapper_file = render_template(
            self.config["mode"],
            "wrapper.py.j2",
            model_module=model_module,
            model_class=self.config["interface"]["class"],
            input_schema=self.config["input_schema"],
            metadata=None,
        )

        dockerfile = render_template(
            self.config["mode"],
            "Dockerfile.j2",
            requirements_file=self.config["requirements"],
        )
        dockerfile_path = os.path.join(self.tempdir, "Dockerfile")

        with open(os.path.join(self.tempdir, "wrapper.py"), "w") as f:
            f.write(wrapper_file)
        with open(
            os.path.join(self.tempdir, "wrapper_requirements.txt"), "w"
        ) as f:
            f.write(wrapper_requirements)
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile)

    def copy_client_files(self):
        logger.info("Copying client files")

        if os.path.exists(self.tempdir):
            rmtree(self.tempdir)

        for file_or_folder in os.listdir(self.args.dir):
            if file_or_folder == self.args.c:
                continue
            if os.path.isdir(file_or_folder):
                if not os.path.exists(self.tempdir):
                    os.mkdir(self.tempdir)
                copytree(
                    file_or_folder, os.path.join(self.tempdir, file_or_folder)
                )
            else:
                if not os.path.exists(self.tempdir):
                    os.mkdir(self.tempdir)
                copyfile(
                    file_or_folder, os.path.join(self.tempdir, file_or_folder)
                )


def render_template(mode, file, **kwargs):
    file = get_pkg_file(mode, file).decode("utf-8")
    if kwargs:
        file = Template(file).render(**kwargs)
    return file


def get_pkg_file(mode: str, file: str):
    filepath = os.path.join("/templates/", mode, file)
    # f"/templates/{config['mode']}/wrapper-requirements.txt"
    return pkgutil.get_data("nervosum", filepath)
