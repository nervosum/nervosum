import argparse
import logging
from datetime import datetime
from typing import Iterator, List, Optional, Union

import docker
import timeago
from dateutil import parser as datetime_parser
from docker.models.images import Image

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel("DEBUG")

client = docker.from_env()


def get_nervosum_images() -> Iterator[Image]:
    return iter(client.images.list(filters={"reference": "nervosum/*"}))


def pretty_print_images(images: Iterator[Image]) -> None:
    now = datetime.utcnow()
    print(f"{'TAG':15s}{'NAME':15s}{'CREATED':20s}LABELS")
    for image in images:
        time_last_run = datetime_parser.parse(image.attrs["Created"]).replace(
            tzinfo=None
        )
        time_since_last_run = timeago.format(time_last_run, now)

        labels = ", ".join(f"{k}='{v}'" for k, v in image.labels.items())
        print(
            f"{image.short_id[7:]:15s}{image.labels.get('name'):15s}"
            f"{time_since_last_run:20s}{labels}"
        )


def filter_images(
    images: Iterator[Image], filters: Union[List[str], str]
) -> Iterator[Image]:

    if not isinstance(filters, list):
        filters = list(filters)

    for a_filter in filters:
        k, v = a_filter.split("=")
        if k == "id":
            images = filter(lambda image: v in image.id, images,)
        else:
            images = filter(lambda image: v in image.labels.get(k), images)
    return images


def get_images(
    filters: Optional[Union[List[str], str]] = None
) -> Iterator[Image]:
    images = get_nervosum_images()
    if filters is not None:
        images = filter_images(images, filters)
    return images


def execute(args: argparse.Namespace) -> None:
    images = get_nervosum_images()
    if args.filter:
        images = filter_images(images, args.filter)
    pretty_print_images(images)
