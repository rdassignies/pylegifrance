"""Core domain models for JURI."""

from typing import List, Optional
from pydantic import Field

from pylegifrance.models.generated.model import TexteSimple, TexteLien


class Decision(TexteSimple):
    """
    Judicial decision domain model.

    Extends the generated TexteSimple model with JURI-specific fields.
    """

    siege_appel: Optional[str] = Field(alias="siegeAppel", default=None)
    avocat_general: Optional[str] = Field(alias="avocatGl", default=None)
    liens: List[TexteLien] = Field(default=[])
