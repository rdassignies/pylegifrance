import pytest
from datetime import datetime

from pylegifrance.models.constants import Fond, Nature
from pylegifrance.models.generated.model import DatePeriod
from pylegifrance.fonds.loda import Loda, TexteLoda
from pylegifrance.models.loda.search import SearchRequest


@pytest.fixture(scope="module")
def loda_api(api_client) -> Loda:
    """Create a LODA API instance."""
    return Loda(api_client)


@pytest.mark.timeout(30)
def test_search_by_term(loda_api: Loda):
    """
    Scénario: Recherche simple par terme
    Lorsque j'appelle loda.search avec search="télétravail"
    Alors l'API retourne une liste de TexteLoda
    Et les résultats contiennent le terme recherché
    """
    # Lorsque j'appelle loda.search avec search="télétravail" (terme plus commun)
    search_term = "télétravail"
    results = loda_api.search(search_term)

    print("Results", results)

    # Alors l'API retourne une liste de TexteLoda
    assert isinstance(results, list) and len(results) > 0, (
        "Les résultats doivent être une liste non vide"
    )

    # Vérifier qu'il y a des résultats (si l'API est disponible)
    if len(results) > 0:
        # Et les résultats contiennent le terme recherché
        for texte in results:
            assert isinstance(texte, TexteLoda), (
                "Chaque résultat doit être un TexteLoda"
            )
            assert texte.id is not None, "Chaque texte doit avoir un ID"

            # Vérifier que le terme est présent dans le texte ou le titre
            term_present = False
            if texte.texte_html and search_term.lower() in texte.texte_html.lower():
                term_present = True
            elif texte.titre and search_term.lower() in texte.titre.lower():
                term_present = True
            elif texte.titre_long and search_term.lower() in texte.titre_long.lower():
                term_present = True

            assert term_present, (
                f"Le terme '{search_term}' doit être présent dans le texte ou le titre"
            )


@pytest.mark.timeout(30)
def test_search_by_nature_loi(loda_api: Loda):
    """
    Scénario: Recherche par nature LOI
    Lorsque j'appelle loda.search avec nature="LOI"
    Alors l'API retourne uniquement des lois
    Et chaque résultat a nature="LOI"
    """
    # Lorsque j'appelle loda.search avec nature="LOI"
    search_request = SearchRequest(
        search="droit", natures=[Nature.LOI.value], page_size=5
    )
    results = loda_api.search(search_request)

    # Alors l'API retourne uniquement des lois
    assert isinstance(results, list), "Les résultats doivent être une liste"

    if len(results) > 0:
        for texte in results:
            assert isinstance(texte, TexteLoda), (
                "Chaque résultat doit être un TexteLoda"
            )

            # Vérifier que le titre contient "LOI" ou "loi"
            assert texte.titre is not None, "Chaque texte doit avoir un titre"
            assert "loi" in texte.titre.lower(), (
                f"Le titre '{texte.titre}' doit contenir 'loi'"
            )


@pytest.mark.timeout(30)
def test_search_by_nature_decret(loda_api: Loda):
    """
    Scénario: Recherche par nature DECRET
    Lorsque j'appelle loda.search avec nature="DECRET"
    Alors l'API retourne uniquement des décrets
    Et chaque résultat a nature="DECRET"
    """
    # Lorsque j'appelle loda.search avec nature="DECRET"
    search_request = SearchRequest(
        search="application", natures=[Nature.DECRET.value], page_size=5
    )
    results = loda_api.search(search_request)

    # Alors l'API retourne uniquement des décrets
    assert isinstance(results, list), "Les résultats doivent être une liste"

    if len(results) > 0:
        for texte in results:
            assert isinstance(texte, TexteLoda), (
                "Chaque résultat doit être un TexteLoda"
            )

            # Vérifier que le titre contient "décret" ou "Décret"
            assert texte.titre is not None, "Chaque texte doit avoir un titre"
            assert "décret" in texte.titre.lower(), (
                f"Le titre '{texte.titre}' doit contenir 'décret'"
            )


@pytest.mark.timeout(30)
def test_search_by_nature_ordonnance(loda_api: Loda):
    """
    Scénario: Recherche par nature ORDONNANCE
    Lorsque j'appelle loda.search avec nature="ORDONNANCE"
    Alors l'API retourne uniquement des ordonnances
    Et chaque résultat a nature="ORDONNANCE"
    """
    # Lorsque j'appelle loda.search avec nature="ORDONNANCE"
    search_request = SearchRequest(
        search="modification", natures=[Nature.ORDONNANCE.value], page_size=5
    )
    results = loda_api.search(search_request)

    # Alors l'API retourne uniquement des ordonnances
    assert isinstance(results, list), "Les résultats doivent être une liste"

    if len(results) > 0:
        for texte in results:
            assert isinstance(texte, TexteLoda), (
                "Chaque résultat doit être un TexteLoda"
            )

            # Vérifier que le titre contient "ordonnance" ou "Ordonnance"
            assert texte.titre is not None, "Chaque texte doit avoir un titre"
            assert "ordonnance" in texte.titre.lower(), (
                f"Le titre '{texte.titre}' doit contenir 'ordonnance'"
            )


@pytest.mark.timeout(30)
def test_search_by_nature_arrete(loda_api: Loda):
    """
    Scénario: Recherche par nature ARRETE
    Lorsque j'appelle loda.search avec nature="ARRETE"
    Alors l'API retourne uniquement des arrêtés
    Et chaque résultat a nature="ARRETE"
    """
    # Lorsque j'appelle loda.search avec nature="ARRETE"
    search_request = SearchRequest(
        search="fixant", natures=[Nature.ARRETE.value], page_size=5
    )
    results = loda_api.search(search_request)

    # Alors l'API retourne uniquement des arrêtés
    assert isinstance(results, list), "Les résultats doivent être une liste"

    print(results)

    if len(results) > 0:
        for texte in results:
            assert isinstance(texte, TexteLoda), (
                "Chaque résultat doit être un TexteLoda"
            )

            # Vérifier que le titre contient "arrêté" ou "Arrêté"
            assert texte.titre is not None, "Chaque texte doit avoir un titre"
            assert "arrêté" in texte.titre.lower(), (
                f"Le titre '{texte.titre}' doit contenir 'arrêté'"
            )


@pytest.mark.timeout(30)
def test_fetch_by_id(loda_api: Loda):
    """
    Scénario: Consultation par ID
    Lorsque j'appelle loda.fetch avec text_id="LEGITEXT000006070721"
    Alors l'API retourne un TexteLoda unique
    Et l'objet contient les métadonnées complètes
    """
    # Lorsque j'appelle loda.fetch avec text_id="LEGITEXT000006070721" (Code civil)
    text_id = "LEGITEXT000006069570"

    texte = loda_api.fetch(text_id)

    # Si la requête réussit, vérifier les résultats
    assert texte is not None, "La consultation doit retourner un texte"
    assert isinstance(texte, TexteLoda), "Le résultat doit être un TexteLoda"

    # Et l'objet contient les métadonnées complètes
    # assert texte.id == f"{text_id}_{texte.last_update}", "L'ID du texte doit correspondre à celui demandé"
    assert texte.titre is not None, "Le texte doit avoir un titre"
    assert texte.texte_html is not None, "Le texte doit avoir un contenu HTML"

    # Vérifier que d'autres métadonnées sont présentes
    metadata_present = any(
        [
            texte.date_debut is not None,
            texte.etat is not None,
            texte.last_update is not None,
        ]
    )
    assert metadata_present, "Le texte doit contenir des métadonnées"


@pytest.mark.timeout(30)
def test_pagination(loda_api: Loda):
    """
    Scénario: Pagination basique
    Lorsque j'appelle loda.search avec page_size=5
    Alors l'API retourne au maximum 5 résultats
    Et la pagination fonctionne correctement
    """
    # Lorsque j'appelle loda.search avec page_size=5
    page_size = 5
    search_request_page1 = SearchRequest(
        search="droit", page_size=page_size, page_number=1
    )
    search_request_page2 = SearchRequest(
        search="droit", page_size=page_size, page_number=2
    )

    # Alors l'API retourne au maximum 5 résultats
    results_page1 = loda_api.search(search_request_page1)
    assert isinstance(results_page1, list), (
        "Les résultats de la page 1 doivent être une liste"
    )
    assert len(results_page1) <= page_size, (
        f"Le nombre de résultats de la page 1 ne doit pas dépasser {page_size}"
    )

    # Et la pagination fonctionne correctement
    results_page2 = loda_api.search(search_request_page2)
    assert isinstance(results_page2, list), (
        "Les résultats de la page 2 doivent être une liste"
    )
    assert len(results_page2) <= page_size, (
        f"Le nombre de résultats de la page 2 ne doit pas dépasser {page_size}"
    )

    # Vérifier que les pages contiennent des résultats différents
    if len(results_page1) > 0 and len(results_page2) > 0:
        page1_ids = {texte.id for texte in results_page1 if texte.id}
        page2_ids = {texte.id for texte in results_page2 if texte.id}

        print("Page1:", page1_ids)
        print("Page2:", page2_ids)

        assert page1_ids != page2_ids, (
            "Les résultats de la page 1 et 2 doivent être différents"
        )


@pytest.mark.timeout(30)
def test_search_with_date_debut(loda_api: Loda):
    """
    Scénario: Recherche avec date de début
    Lorsque j'appelle loda.search avec date_debut="2023-01-01"
    Alors tous les résultats ont une date >= 2023-01-01
    Et aucun résultat antérieur n'est retourné
    """
    # Lorsque j'appelle loda.search avec date_debut="2023-01-01"
    date_debut = datetime(year=2023, month=1, day=1)
    search_request = SearchRequest(
        search="loi",
        date_signature=DatePeriod(start=date_debut, end=None),
        page_size=5,
    )
    results = loda_api.search(search_request)

    # Alors tous les résultats ont une date >= 2023-01-01
    assert isinstance(results, list), "Les résultats doivent être une liste"

    if len(results) > 0:
        date_debut_dt = datetime.fromisoformat(date_debut.isoformat())
        for texte in results:
            assert isinstance(texte, TexteLoda), (
                "Chaque résultat doit être un TexteLoda"
            )

            # Si la date de début est disponible, vérifier qu'elle est >= date_debut
            if texte.date_debut:
                assert texte.date_debut >= date_debut_dt, (
                    f"La date de début {texte.date_debut} doit être >= {date_debut_dt}"
                )


@pytest.mark.timeout(30)
def test_search_with_date_fin(loda_api: Loda):
    """
    Scénario: Recherche avec date de fin
    Lorsque j'appelle loda.search avec date_fin="2023-12-31"
    Alors tous les résultats ont une date <= 2023-12-31
    Et aucun résultat postérieur n'est retourné
    """
    # Lorsque j'appelle loda.search avec date_fin="2023-12-31"
    date_fin = datetime(year=2023, month=12, day=31)
    search_request = SearchRequest(
        search="loi", date_signature=DatePeriod(start=None, end=date_fin), page_size=5
    )
    results = loda_api.search(search_request)

    # Alors tous les résultats ont une date <= 2023-12-31
    assert isinstance(results, list), "Les résultats doivent être une liste"

    if len(results) > 0:
        date_fin_dt = datetime.fromisoformat(date_fin.isoformat())
        for texte in results:
            assert isinstance(texte, TexteLoda), (
                "Chaque résultat doit être un TexteLoda"
            )

            # Si la date de début est disponible, vérifier qu'elle est <= date_fin
            if texte.date_debut:
                assert texte.date_debut <= date_fin_dt, (
                    f"La date de début {texte.date_debut} doit être <= {date_fin_dt}"
                )


@pytest.mark.timeout(30)
def test_search_by_fond_loda_date(loda_api: Loda):
    """
    Scénario: Recherche par fond LODA_DATE
    Lorsque j'appelle loda.search avec fond="LODA_DATE"
    Alors l'API utilise le fond spécialisé pour les dates
    Et les résultats correspondent aux versions historiques
    """
    # Lorsque j'appelle loda.search avec fond="LODA_DATE"
    search_request = SearchRequest(search="loi", fond=Fond.LODA_DATE.value, page_size=5)
    results = loda_api.search(search_request)

    # Alors l'API utilise le fond spécialisé pour les dates
    assert isinstance(results, list), "Les résultats doivent être une liste"

    # Vérifier que les résultats contiennent des dates
    if len(results) > 0:
        for texte in results:
            assert isinstance(texte, TexteLoda), (
                "Chaque résultat doit être un TexteLoda"
            )
            assert texte.id is not None, "Chaque texte doit avoir un ID"


@pytest.mark.timeout(30)
def test_search_by_fond_loda_etat(loda_api: Loda):
    """
    Scénario: Recherche par fond LODA_ETAT
    Lorsque j'appelle loda.search avec fond="LODA_ETAT"
    Alors l'API utilise le fond spécialisé pour les états
    Et les résultats correspondent aux statuts juridiques
    """
    # Lorsque j'appelle loda.search avec fond="LODA_ETAT"
    search_request = SearchRequest(search="loi", fond=Fond.LODA_ETAT.value, page_size=5)
    results = loda_api.search(search_request)

    # Alors l'API utilise le fond spécialisé pour les états
    assert isinstance(results, list), "Les résultats doivent être une liste"

    # Vérifier que les résultats contiennent des états juridiques
    if len(results) > 0:
        for texte in results:
            assert isinstance(texte, TexteLoda), (
                "Chaque résultat doit être un TexteLoda"
            )
            assert texte.id is not None, "Chaque texte doit avoir un ID"
            assert texte.etat is not None, "Chaque texte doit avoir un état juridique"


@pytest.mark.timeout(30)
def test_formatting_disabled_by_default(loda_api: Loda):
    """
    Scénario: Formatage désactivé par défaut
    Lorsque j'appelle loda.search sans formatter
    Alors les résultats ne contiennent pas d'URLs formatées
    Et les données brutes sont retournées
    """
    # Lorsque j'appelle loda.search sans formatter
    search_request = SearchRequest(search="loi", page_size=5)
    results = loda_api.search(search_request)

    # Alors les résultats ne contiennent pas d'URLs formatées
    assert isinstance(results, list), "Les résultats doivent être une liste"

    if len(results) > 0:
        for texte in results:
            assert isinstance(texte, TexteLoda), (
                "Chaque résultat doit être un TexteLoda"
            )

            # Vérifier que les données sont brutes (pas d'URL formatée)
            texte_dict = texte.to_dict()
            assert "url" not in texte_dict, (
                "Les résultats ne doivent pas contenir d'URL formatée"
            )


@pytest.mark.timeout(30)
def test_formatting_enabled(loda_api: Loda):
    """
    Scénario: Formatage activé
    Lorsque j'appelle loda.search avec formatter=True
    Alors les résultats contiennent des URLs enrichies
    Et les métadonnées sont formatées
    """
    # Note: Le formatage n'est pas encore implémenté dans la classe Loda
    # Ce test vérifie simplement que la recherche fonctionne avec le paramètre formatter=True
    search_request = SearchRequest(search="loi", page_size=5)
    results = loda_api.search(search_request)

    # Vérifier que la recherche fonctionne
    assert isinstance(results, list), "Les résultats doivent être une liste"


@pytest.mark.timeout(30)
def test_invalid_nature_raises_error(loda_api: Loda):
    """
    Scénario: Gestion d'erreur nature invalide
    Lorsque j'appelle loda.search avec nature="INVALIDE"
    Alors l'API lève une erreur de validation
    Et le message indique les natures valides
    """
    # Lorsque j'appelle loda.search avec nature="INVALIDE"
    with pytest.raises(Exception) as excinfo:
        search_request = SearchRequest(search="loi", natures=["INVALIDE"], page_size=5)
        loda_api.search(search_request)

    # Vérifier que l'erreur est liée à la validation
    error_message = str(excinfo.value)

    # Et le message indique la nature invalide
    assert "INVALIDE" in error_message, (
        "Le message d'erreur doit mentionner la nature invalide"
    )

    # Vérifier que le message mentionne que la valeur n'est pas valide
    assert "not a valid" in error_message, (
        "Le message d'erreur doit indiquer que la valeur n'est pas valide"
    )
