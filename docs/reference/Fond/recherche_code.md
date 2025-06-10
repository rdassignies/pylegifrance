# recherche_code

```python
def recherche_code(
    code_name: str,
    search: str = None,
    champ: str = "NUM_ARTICLE",
    type_recherche: str = "EXACTE",
    fond: str = "CODE_DATE",
    formatter: bool = False,
    page_number: int = 1,
    page_size: int = 10,
    *args,
) -> dict
```

Fonction qui permet de rechercher des articles dans les codes français en utilisant l'API Legifrance.

## Description

Cette fonction permet d'effectuer des recherches dans les codes français (Code civil, Code pénal, etc.) en spécifiant différents critères de recherche. Elle utilise l'API Legifrance pour récupérer les résultats et peut les formater pour une meilleure lisibilité.

## Paramètres

- `code_name` (str): Nom du code dans lequel effectuer la recherche (ex: "LEGITEXT000006070721" pour le Code civil).
- `search` (str, optionnel): Terme de recherche. Si None, aucun terme de recherche n'est utilisé.
- `champ` (str, optionnel): Champ dans lequel effectuer la recherche. Valeurs possibles:
  - "NUM_ARTICLE": Numéro d'article (défaut)
  - "TITLE": Titre de l'article
  - "TEXT": Texte de l'article
  - "ALL": Tous les champs
- `type_recherche` (str, optionnel): Type de recherche à effectuer. Valeurs possibles:
  - "EXACTE": Recherche exacte (défaut)
  - "APPROXIMATIVE": Recherche approximative
- `fond` (str, optionnel): Fond documentaire à utiliser. Valeurs possibles:
  - "CODE_DATE": Code à la date du jour (défaut)
  - "CODE_ETAT": Code dans son état actuel
- `formatter` (bool, optionnel): Si True, formate les résultats pour une meilleure lisibilité.
- `page_number` (int, optionnel): Numéro de page des résultats (défaut: 1).
- `page_size` (int, optionnel): Nombre de résultats par page (défaut: 10).
- `*args`: Arguments supplémentaires à passer à l'API.

## Retourne

- `dict`: Dictionnaire contenant les résultats de la recherche. Structure:
  ```python
  {
      "results": [
          {
              "id": "LEGIARTI000006419305",
              "title": "Article 1",
              "text": "Contenu de l'article...",
              "num": "1",
              "etat": "VIGUEUR",
              "date_version": "2023-01-01",
              "liens": [...]
          },
          # Autres résultats...
      ],
      "pagination": {
          "page": 1,
          "pageSize": 10,
          "total": 42
      }
  }
  ```

## Exceptions

- `ValueError`: Si les paramètres fournis sont invalides.
- `Exception`: Si l'appel à l'API échoue.

## Exemples

### Recherche d'un article par numéro dans le Code civil

```python
from pylegifrance import recherche_code

# Recherche de l'article 1382 du Code civil
resultats = recherche_code(
    code_name="LEGITEXT000006070721",  # Code civil
    search="1382",
    champ="NUM_ARTICLE",
    formatter=True
)

# Affichage du premier résultat
if resultats["results"]:
    article = resultats["results"][0]
    print(f"Article {article['num']}: {article['title']}")
    print(article['text'])
```

### Recherche par mot-clé dans le texte des articles

```python
# Recherche des articles contenant le mot "responsabilité" dans le Code civil
resultats = recherche_code(
    code_name="LEGITEXT000006070721",
    search="responsabilité",
    champ="TEXT",
    type_recherche="APPROXIMATIVE",
    page_size=20
)

# Affichage du nombre de résultats
print(f"Nombre de résultats: {resultats['pagination']['total']}")
```

## Codes fréquemment utilisés

- Code civil: "LEGITEXT000006070721"
- Code pénal: "LEGITEXT000006070719"
- Code de commerce: "LEGITEXT000005634379"
- Code du travail: "LEGITEXT000006072050"
- Code de procédure civile: "LEGITEXT000006070716"
- Code de procédure pénale: "LEGITEXT000006071154"
