from pathlib import Path
from typing import Any, Dict, Union

import yaml


def read_yaml(config_file: Union[Path, str]) -> Dict[str, Any]:
    """
    Function to parse a config file with the yml extension

    Args:
        config_file (pathlib.Path, str): The file to parse

    Returns:
        A dict object containing all key value pairs as defined in the config
        file

    """
    with open(config_file) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        config = yaml.load(file, Loader=yaml.FullLoader)

    return config
