"""Base classes for JURI module."""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class JuriBaseModel(BaseModel):
    """Base model with consistent configuration for all JURI models."""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        str_strip_whitespace=True,
        validate_assignment=True,
    )
