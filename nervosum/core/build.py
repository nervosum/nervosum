import os
from nervosum.core.utils import read_yaml
import tempfile
from nervosum.core.image_builder import Director


def execute(args, parser):
    # todo
    config_file = os.path.join(args.dir, args.c)
    config = read_yaml(config_file) # pydantic

    with tempfile.TemporaryDirectory(dir=os.path.abspath(args.dir)) as td:
        director = Director()
        director.setup_builder(args, config, td)
        director.build_image()


