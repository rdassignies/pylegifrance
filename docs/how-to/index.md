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

## Exemples d'utilisation

### Recherche dans les codes

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

### Recherche dans le fond LODA (LOI, ORDONNANCE, DECRET, ARRETE)

```python
from pylegifrance import recherche_LODA

# Obtenir l'article 9 de la loi informatique et libertés
recherche_LODA(text_id="78-17", search="9")

# Obtenir l'article 2 de l'ordonnance 58-1100 
recherche_LODA(text_id='58-1100', search="2", nature=["ORDONNANCE"])

# Obtenir l'intégralité de la loi informatique et libertés
recherche_LODA(text_id="78-17")

# Rechercher le mot "autorité" dans tous les contenus de la loi informatique et libertés
recherche_LODA(text_id="78-17", search="autorité", champ="ALL")

# Rechercher le mot "publique" dans le champ "article" du décret n°2023-823
recherche_LODA(text_id='2023-823', search="publique", nature=["DECRET"], champ="ARTICLE")

# Rechercher le mot "autorité" dans tous les contenus de la loi informatique et libertés en ne sélectionnant que certains champs spécifiques
recherche_LODA(text_id="78-17", search="autorité", champ="ALL", formatter=True)

# Rechercher les arrêtés et les décrets dont la date de signature est entre le 09 août et le 12 août 2023
recherche_LODA(date_signature=["2023-08-09", "2023-08-12"], nature=["DECRET", "ARRETE"])

# Recherche l'expression complète "signature électronique" dans le champ ARTICLE des décrets signés entre le 09 août 2017 et le 12 août 2018 
recherche_LODA(search="signature électronique", champ='ARTICLE', type_recherche="TOUS_LES_MOTS_DANS_UN_CHAMP", nature=['DECRET'], date_signature=["2017-08-09", "2018-08-12"])
```

La fonction recherche LODA permet la recherche dans le fond LODA (LODA_DATE, LODA_ETAT) d'un texte par son numéro, d'un article dans un texte spécifique, ou d'un terme de recherche dans les champs d'un texte.
Il est possible de sélectionner le type de textes en modifiant la liste "nature" qui est par défaut ["LOI", "ORDONNANCE", "DECRET", "ARRETE"]. 

Cette fonction ne récupère que les textes en vigueur à la date actuelle. Par défaut, la facette "DATE_VERSION" est définie sur la date du jour, et les facettes "TEXT_LEGAL_STATUS" et "ARTICLE_LEGAL_STATUTS" sont définies sur "VIGEUR", quel que soit le fond cible (LODA_DATE ou LODA_ETAT).

**! Attention** : Il est de la responsabilité exclusive de l'utilisateur de vérifier que les informations renvoyées par l'API sont pertinentes et à jour.

### Options supplémentaires

```python
# Formatage des résultats
recherche_code(code_name="Code civil", search="7", formatter=True)

# Pagination
recherche_LODA(search="environnement", page_number=2, page_size=20)
```
