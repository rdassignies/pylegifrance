import pytest
from pydantic import ValidationError
from pylegifrance.pipeline.pipeline_factory import recherche_code, recherche_LODA
from pylegifrance.process.processors import GetArticleIdError


@pytest.fixture
def civil_code():
    """Fixture to provide the name of the Civil Code."""
    return "Code civil"


@pytest.fixture
def privacy_law():
    """Fixture to provide the ID of the French Data Protection Act."""
    return "78-17"


def test_search_code_with_article_number(civil_code):
    """
    Test searching for an article by number in a code.
    """
    # Given a valid code name and article number
    code_name = civil_code
    article_number = "7"

    # When searching for the article
    result = recherche_code(code_name=code_name, search=article_number)

    # Then the search should complete without errors
    assert result is not None


def test_search_loda_with_article_number(privacy_law):
    """
    Test searching for an article by number in a law.
    """
    # Given a valid law ID and article number
    text_id = privacy_law
    article_number = "7"

    # When searching for the article
    result = recherche_LODA(text_id=text_id, search=article_number)

    # Then the search should complete without errors
    assert result is not None


def test_search_loda_entire_text(privacy_law):
    """
    Test searching for an entire law text.
    """
    # Given a valid law ID
    text_id = privacy_law

    # When searching for the entire text
    result = recherche_LODA(text_id=text_id)

    # Then the search should complete without errors
    assert result is not None


def test_search_loda_with_nature_filter():
    """
    Test searching for a decree with nature filter.
    """
    # Given a valid decree ID and nature filter
    text_id = "2023-823"
    nature = ["DECRET"]

    # When searching with the nature filter
    result = recherche_LODA(text_id=text_id, nature=nature)

    # Then the search should complete without errors
    assert result is not None


def test_search_loda_with_term_in_all_fields(privacy_law):
    """
    Test searching for a term in all fields of a law.
    """
    # Given a valid law ID, search term, and field
    text_id = privacy_law
    search_term = "poursuite"
    field = "ALL"

    # When searching for the term in all fields
    result = recherche_LODA(text_id=text_id, search=search_term, champ=field)

    # Then the search should complete without errors
    assert result is not None


def test_search_loda_without_text_id_raises_error():
    """
    Test that searching without a text ID raises an error.
    """
    # Given only a search term without a text ID
    search_term = "autorité"

    # When searching without a text ID
    # Then an error should be raised
    with pytest.raises(GetArticleIdError):
        recherche_LODA(search=search_term)


def test_search_loda_with_invalid_field_raises_error(privacy_law):
    """
    Test that searching with an invalid field raises a ValueError.
    """
    # Given a valid law ID but an invalid field
    text_id = privacy_law
    search_term = "poursuite"
    invalid_field = "RAISON SOCIALE"

    # When searching with an invalid field
    # Then a ValueError should be raised because the field is not a valid TypeChamp
    with pytest.raises(ValueError):
        recherche_LODA(text_id=text_id, search=search_term, champ=invalid_field)


def test_search_loda_with_custom_fond(privacy_law):
    """
    Test searching with a custom fond parameter.
    """
    # Given a valid law ID, search term, field, and custom fond
    text_id = privacy_law
    search_term = "poursuite"
    field = "ALL"
    fond = "LOI"

    # When searching with a custom fond
    result = recherche_LODA(text_id=text_id, search=search_term, champ=field, fond=fond)

    # Then the search should complete without errors
    assert result is not None


def test_search_code_for_specific_article(civil_code):
    """
    Test searching for a specific article in a code with formatting.
    """
    # Given a valid code name and article number with formatting enabled
    code_name = civil_code
    article_number = "1200"

    # When searching for the specific article with formatting
    result = recherche_code(code_name=code_name, search=article_number, formatter=True)

    # Then the search should complete without errors
    assert result is not None


def test_search_entire_code(civil_code):
    """
    Test searching for an entire code with formatting.
    """
    # Given a valid code name with formatting enabled
    code_name = civil_code

    # When searching for the entire code with formatting
    result = recherche_code(code_name=code_name, formatter=True)

    # Then the search should complete without errors
    assert result is not None


def test_search_code_with_term_in_article_field(civil_code):
    """
    Test searching for a term in the article field of a code.
    """
    # Given a valid code name, search term, and field with formatting enabled
    code_name = civil_code
    search_term = "mineur"
    field = "ARTICLE"

    # When searching for the term in the article field with formatting
    result = recherche_code(
        code_name=code_name,
        search=search_term,
        champ=field,
        formatter=True,
    )

    # Then the search should complete without errors
    assert result is not None


def test_search_code_with_pagination(civil_code):
    """
    Test searching for a term in a code with pagination.
    """
    # Given a valid code name, search term, field, and page number with formatting enabled
    code_name = civil_code
    search_term = "mineur"
    field = "ARTICLE"
    page_number = 2

    # When searching with pagination
    result = recherche_code(
        code_name=code_name,
        search=search_term,
        champ=field,
        page_number=page_number,
        formatter=True,
    )

    # Then the search should complete without errors
    assert result is not None


def test_search_code_with_invalid_code_raises_error():
    """
    Test that searching with an invalid code name raises a validation error.
    """
    # Given an invalid code name
    invalid_code = "inexistant"
    search_term = "mineur"
    field = "ARTICLE"

    # When searching with an invalid code name
    # Then a validation error should be raised
    with pytest.raises(ValidationError):
        recherche_code(
            code_name=invalid_code,
            search=search_term,
            champ=field,
            formatter=True,
        )


def test_search_code_with_abbreviated_field(civil_code):
    """
    Test searching in a code with an abbreviated field name.
    """
    # Given a valid code name, search term, and abbreviated field with formatting enabled
    code_name = civil_code
    search_term = "7"
    abbreviated_field = "NUM"  # Abbreviated form of NUM_ARTICLE

    # When searching with the abbreviated field
    result = recherche_code(
        code_name=code_name, search=search_term, champ=abbreviated_field, formatter=True
    )

    # Then the search should complete without errors
    assert result is not None


def test_search_code_with_custom_fond(civil_code):
    """
    Test searching in a code with a custom fond parameter.
    """
    # Given a valid code name, search term, field, and custom fond with formatting enabled
    code_name = civil_code
    search_term = "7"
    field = "NUM_ARTICLE"
    fond = "LODA_DATE"

    # When searching with a custom fond
    result = recherche_code(
        code_name=code_name,
        search=search_term,
        champ=field,
        fond=fond,
        formatter=True,
    )

    # Then the search should complete without errors
    assert result is not None


def test_article_url_generation(civil_code):
    """
    Test that the URL is correctly generated for articles with a cid.
    """
    # Given a valid code name and article number with formatting enabled
    code_name = civil_code
    article_number = "7"

    # When searching for the article with formatting
    result = recherche_code(
        code_name=code_name,
        search=article_number,
        formatter=True,
    )

    # Then the result should contain a URL field with the correct format
    assert result is not None

    # Check if the result is a list or a single item
    if isinstance(result, list):
        for article in result:
            if article.get("cid"):
                assert "url" in article
                assert (
                    article["url"]
                    == f"https://www.legifrance.gouv.fr/codes/article_lc/{article['cid']}"
                )
    else:
        if result.get("cid"):
            assert "url" in result
            assert (
                result["url"]
                == f"https://www.legifrance.gouv.fr/codes/article_lc/{result['cid']}"
            )
