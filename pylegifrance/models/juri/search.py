"""Search models and functionality for JURI."""

from typing import List, Optional
from pydantic import Field

from pylegifrance.models.juri.base import JuriBaseModel
from pylegifrance.models.juri.constants import (
    SortOptions,
    PublicationStatus,
    FacettesJURI,
)
from pylegifrance.models.generated.model import (
    SearchRequestDTO,
    RechercheSpecifiqueDTO,
    ChampDTO,
    CritereDTO,
    FiltreDTO,
    TypePagination,
    Operateur,
    TypeChamp,
    TypeRecherche,
    Fond,
)


class SearchRequest(JuriBaseModel):
    """JURI search request model."""

    search: str = Field("", description="Search text or keywords")
    publication_bulletin: Optional[List[PublicationStatus]] = Field(
        default=None, description="Publication status filter"
    )
    sort: SortOptions = Field(default=SortOptions.RELEVANCE)
    field: TypeChamp = Field(default=TypeChamp.all)
    search_type: TypeRecherche = Field(default=TypeRecherche.un_des_mots)
    page_size: int = Field(default=5, ge=1, le=100)
    page_number: int = Field(default=1, ge=1)

    # Advanced options
    formatter: bool = Field(default=True, description="Extract only specific fields")
    fetch_all: bool = Field(default=False, description="Fetch all results")
    keys: Optional[List[str]] = Field(
        default=None, description="Specific field extraction keys"
    )
    juridiction_judiciaire: Optional[List[str]] = Field(default=None)

    def to_api_model(self) -> SearchRequestDTO:
        """Convert to generated model for API calls."""
        criteria = self._create_criteria()
        field = self._create_field(criteria)
        filters = self._create_filters()
        search_spec = self._create_search_specification(field, filters)

        return SearchRequestDTO(recherche=search_spec, fond=Fond.juri)

    def _create_criteria(self) -> CritereDTO:
        """Create search criteria from the search text."""
        return CritereDTO(
            valeur=self.search,
            operateur=Operateur.et,
            typeRecherche=self.search_type,
            proximite=None,
            criteres=None,
        )

    def _create_field(self, criteria: CritereDTO) -> ChampDTO:
        """Create search field with the given criteria."""
        return ChampDTO(
            criteres=[criteria], operateur=Operateur.et, typeChamp=self.field
        )

    def _create_filters(self) -> List[FiltreDTO]:
        """Create filters based on search parameters."""
        filters = []

        # Add publication bulletin filter if specified
        if self.publication_bulletin:
            filters.append(self._create_publication_filter())

        # Add jurisdiction judiciaire filter if specified
        if self.juridiction_judiciaire:
            filters.append(self._create_jurisdiction_filter())

        return filters

    def _create_publication_filter(self) -> FiltreDTO:
        """Create publication bulletin filter."""
        # Ensure publication_bulletin is not None before using it as an iterable
        pub_values = []
        if self.publication_bulletin:
            pub_values = [p.value for p in self.publication_bulletin]

        return FiltreDTO(
            facette=FacettesJURI.CASSATION_TYPE_PUBLICATION_BULLETIN.value,
            valeurs=pub_values,
            dates=None,
            singleDate=None,
            multiValeurs=None,
        )

    def _create_jurisdiction_filter(self) -> FiltreDTO:
        """Create jurisdiction filter."""
        return FiltreDTO(
            facette=FacettesJURI.JURIDICTION_JUDICIAIRE.value,
            valeurs=self.juridiction_judiciaire,
            dates=None,
            singleDate=None,
            multiValeurs=None,
        )

    def _create_search_specification(
        self, field: ChampDTO, filters: List[FiltreDTO]
    ) -> RechercheSpecifiqueDTO:
        """Create search specification with fields and filters."""
        return RechercheSpecifiqueDTO(
            champs=[field],
            filtres=filters,
            pageNumber=self.page_number,
            pageSize=self.page_size,
            sort=self.sort.value,
            fromAdvancedRecherche=False,
            secondSort="ID",
            typePagination=TypePagination.defaut,
            operateur=Operateur.et,
        )


class SearchResponse(JuriBaseModel):
    """JURI search response model."""

    total_results: int = Field(alias="totalNbResult")
    execution_time: int = Field(alias="executionTime")
    results: List[dict] = Field(default=[])
    page_number: int = Field(alias="pageNumber")
    page_size: int = Field(alias="pageSize")
