import logging
import os
from abc import ABC, abstractmethod

import docker

from nervosum.config import NervosumConfig
from nervosum.core import utils

logger = logging.getLogger(__name__)

client = docker.from_env()


class ImageBuilder(ABC):
    mode: str

    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = source_dir
        self.target_dir = target_dir

    @abstractmethod
    def generate_wrapper_files(self, config: NervosumConfig) -> None:
        pass

    def copy_client_files_to_build_dir(self) -> None:
        logger.info("Copying client files")
        utils.create_dir(self.target_dir, mode="skip")
        utils.copy_contents_to_target_dir(self.source_dir, self.target_dir)

    def build_image(
        self, config: NervosumConfig, silent: bool = False
    ) -> None:
        logger.info("Building docker image")

        os.chdir(self.target_dir)
        build_stream = client.api.build(
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
        if silent:
            return

        utils.print_build_stream(build_stream)
