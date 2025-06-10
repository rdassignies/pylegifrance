# Recherche dans le fond LODA (LOI, ORDONNANCE, DECRET, ARRETE)

La classe `Loda` permet la recherche dans le fond LODA (LODA_DATE, LODA_ETAT) d'un texte par son numéro, d'un article dans un texte spécifique, ou d'un terme de recherche dans les champs d'un texte.
Il est possible de sélectionner le type de textes en modifiant la liste "nature" qui est par défaut ["LOI", "ORDONNANCE", "DECRET", "ARRETE"]. 

Cette API ne récupère que les textes en vigueur à la date actuelle. Par défaut, la facette "DATE_VERSION" est définie sur la date du jour, et les facettes "TEXT_LEGAL_STATUS" et "ARTICLE_LEGAL_STATUTS" sont définies sur "VIGEUR", quel que soit le fond cible (LODA_DATE ou LODA_ETAT).

> **⚠️ Attention** : Il est de la responsabilité exclusive de l'utilisateur de vérifier que les informations renvoyées par l'API sont pertinentes et à jour.

# Options supplémentaires de recherche

```python
# Pagination
resultats = loda.search(SearchRequest(search="environnement", page_number=2, page_size=20))

# Recherche simplifiée avec une chaîne de caractères
resultats = loda.search("environnement")

# Accéder à une version spécifique d'un texte à une date donnée
texte_version = loda.fetch_version_at("78-17", "2022-01-01")

# Récupérer toutes les versions d'un texte
versions = loda.fetch_versions("78-17")
```
