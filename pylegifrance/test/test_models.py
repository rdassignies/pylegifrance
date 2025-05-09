import pytest
from pydantic import ValidationError

from pylegifrance.models.search import (
    Critere,
    Champ,
    NomCodeFiltre,
    DateVersionFiltre,
    NatureFiltre,
    Recherche,
    RechercheFinal,
    TypeRecherche,
    Operateur,
)

from pylegifrance.models.consult import (
    CodeTableMatieres,
    LegiSommaireConsult,
)


@pytest.fixture
def basic_criteria():
    """Fixture to provide a basic search criteria."""
    # Given a basic search value and parameters
    return Critere(
        valeur="7", typeRecherche=TypeRecherche.EXACTE, operateur=Operateur.ET
    )


def test_field_with_valid_criteria(basic_criteria):
    """
    Test that a field with valid criteria is correctly constructed.
    """
    # Given a valid criteria
    criteria = basic_criteria

    # When a field is created with the criteria
    field = Champ(typeChamp="VISA", criteres=[criteria], operateur=Operateur.ET)

    # Then the field should have the correct properties
    assert field.typeChamp.value == "VISA"
    assert len(field.criteres) == 1
    assert field.criteres[0].valeur == "7"
    assert field.operateur == Operateur.ET


def test_recherche_final_with_valid_field_and_fond(basic_criteria):
    """
    Test that a RechercheFinal with valid field and fond is correctly constructed.
    """
    # Given a valid field and filter
    field = Champ(typeChamp="VISA", criteres=[basic_criteria], operateur=Operateur.ET)
    filtre = NatureFiltre(valeurs=["LOI", "DECRET"])

    # When a search and final search are created
    search = Recherche(champs=[field], filtres=[filtre])
    final = RechercheFinal(recherche=search, fond="LODA_DATE")

    # Then the final search should have the correct properties
    assert final.fond == "LODA_DATE"
    assert len(final.recherche.champs) == 1
    assert final.recherche.champs[0].typeChamp.value == "VISA"
    assert final.recherche.filtres[0].valeurs == ["LOI", "DECRET"]


@pytest.mark.parametrize(
    "field_type, fond, expected_error",
    [
        # Invalid field type for CODE_DATE fond
        (
            "VISA",
            "CODE_DATE",
            "TypeChamp TypeChamp.VISA is not valid for the fond Fonds.CODE_DATE",
        ),
        # Add more invalid combinations as needed
    ],
)
def test_recherche_final_with_invalid_field_type(
    field_type, fond, expected_error, basic_criteria
):
    """
    Test that validation correctly rejects invalid field types for specific fonds.
    """
    # Given a field with an invalid type for the specified fond
    field = Champ(
        typeChamp=field_type, criteres=[basic_criteria], operateur=Operateur.ET
    )
    filtre = NomCodeFiltre(valeurs=["Code civil"])
    search = Recherche(champs=[field], filtres=[filtre])

    # When attempting to create a RechercheFinal with the invalid combination
    # Then validation should fail with the expected error message
    with pytest.raises(ValidationError, match=expected_error):
        RechercheFinal(recherche=search, fond=fond)


def test_recherche_final_with_valid_filters(basic_criteria):
    """
    Test that a RechercheFinal with valid filters is correctly constructed.
    """
    # Given valid field and filters
    field = Champ(typeChamp="NUM_ARTICLE", criteres=[basic_criteria], operateur="ET")
    filtre1 = NomCodeFiltre(valeurs=["Code civil"])
    filtre2 = DateVersionFiltre()

    # When a search and final search are created with the filters
    search = Recherche(champs=[field], filtres=[filtre1, filtre2])
    final = RechercheFinal(recherche=search, fond="CODE_DATE")

    # Then the final search should have the correct filter properties
    assert final.fond == "CODE_DATE"
    assert len(final.recherche.filtres) == 2
    assert isinstance(final.recherche.filtres[0], NomCodeFiltre)
    assert isinstance(final.recherche.filtres[1], DateVersionFiltre)


@pytest.mark.parametrize(
    "facet_type, fond, expected_error",
    [
        # Invalid facet type for LODA_DATE fond
        (
            "NOM_CODE",
            "LODA_DATE",
            "Facet TypeFacettes.NOM_CODE is not valid for the fond Fonds.LODA_DATE",
        ),
        # Add more invalid combinations as needed
    ],
)
def test_recherche_final_with_invalid_facet_type(
    facet_type, fond, expected_error, basic_criteria
):
    """
    Test that validation correctly rejects invalid facet types for specific fonds.
    """
    # Given a field and a filter with an invalid facet type for the specified fond
    field = Champ(
        typeChamp="NUM_ARTICLE", criteres=[basic_criteria], operateur=Operateur.ET
    )
    filtre1 = NomCodeFiltre(valeurs=["Code civil"])
    filtre2 = DateVersionFiltre()

    # When a search is created with the invalid filter
    search = Recherche(champs=[field], filtres=[filtre1, filtre2])

    # Then validation should fail with the expected error message when creating the final search
    with pytest.raises(ValidationError, match=expected_error):
        RechercheFinal(recherche=search, fond=fond)


def test_deprecated_route_warning():
    """
    Test that a deprecation warning is raised when using a deprecated route.
    """
    # Given a text ID for a code
    text_id = "LEGITEXT000006070721"

    # When creating a CodeTableMatieres instance
    # Then a deprecation warning should be raised
    with pytest.warns(
        DeprecationWarning, match="La route 'consult/code/tableMatieres' est dépréciée"
    ):
        code_table = CodeTableMatieres(textId=text_id)

    # And the model should still be usable despite the warning
    assert code_table.textId == text_id
    assert code_table.route == "consult/code/tableMatieres"

    # When creating the recommended replacement
    legi_sommaire = LegiSommaireConsult(textId=text_id)

    # Then it should have the correct properties
    assert legi_sommaire.textId == text_id
    assert legi_sommaire.route == "consult/legi/tableMatieres"
