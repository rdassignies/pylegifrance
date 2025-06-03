"""Filter models for JURI search."""

from typing import List
from pydantic import Field

from pylegifrance.models.juri.base import JuriBaseModel
from pylegifrance.models.juri.constants import (
    FilterTypes,
    JuridictionJudiciaire,
    FormationsJudiciaires,
    CoursAppel,
    PublicationStatus,
)


class BaseFilter(JuriBaseModel):
    """Base filter with common structure."""

    facette: FilterTypes
    valeurs: List[str]


class JurisdictionFilter(BaseFilter):
    """Filter for judicial jurisdictions."""

    facette: FilterTypes = FilterTypes.JURIDICTION_JUDICIAIRE
    valeurs: List[JuridictionJudiciaire]


class FormationFilter(BaseFilter):
    """Filter for judicial formations."""

    facette: FilterTypes = FilterTypes.FORMATION
    valeurs: List[FormationsJudiciaires]


class CourAppelFilter(BaseFilter):
    """Filter for appeal courts."""

    facette: FilterTypes = FilterTypes.COUR_APPEL
    valeurs: List[CoursAppel]


class PublicationFilter(BaseFilter):
    """Filter for publication status."""

    facette: FilterTypes = FilterTypes.PUBLICATION_BULLETIN
    valeurs: List[PublicationStatus] = Field(default=[PublicationStatus.PUBLISHED])
