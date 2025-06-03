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
)
from pylegifrance.models.constants import Operateur

from pylegifrance.models.consult import (
    CodeTableMatieres,
    LegiSommaireConsult,
)

from pylegifrance.models.constants import CodeNom, Fonds, Nature, TypeChamp


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
    field = Champ(typeChamp=TypeChamp.VISA, criteres=[criteria], operateur=Operateur.ET)

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
    field = Champ(
        typeChamp=TypeChamp.VISA, criteres=[basic_criteria], operateur=Operateur.ET
    )
    filtre = NatureFiltre(valeurs=[Nature.LOI, Nature.DECRET])

    # When a search and final search are created
    search = Recherche(champs=[field], filtres=[filtre])
    final = RechercheFinal(recherche=search, fond=Fonds.LODA_DATE)

    # Then the final search should have the correct properties
    assert final.fond == Fonds.LODA_DATE
    assert len(final.recherche.champs) == 1
    assert final.recherche.champs[0].typeChamp.value == "VISA"
    assert isinstance(final.recherche.filtres[0], NatureFiltre), (
        "First filter should be NatureFiltre"
    )
    assert final.recherche.filtres[0].valeurs == [Nature.LOI, Nature.DECRET]


@pytest.mark.parametrize(
    "field_type, fond, expected_error",
    [
        # Invalid field type for CODE_DATE fond
        (
            TypeChamp.VISA,
            Fonds.CODE_DATE,
            r"TypeChamp TypeChamp.VISA is not valid for the fond Fonds.CODE_DATE",
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
    field = Champ(
        typeChamp=TypeChamp.NUM_ARTICLE,
        criteres=[basic_criteria],
        operateur=Operateur.ET,
    )
    filtre1 = NomCodeFiltre(valeurs=["Code civil"])
    filtre2 = DateVersionFiltre()

    # When a search and final search are created with the filters
    search = Recherche(champs=[field], filtres=[filtre1, filtre2])
    final = RechercheFinal(recherche=search, fond=Fonds.CODE_DATE)

    # Then the final search should have the correct filter properties
    assert final.fond == Fonds.CODE_DATE
    assert len(final.recherche.filtres) == 2
    assert isinstance(final.recherche.filtres[0], NomCodeFiltre)
    assert isinstance(final.recherche.filtres[1], DateVersionFiltre)


@pytest.mark.parametrize(
    "facet_type, fond, expected_error",
    [
        # Invalid facet type for LODA_DATE fond
        (
            "NOM_CODE",
            Fonds.LODA_DATE,
            r"Facet TypeFacettes.NOM_CODE is not valid for the fond Fonds.LODA_DATE",
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
        typeChamp=TypeChamp.NUM_ARTICLE,
        criteres=[basic_criteria],
        operateur=Operateur.ET,
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


def test_nom_code_filtre_with_valid_code_names():
    """
    Test that NomCodeFiltre accepts valid code names.
    """
    # Given valid code names from the CodeNom enum
    valid_code_names = [
        "Code civil",  # String value
        CodeNom.CCIV,  # Enum value
        "CCIV",  # Enum member name
    ]

    # When creating a NomCodeFiltre with these values
    filtre = NomCodeFiltre(valeurs=valid_code_names)

    # Then the filter should have the correct values
    assert len(filtre.valeurs) == 3
    assert all(isinstance(code, CodeNom) for code in filtre.valeurs)
    assert CodeNom.CCIV in filtre.valeurs


def test_nom_code_filtre_with_code_de_commerce():
    """
    Test that NomCodeFiltre accepts 'Code de commerce' as a valid code name.
    """
    # Given 'Code de commerce' as a code name
    code_name = "Code de commerce"

    # When creating a NomCodeFiltre with this value
    # Then it should not raise a validation error
    try:
        filtre = NomCodeFiltre(valeurs=[code_name])
        assert len(filtre.valeurs) == 1
        assert filtre.valeurs[0] == CodeNom.CCOM
    except ValidationError as e:
        pytest.fail(f"NomCodeFiltre validation failed for 'Code de commerce': {e}")


def test_nom_code_filtre_with_code_de_commerce_in_recherche():
    """
    Test that 'Code de commerce' is accepted in a complete Recherche model.
    """
    # Given a basic search criteria
    critere = Critere(
        valeur="7", typeRecherche=TypeRecherche.EXACTE, operateur=Operateur.ET
    )
    field = Champ(
        typeChamp=TypeChamp.NUM_ARTICLE, criteres=[critere], operateur=Operateur.ET
    )

    # And 'Code de commerce' as a code name
    code_name = "Code de commerce"
    filtre_code = NomCodeFiltre(valeurs=[code_name])
    filtre_date = DateVersionFiltre()

    # When creating a Recherche with these values
    # Then it should not raise a validation error
    try:
        recherche = Recherche(
            champs=[field],
            filtres=[filtre_code, filtre_date],
            pageNumber=1,
            pageSize=10,
        )
        assert len(recherche.filtres) == 2
        assert isinstance(recherche.filtres[0], NomCodeFiltre), (
            "First filter should be NomCodeFiltre"
        )
        assert recherche.filtres[0].valeurs[0] == CodeNom.CCOM
    except ValidationError as e:
        pytest.fail(f"Recherche validation failed for 'Code de commerce': {e}")


def test_nom_code_filtre_with_code_de_commerce_in_recherche_final():
    """
    Test that 'Code de commerce' is accepted in a complete RechercheFinal model.
    """
    # Given a basic search criteria
    critere = Critere(
        valeur="7", typeRecherche=TypeRecherche.EXACTE, operateur=Operateur.ET
    )
    field = Champ(
        typeChamp=TypeChamp.NUM_ARTICLE, criteres=[critere], operateur=Operateur.ET
    )

    # And 'Code de commerce' as a code name
    code_name = "Code de commerce"
    filtre_code = NomCodeFiltre(valeurs=[code_name])
    filtre_date = DateVersionFiltre()

    # When creating a Recherche and RechercheFinal with these values
    # Then it should not raise a validation error
    try:
        recherche = Recherche(
            champs=[field],
            filtres=[filtre_code, filtre_date],
            pageNumber=1,
            pageSize=10,
        )
        recherche_final = RechercheFinal(recherche=recherche, fond=Fonds.CODE_DATE)
        assert isinstance(
            recherche_final.recherche.filtres[0], NomCodeFiltre
        )  # Make sure it's the right type
        assert recherche_final.recherche.filtres[0].valeurs[0] == CodeNom.CCOM
    except ValidationError as e:
        pytest.fail(f"RechercheFinal validation failed for 'Code de commerce': {e}")


def test_nom_code_filtre_with_invalid_code_name():
    """
    Test that NomCodeFiltre rejects invalid code names.
    """
    # Given an invalid code name
    invalid_code_name = "Code inexistant"

    # When attempting to create a NomCodeFiltre with this value
    # Then a validation error should be raised
    with pytest.raises(ValidationError, match="Invalid code name"):
        NomCodeFiltre(valeurs=[invalid_code_name])
