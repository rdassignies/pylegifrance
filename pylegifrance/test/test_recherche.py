#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pylegifrance.pipeline.pipeline_factory import recherche_CODE, recherche_LODA
from pylegifrance.process.processors import GetArticleIdError
from pydantic import ValidationError
import pytest


def test_recherche_CODE_valide():
    recherche_CODE(code_name="Code civil", search="7")


def test_recherche_LODA_1article():
    recherche_LODA(text_id="78-17", search="7")


def test_recherche_LODA_1text():
    recherche_LODA(text_id="78-17")


def test_recherche_LODA_1decret():
    recherche_LODA(text_id="2023-823", nature=["DECRET"])


def test_recherche_LODA_term():
    recherche_LODA(text_id="78-17", search="poursuite", champ="ALL")


def test_recherche_LODA_empty_text():
    with pytest.raises(GetArticleIdError):
        recherche_LODA(search="autorité")


def test_recherche_LODA_wrong_field():
    with pytest.raises(ValidationError):
        recherche_LODA(text_id="78-17", search="poursuite", champ="RAISON SOCIALE")


def test_recherche_LODA_wrong_fond():
    recherche_LODA(text_id="78-17", search="poursuite", champ="ALL", fond="LOI")


def test_recherche_CODE_1article():
    recherche_CODE(code_name="Code civil", search="1200", formatter=True)


def test_recherche_CODE_all():
    recherche_CODE(code_name="Code civil", formatter=True)


def test_recherche_CODE_term():
    recherche_CODE(
        code_name="Code civil",
        search="mineur",
        champ="ARTICLE",
        formatter=True,
    )


def test_recherche_CODE_term_page2():
    recherche_CODE(
        code_name="Code civil",
        search="mineur",
        champ="ARTICLE",
        page_number=2,
        formatter=True,
    )


def test_recherche_CODE_wrong_code():
    with pytest.raises(ValidationError):
        recherche_CODE(
            code_name="inexistant",
            search="mineur",
            champ="ARTICLE",
            formatter=True,
        )


def test_recherche_CODE_wrong_field():
    recherche_CODE(code_name="Code civil", search="7", champ="NUM", formatter=True)


def test_recherche_CODE_wrong_fond():
    recherche_CODE(
        code_name="Code civil",
        search="7",
        champ="NUM_ARTICLE",
        fond="LODA_DATE",
        formatter=True,
    )
