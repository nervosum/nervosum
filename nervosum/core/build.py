import argparse
import os
import tempfile

from nervosum.config import get_config
from nervosum.core.builders.batch_image_builder import BatchImageBuilder
from nervosum.core.builders.flask_image_builder import FlaskImageBuilder
from nervosum.core.builders.image_builder import ImageBuilder


def execute(args: argparse.Namespace):
    config_file = os.path.join(args.dir, args.c)
    config = get_config(config_file)

    with tempfile.TemporaryDirectory(dir=os.path.abspath(args.dir)) as td:
        if config.mode == "batch":
            builder: ImageBuilder = BatchImageBuilder(
                source_dir=args.dir, target_dir=td
            )
        elif config.mode == "http":
            builder = FlaskImageBuilder(source_dir=args.dir, target_dir=td)
        else:
            raise NotImplementedError(
                f"Currently no support for mode {config.mode}"
            )

        builder.generate_wrapper_files(config)
        builder.copy_client_files_to_build_dir()
        builder.build_image(config)
