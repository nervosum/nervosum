import argparse
import logging
import signal
import sys
import types
from typing import Iterator

import docker
from dateutil import parser as datetime_parser
from docker.models.containers import Container
from docker.models.images import Image

from nervosum.core.list import filter_images, get_images

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel("DEBUG")

client = docker.from_env()


def execute(args: argparse.Namespace) -> None:
    conf = {}

    images = get_images()

    if args.name:
        images = filter_images(images, [f"name={args.name}"])

    if args.tag:
        images = filter_images(images, [f"tag={args.tag}"])
    else:
        logger.warning("No container name given, running latest image.")

    latest_image = filter_latest_image(images)

    if latest_image.labels["mode"] == "http":
        conf["ports"] = {"5000/tcp": 5000}

    logger.info(f"Running {latest_image}")
    container = client.containers.run(latest_image, detach=True, **conf)
    print(type(container))
    set_kill_signal(container)

    while True:
        continue


def set_kill_signal(container: Container):
    def signal_handler(sig: int, frame: types.FrameType) -> None:
        logger.info("\rStopping container...")
        container.stop()
        logger.info("Done")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)


def filter_latest_image(images: Iterator[Image]) -> Image:
    latest_image = max(
        images, key=lambda x: datetime_parser.parse(x.attrs["Created"])
    )
    return latest_image
