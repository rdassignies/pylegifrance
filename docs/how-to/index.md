# Guides pratiques

## Installation

```bash
uv pip install git+https://github.com/pylegifrance/pylegifrance
```

## Obtenir un compte PISTE

1. Créez un compte sur [https://piste.gouv.fr](https://piste.gouv.fr)
2. Souscrivez à l'API Legifrance
3. Récupérez vos identifiants (client_id et client_secret)

Voir le [guide officiel](https://piste.gouv.fr/en/help-center/guide) pour plus de détails.

## Configuration des clés API

Variables d'environnement ou fichier `.env` :
```
LEGIFRANCE_CLIENT_ID=votre_client_id
LEGIFRANCE_CLIENT_SECRET=votre_client_secret
```

Ou configuration manuelle :
```python
from pylegifrance import LegiHandler
client = LegiHandler()
client.set_api_keys(legifrance_api_key="votre_client_id", legifrance_api_secret="votre_client_secret")
```

## Exemples d'utilisation

### Recherche dans les codes

```python
from pylegifrance import recherche_code

# Article spécifique
recherche_code(code_name="Code civil", search="7")

# Recherche par terme
recherche_code(code_name="Code civil", search="sûreté", champ="ARTICLE")

# Code entier
recherche_code(code_name="Code civil")
```

### Recherche dans les textes législatifs
```python
from pylegifrance import recherche_LODA

# Texte par numéro
recherche_LODA(text_id="78-17")

# Article spécifique
recherche_LODA(text_id="78-17", search="9")

# Filtrage par date et type
recherche_LODA(nature=["DECRET"], date_signature=["2023-01-01", "2023-01-31"])
```

### Options supplémentaires
```python
# Formatage des résultats
recherche_CODE(code_name="Code civil", search="7", formatter=True)

# Pagination
recherche_LODA(search="environnement", page_number=2, page_size=20)
```
