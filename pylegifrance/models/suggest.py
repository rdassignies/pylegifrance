from typing import List, ClassVar
from pylegifrance.models.constants import SupplyEnum
from pydantic import BaseModel, Field


class SuggestSupplyRequest(BaseModel):
    """Requête de suggestion d'une recherche textuelle dans un ou
    plusieurs fonds
    """

    searchText: str = Field(..., description="Texte à rechercher", examples=["mariage"])
    supplies: List[SupplyEnum] = Field(
        default_factory=list,
        description="Liste des fonds dans lesquels exécuter la recherche pour la suggestion",
        examples=[[SupplyEnum.JORF, SupplyEnum.JURI]],
    )
    documentsDits: bool = Field(
        True, description="Indicateur de la présence de documents dits"
    )

    route: ClassVar[str] = "suggest"
