import logging
import os
from abc import ABC, abstractmethod

import docker

from nervosum import utils
from nervosum.config import Config

logger = logging.getLogger(__name__)

client = docker.from_env()


class ImageBuilder(ABC):
    mode: str

    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = source_dir
        self.target_dir = target_dir

    @abstractmethod
    def generate_wrapper_files(self, config: Config) -> None:
        pass

    def copy_client_files_to_build_dir(self) -> None:
        logger.info("Copying client files")
        utils.create_dir(self.target_dir)
        utils.copy_contents_to_target_dir(self.source_dir, self.target_dir)

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
