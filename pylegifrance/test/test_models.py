#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 12:12:19 2023

@author: raphael
"""

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


def test_champ_valide():
    """
    Teste si un champ est valide avec des critères corrects.
    """
    criteria = Critere(
        valeur="7", typeRecherche=TypeRecherche.EXACTE, operateur=Operateur.ET
    )
    field = Champ(typeChamp="VISA", criteres=[criteria], operateur=Operateur.ET)

    # Vérification du type du champ et des critères
    assert field.typeChamp.value == "VISA"
    assert len(field.criteres) == 1
    assert field.criteres[0].valeur == "7"
    assert field.operateur == Operateur.ET


def test_RechercheFinal_fond_type_champs_valide():
    """
    Teste si une recherche finale est valide avec un fond correct
    et un champ autorisé.
    """
    criteria = Critere(valeur="7", typeRecherche="EXACTE", operateur="ET")
    field = Champ(typeChamp="VISA", criteres=[criteria], operateur=Operateur.ET)

    # Création des filtres et recherche finale
    # Use a valid filter for LODA_DATE (NatureFiltre instead of NomCodeFiltre)
    filtre = NatureFiltre(valeurs=["LOI", "DECRET"])
    search = Recherche(champs=[field], filtres=[filtre])
    final = RechercheFinal(recherche=search, fond="LODA_DATE")

    # Assertions pour vérifier la validité du modèle
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
def test_RechercheFinal_invalid_field_type(field_type, fond, expected_error):
    """
    Tests that validation correctly rejects invalid field types for specific fonds.
    """
    criteria = Critere(valeur="7", typeRecherche="EXACTE", operateur="ET")
    field = Champ(typeChamp=field_type, criteres=[criteria], operateur=Operateur.ET)

    filtre = NomCodeFiltre(valeurs=["Code civil"])
    search = Recherche(champs=[field], filtres=[filtre])

    # Validation should fail with the expected error message
    with pytest.raises(ValidationError, match=expected_error):
        RechercheFinal(recherche=search, fond=fond)


def test_RechercheFinal_fond_type_filtres_valide():
    """
    Teste si une recherche finale avec des filtres valides
    est correctement construite.
    """
    criteria = Critere(valeur="7", typeRecherche="EXACTE", operateur="ET")
    field = Champ(typeChamp="NUM_ARTICLE", criteres=[criteria], operateur="ET")

    filtre = NomCodeFiltre(valeurs=["Code civil"])
    filtre2 = DateVersionFiltre()

    search = Recherche(champs=[field], filtres=[filtre, filtre2])
    final = RechercheFinal(recherche=search, fond="CODE_DATE")

    # Assertions sur le contenu des filtres et la recherche
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
def test_RechercheFinal_invalid_facet_type(facet_type, fond, expected_error):
    """
    Tests that validation correctly rejects invalid facet types for specific fonds.
    """
    criteria = Critere(valeur="7", typeRecherche="EXACTE", operateur="ET")
    field = Champ(typeChamp="NUM_ARTICLE", criteres=[criteria], operateur=Operateur.ET)

    # Create a filter with the specified facet type
    if facet_type == "NOM_CODE":
        filtre = NomCodeFiltre(valeurs=["Code civil"])
    else:
        # Add handling for other facet types if needed
        filtre = NomCodeFiltre(valeurs=["Code civil"])

    filtre2 = DateVersionFiltre()

    search = Recherche(champs=[field], filtres=[filtre, filtre2])

    # Validation should fail with the expected error message
    with pytest.raises(ValidationError, match=expected_error):
        RechercheFinal(recherche=search, fond=fond)


def test_deprecated_route_warning():
    """
    Tests that a deprecation warning is raised when using a deprecated route.
    """
    # Test that CodeTableMatieres raises a deprecation warning
    with pytest.warns(
        DeprecationWarning, match="La route 'consult/code/tableMatieres' est dépréciée"
    ):
        code_table = CodeTableMatieres(textId="LEGITEXT000006070721")

    # Verify the model is still usable despite the warning
    assert code_table.textId == "LEGITEXT000006070721"
    assert code_table.route == "consult/code/tableMatieres"

    # Test that the recommended replacement works
    legi_sommaire = LegiSommaireConsult(textId="LEGITEXT000006070721")
    assert legi_sommaire.textId == "LEGITEXT000006070721"
    assert legi_sommaire.route == "consult/legi/tableMatieres"
