from abc import ABC
from typing import Optional, Type

import pydantic


class AbstractAd(pydantic.BaseModel, ABC):
    name: str
    title: str
    description: str

    @pydantic.field_validator("name")
    @classmethod
    def name_length(cls, v: str) -> str:
        if len(v) > 100:
            raise ValueError("Maxima length of name is 100")
        return v

    @pydantic.field_validator("title")
    @classmethod
    def title_length(cls, v: str) -> str:
        if len(v) > 500:
            raise ValueError("Maxima length of title is 500")
        return v

    @pydantic.field_validator("description")
    @classmethod
    def title_length(cls, v: str) -> str:
        if len(v) > 1000:
            raise ValueError("Maxima length of description is 1000")
        return v


class CreateAd(AbstractAd):
    name: str
    title: str
    description: str


class UpdateAd(AbstractAd):
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None


SCHEMA_CLASS = Type[CreateAd | UpdateAd]
SCHEMA = CreateAd | UpdateAd
