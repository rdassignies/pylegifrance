"""API wrapper models for JURI."""

from typing import Optional
from pydantic import Field

from pylegifrance.models.generated.model import (
    JuriConsultRequest,
    JuriConsultWithAncienId,
    TexteSimple,
)
from pylegifrance.models.juri.base import JuriBaseModel


class ConsultRequest(JuriBaseModel):
    """Request to consult a JURI text."""

    searched_string: Optional[str] = Field(
        None, alias="searchedString", description="Search text that led to consultation"
    )
    text_id: str = Field(..., alias="textId", description="Text identifier")

    def to_api_model(self) -> JuriConsultRequest:
        """Convert to generated model for API calls."""
        return JuriConsultRequest(**self.model_dump(by_alias=True))


class ConsultByAncienIdRequest(JuriBaseModel):
    """Request to consult by ancien ID."""

    ancien_id: Optional[str] = Field(
        None, alias="ancienId", description="Legacy ID for JURI text consultation"
    )

    def to_api_model(self) -> JuriConsultWithAncienId:
        """Convert to generated model for API calls."""
        return JuriConsultWithAncienId(**self.model_dump(by_alias=True))


class ConsultResponse(JuriBaseModel):
    """Response from text consultation."""

    text: Optional[TexteSimple] = Field(None, description="Text content")
    execution_time: Optional[int] = Field(None, alias="executionTime")
    dereferenced: Optional[bool] = Field(None, description="Indexable by robots")

    @classmethod
    def from_api_model(cls, model) -> "ConsultResponse":
        """
        Create from generated model or dictionary.

        Parameters
        ----------
        model : Union[ConsultJuriTextResponse, dict]
            The model or dictionary to convert from.

        Returns
        -------
        ConsultResponse
            The converted response.
        """
        if isinstance(model, dict):
            return cls(**model)
        else:
            return cls(**model.model_dump())
