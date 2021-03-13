import argparse
import os
import tempfile

from nervosum.core.image_builder import Director
from nervosum.core.utils import read_yaml


def execute(args: argparse.Namespace, parser: argparse.ArgumentParser):
    config_file = os.path.join(args.dir, args.c)
    config = read_yaml(config_file)

    with tempfile.TemporaryDirectory(dir=os.path.abspath(args.dir)) as td:
        director = Director()
        director.setup_builder(args, config, td)
        director.build_image()
