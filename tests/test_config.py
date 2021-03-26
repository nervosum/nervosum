from typing import Callable, List

import pytest
from pydantic import ValidationError

from nervosum.config import Interface, NervosumConfig, get_config


@pytest.fixture
def generate_config() -> Callable:
    def fun(
        name: str = None,
        mode: str = None,
        platform_tag: str = None,
        tag: str = None,
        src: str = None,
        interface: str = None,
        input_schema: str = None,
        requirements: str = None,
        output_schema: str = None,
    ):
        config = f"""
name: {name if name else 'a_name'}

mode: {mode if mode else 'batch'}

{"platform_tag: " + platform_tag if platform_tag else ""}

tag: {tag if tag else 'a_tag'}

src: {src if src else 'a_src'}

interface:
{interface if interface else chr(10).join(["  model_module: a_module",
"  model_class: a_class"])}

requirements: {requirements if requirements else "a_requirements_file"}

input_schema:
{input_schema if input_schema else chr(10).join([
"  - name: field",
"    type: a_type"])}
output_schema:
{output_schema if output_schema else chr(10).join([
"  - name: prediction",
"    type: a_type"])}
"""
        return config

    return fun


def test_get_config_default(tmp_path, generate_config) -> None:

    file = tmp_path / "file"
    file.write_text(generate_config())
    config = get_config(file)
    assert isinstance(config, NervosumConfig)
    assert config.name == "a_name"
    assert config.mode == "batch"
    assert config.src == "a_src"
    assert config.tag == "a_tag"
    assert config.platform_tag is None
    assert isinstance(config.interface, Interface)
    assert config.interface.model_module == "a_module"
    assert config.interface.model_class == "a_class"
    assert config.requirements == "a_requirements_file"
    assert isinstance(config.input_schema, List)
    assert config.input_schema[0].name == "field"
    assert config.input_schema[0].type == "a_type"
    assert config.output_schema[0].name == "prediction"
    assert config.output_schema[0].type == "a_type"


def test_get_config_mode_batch(tmp_path, generate_config) -> None:
    file = tmp_path / "file"
    file.write_text(generate_config(mode="batch"))
    config = get_config(file)
    assert config.mode == "batch"


def test_get_config_mode_http(tmp_path, generate_config) -> None:
    file = tmp_path / "file"
    file.write_text(generate_config(mode="http"))
    config = get_config(file)
    assert config.mode == "http"


def test_get_config_mode_unsupported(tmp_path, generate_config) -> None:
    file = tmp_path / "file"
    file.write_text(generate_config(mode="unsupported"))
    with pytest.raises(ValidationError):
        get_config(file)
