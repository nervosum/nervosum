import argparse
import os
import tempfile

from nervosum.core.builders.director import Director
from nervosum.utils import read_yaml


def execute(args: argparse.Namespace):
    config_file = os.path.join(args.dir, args.c)
    config = read_yaml(config_file)

    with tempfile.TemporaryDirectory(dir=os.path.abspath(args.dir)) as td:
        director = Director()
        director.setup_builder(
            target_dir=td, source_dir=args.dir, mode=config.mode
        )
        director.build(config)
