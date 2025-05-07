from typing import List, ClassVar
from pylegifrance.models.constants import SupplyEnum


from pydantic import BaseModel, Field


# SUGGEST CONTROLLER


class SuggestSupplyRequest(BaseModel):
    """Requête de suggestion d'une recherche textuelle dans un ou
    plusieurs fonds
    """

    searchText: str = Field(..., example="mariage", description="Texte à rechercher")
    supplies: List[SupplyEnum] = Field(
        ...,
        example=["JORF", "JURI"],
        description="Liste des fonds dans lesquels exécuter la recherche pour la suggestion",
    )
    documentsDits: bool = Field(
        True, description="Indicateur de la présence de documents dits"
    )

    route: ClassVar[str] = "suggest"
