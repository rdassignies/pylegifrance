# Recherche dans les codes

Pour la liste des codes disponibles : [https://www.legifrance.gouv.fr/liste/code?etatTexte=VIGUEUR](https://www.legifrance.gouv.fr/liste/code?etatTexte=VIGUEUR)

```python
from pylegifrance import recherche_code

# Obtenir l'article 7 du Code civil
recherche_code(code_name="Code civil", search="7")

# Obtenir l'article 7 du Code civil en ne sélectionnant que certains champs spécifiques
recherche_code(code_name="Code civil", search="7", formatter=True)

# Obtenir l'intégralité du Code civil
recherche_code(code_name="Code civil")

# Rechercher le mot "sûreté" dans les articles du Code civil
recherche_code(code_name="Code civil", search="sûreté", champ="ARTICLE")
```

La fonction recherche_code permet la recherche dans le fond CODE (CODE_DATE, CODE_ETAT) d'un article par son numéro, d'un terme de recherche ou d'un code dans son intégralité.

Cette fonction ne récupère que les codes en vigueur à la date actuelle. 
Par défaut, la facette "DATE_VERSION" est définie sur la date du jour, quel que soit le fond cible (CODE_DATE ou CODE_ETAT).

**! Attention** : Il est de la responsabilité exclusive de l'utilisateur de vérifier que les informations renvoyées par l'API sont pertinentes et à jour.

# Options supplémentaires de recherche

```python
# Formatage des résultats
recherche_code(code_name="Code civil", search="7", formatter=True)
```
