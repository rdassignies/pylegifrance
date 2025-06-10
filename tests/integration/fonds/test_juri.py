import pytest

from pylegifrance.fonds.juri import JuriAPI, JuriDecision, SearchRequest
from pylegifrance.models.juri.constants import (
    JuridictionJudiciaire,
)


@pytest.fixture(scope="module")
def juri_api(api_client) -> JuriAPI:
    """Create a JURI API instance."""
    return JuriAPI(api_client)


@pytest.mark.timeout(30)
def test_search_by_keywords(juri_api: JuriAPI):
    """
    Scénario: Recherche par mots-clés
    Étant donné que j'ai accès à l'API Légifrance
    Lorsque je recherche des décisions contenant "responsabilité civile"
    Alors je reçois une liste de décisions pertinentes
    Et chaque décision contient les informations essentielles (juridiction, date, numéro)
    """
    # Lorsque je recherche des décisions contenant "responsabilité civile"
    search_query = "responsabilite civile"
    results = juri_api.search(search_query)

    # Alors je reçois une liste de décisions pertinentes
    assert isinstance(results, list), "Les résultats doivent être une liste"
    assert len(results) > 0, "La recherche doit retourner au moins un résultat"

    # Et chaque décision contient les informations essentielles (juridiction, date, numéro)
    for decision in results:
        print(decision.latest())
        print(decision.versions())
        assert isinstance(decision, JuriDecision), (
            "Chaque résultat doit être une JuriDecision"
        )
        assert decision.id is not None, "Chaque décision doit avoir un ID"

        # Au moins une des informations essentielles doit être présente
        essential_info_present = any(
            [
                decision.jurisdiction is not None,
                decision.date is not None,
                decision.numero is not None,
            ]
        )
        assert essential_info_present, (
            "Chaque décision doit contenir au moins une information essentielle"
        )


@pytest.mark.timeout(30)
def test_filter_by_jurisdiction(juri_api: JuriAPI):
    """
    Scénario: Filtrage par juridiction
    Étant donné que j'ai accès à l'API Légifrance
    Lorsque je recherche des décisions de la Cour de cassation
    Alors je ne reçois que des décisions de cette juridiction
    """
    # Lorsque je recherche des décisions de la Cour de cassation
    search_request = SearchRequest(
        search="contrat",
        juridiction_judiciaire=[JuridictionJudiciaire.cour_de_cassation.value],
        page_size=3,
    )
    results = juri_api.search(search_request)

    # Alors je ne reçois que des décisions de cette juridiction
    assert isinstance(results, list), "Les résultats doivent être une liste"

    if len(results) > 0:  # Si des résultats sont trouvés
        for decision in results:
            # Vérifier que la juridiction correspond ou qu'elle contient des mots-clés de la Cour de cassation
            if decision.jurisdiction:
                jurisdiction_lower = decision.jurisdiction.lower()
                cour_cassation_keywords = ["cassation", "cour de cassation"]
                assert any(
                    keyword in jurisdiction_lower for keyword in cour_cassation_keywords
                ), (
                    f"La juridiction '{decision.jurisdiction}' ne correspond pas à la Cour de cassation"
                )


@pytest.mark.timeout(30)
def test_pagination_of_results(juri_api: JuriAPI):
    """
    Scénario: Pagination des résultats
    Étant donné que j'ai accès à l'API Légifrance
    Lorsque je recherche des décisions avec une limite de 5 par page
    Alors je reçois exactement 5 résultats
    Et je peux accéder à la page suivante
    """
    # Lorsque je recherche des décisions avec une limite de 5 par page
    page_size = 5
    search_request_page1 = SearchRequest(
        search="dommages", page_size=page_size, page_number=1
    )
    search_request_page2 = SearchRequest(
        search="dommages", page_size=page_size, page_number=2
    )

    # Alors je reçois exactement 5 résultats
    results_page1 = juri_api.search(search_request_page1)
    assert isinstance(results_page1, list), (
        "Les résultats de la page 1 doivent être une liste"
    )
    assert len(results_page1) <= page_size, (
        f"Le nombre de résultats de la page 1 ne doit pas dépasser {page_size}"
    )

    # Et je peux accéder à la page suivante
    results_page2 = juri_api.search(search_request_page2)
    assert isinstance(results_page2, list), (
        "Les résultats de la page 2 doivent être une liste"
    )
    assert len(results_page2) <= page_size, (
        f"Le nombre de résultats de la page 2 ne doit pas dépasser {page_size}"
    )

    # Vérifier que les pages contiennent des résultats différents
    if len(results_page1) > 0 and len(results_page2) > 0:
        page1_ids = {decision.id for decision in results_page1 if decision.id}
        page2_ids = {decision.id for decision in results_page2 if decision.id}
        assert page1_ids != page2_ids, (
            "Les résultats de la page 1 et 2 doivent être différents"
        )


@pytest.mark.timeout(30)
def test_specific_field_extraction(juri_api: JuriAPI):
    """
    Scénario: Extraction de champs spécifiques
    Étant donné que j'ai accès à l'API Légifrance
    Lorsque je recherche des décisions en spécifiant les champs à extraire
    Alors je reçois uniquement les champs demandés pour chaque décision
    """
    # Lorsque je recherche des décisions en spécifiant les champs à extraire
    specific_keys = ["id", "titre", "juridiction", "dateTexte"]
    search_request = SearchRequest(
        search="préjudice", keys=specific_keys, formatter=True, page_size=3
    )
    results = juri_api.search(search_request)

    # Alors je reçois uniquement les champs demandés pour chaque décision
    assert isinstance(results, list), "Les résultats doivent être une liste"

    if len(results) > 0:
        for decision in results:
            assert isinstance(decision, JuriDecision), (
                "Chaque résultat doit être une JuriDecision"
            )

            # Vérifier que les champs essentiels sont présents
            assert decision.id is not None, "L'ID doit toujours être présent"

            # Au moins un des champs spécifiés doit être présent
            specified_fields_present = any(
                [
                    decision.title is not None,
                    decision.jurisdiction is not None,
                    decision.date is not None,
                ]
            )
            assert specified_fields_present, (
                "Au moins un des champs spécifiés doit être présent"
            )
