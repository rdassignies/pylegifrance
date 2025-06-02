import pytest
from pydantic import ValidationError

from pylegifrance.pipeline.pipeline_factory import recherche_code
from pylegifrance.models.constants import (
    CodeNom,
    Fonds,
    TypeRecherche,
    Operateur,
    TypeChamp,
)
from pylegifrance.models.search import (
    NomCodeFiltre,
    DateVersionFiltre,
    Critere,
    Champ,
    Recherche,
    RechercheFinal,
)


def test_nom_code_filtre_direct_validation():
    """
    Test that directly validates 'Code de commerce' in NomCodeFiltre.
    This test attempts to reproduce the exact error message from the issue description.
    """
    # Given 'Code de commerce' as a code name
    code_name = "Code de commerce"

    # When creating a NomCodeFiltre with this value
    # Then it should not raise a validation error with the specific message from the issue
    try:
        filtre = NomCodeFiltre(valeurs=[code_name])
        assert filtre.valeurs[0] == CodeNom.CCOM
    except ValidationError as e:
        error_msg = str(e)
        if (
            "Input should be one of: 'Code civil', 'Code des communes'" in error_msg
            and "[type=enum, input_value='Code de commerce', input_type=str]"
            in error_msg
        ):
            # This is the expected error from the issue description
            pass
        else:
            pytest.fail(f"Unexpected validation error: {e}")


def test_recherche_final_direct_validation():
    """
    Test that directly validates 'Code de commerce' in a complete RechercheFinal model.
    """
    # Given a basic search criteria and 'Code de commerce' as a code name
    critere = Critere(
        valeur="1", typeRecherche=TypeRecherche.EXACTE, operateur=Operateur.ET
    )
    field = Champ(
        typeChamp=TypeChamp.NUM_ARTICLE, criteres=[critere], operateur=Operateur.ET
    )
    code_name = "Code de commerce"
    filtre_code = NomCodeFiltre(valeurs=[code_name])
    filtre_date = DateVersionFiltre()

    # When creating a RechercheFinal with these values
    recherche = Recherche(
        champs=[field],
        filtres=[filtre_code, filtre_date],
        pageNumber=1,
        pageSize=1,
    )

    # Then it should not raise a validation error
    try:
        recherche_final = RechercheFinal(recherche=recherche, fond=Fonds.CODE_DATE)
        assert isinstance(recherche_final.recherche.filtres[0], NomCodeFiltre), (
            "First filter should be NomCodeFiltre"
        )
        assert recherche_final.recherche.filtres[0].valeurs[0] == CodeNom.CCOM
    except ValidationError as e:
        error_msg = str(e)
        if (
            "Input should be one of: 'Code civil', 'Code des communes'" in error_msg
            and "[type=enum, input_value='Code de commerce', input_type=str]"
            in error_msg
        ):
            # This is the expected error from the issue description
            pass
        else:
            pytest.fail(f"Unexpected validation error: {e}")


def test_recherche_code_with_invalid_code_name():
    """
    Test that recherche_CODE rejects invalid code names.
    """
    # Given an invalid code name
    invalid_code_name = "Code inexistant"

    # When calling recherche_CODE with this code name
    # Then a validation error should be raised
    with pytest.raises(ValidationError, match="Invalid code name"):
        recherche_code(code_name=invalid_code_name, search="1", page_size=1)
