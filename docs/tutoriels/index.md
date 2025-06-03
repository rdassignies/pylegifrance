---
title: Tutoriels
---
# Tutoriels

## Premier pas avec PyLegifrance

### Exemple de base

```python
from pylegifrance import recherche_code

# Rechercher l'article 1382 du Code civil
resultat = recherche_code(code_name="Code civil", search="1382")
print(resultat)
```

## Exemples avancés

### Recherche par mots-clés

```python
from pylegifrance import recherche_LODA

# Rechercher "données personnelles" dans la loi informatique et libertés
resultats = recherche_LODA(
    text_id="78-17",
    search="données personnelles",
    champ="ARTICLE",
    type_recherche="TOUS_LES_MOTS_DANS_UN_CHAMP"
)
```

### Filtrage par date et type

```python
from pylegifrance import recherche_LODA

# Rechercher les décrets sur l'environnement de 2022
resultats = recherche_LODA(
    search="environnement",
    champ="TITLE",
    nature=["DECRET"],
    date_signature=["2022-01-01", "2022-12-31"]
)
```

### Formatage des résultats

```python
# Avec formatage
resultat_formate = recherche_CODE(code_name="Code civil", search="16", formatter=True)
```
