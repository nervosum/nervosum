from pathlib import Path
from typing import List, Optional, Union

import yaml
from pydantic import BaseModel, validator


class SchemaField(BaseModel):
    name: str
    type: str


class DeploymentField(BaseModel):
    mode: str
    platform_tag: Optional[str] = None

    @validator("mode")
    def mode_in_http_batch(cls, v: str):
        if v not in ["batch", "http"]:
            raise ValueError(f"Mode {v} not yet supported")
        return v

    @validator("platform_tag")
    def check_platform_tag(cls, v, values):
        if values["mode"] == "batch":
            if v is None:
                raise ValueError("Must provide platform tag")
        return v


class Interface(BaseModel):
    model_module: str
    model_class: str

    @validator("model_class")
    def no_spaces(cls, x: str):
        if " " in x:
            return ValueError("must not contain a space")
        return x


class NervosumConfig(BaseModel):
    name: str
    deployment: DeploymentField
    src: str
    tag: Optional[str] = None
    interface: Interface
    requirements: str
    input_schema: List[SchemaField]
    output_schema: Union[List[SchemaField], SchemaField]

    @validator("src")
    def replace_slash_with_dot(cls, v: str):
        return v.replace("/", ".")


def get_config(config_file: Union[Path, str]) -> NervosumConfig:
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

    return NervosumConfig(**config)
