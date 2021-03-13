from typing import Dict, List, Optional, Union

from pydantic import BaseModel, validator


class Interface(BaseModel):
    model_module: str
    model_class: str

    # @validator('model_module')
    # def replace_slash_with_dot_remove_python(cls, x):
    #     return x.replace('/','.').replace('.py','')

    @validator("model_class")
    def no_spaces(cls, x: str):
        if " " in x:
            return ValueError("must not contain a space")
        return x


class Config(BaseModel):
    name: str
    mode: str
    src: str
    tag: Optional[str] = None
    interface: Interface
    requirements: str
    input_schema: List[Dict[str, str]]
    output_schema: Union[List[Dict[str, str]], Dict[str, str]]

    @validator("src")
    def replace_slash_with_dot(cls, x: str):
        return x.replace("/", "")
