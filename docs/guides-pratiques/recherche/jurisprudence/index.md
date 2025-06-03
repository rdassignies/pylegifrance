# Récupération du contenu des décisions de jurisprudence

## Création d'une instance JuriAPI

Utilisez le client pour créer une instance JuriAPI :

```python
from pylegifrance.fonds.juri import JuriAPI

juri_api = JuriAPI(client)
```

## Récupération d'une décision

Vous pouvez récupérer une décision en utilisant son identifiant :

```python
# Récupération d'une décision par son identifiant
decision = juri_api.fetch("JURITEXT000037999394")  # Remplacez par l'identifiant réel de la décision
```

Ou par son ancien identifiant :

```python
# Récupération d'une décision par son ancien identifiant
decision = juri_api.fetch_with_ancien_id("07-87362")  # Remplacez par l'ancien identifiant réel
```

## Accès au contenu de la décision

Une fois que vous avez un objet `JuriDecision`, vous pouvez accéder à son contenu en utilisant diverses propriétés :

```python
# Obtenir le contenu textuel de la décision
contenu_texte = decision.text

# Obtenir le contenu formaté en HTML de la décision
contenu_html = decision.text_html

# Obtenir d'autres propriétés
titre = decision.title
titre_long = decision.long_title
formation = decision.formation
numero = decision.numero
juridiction = decision.jurisdiction
solution = decision.solution
date = decision.date
```

## Recherche de décisions

Si vous ne connaissez pas l'identifiant, vous pouvez rechercher des décisions :

```python
from pylegifrance.fonds.juri import SearchRequest
from pylegifrance.models.juri.constants import JuridictionJudiciaire

# Recherche simple par mots-clés
resultats = juri_api.search("responsabilité civile")

# Recherche avancée avec filtres
requete_recherche = SearchRequest(
    search="contrat",
    juridiction_judiciaire=[JuridictionJudiciaire.cour_de_cassation.value],
    page_size=5
)
resultats = juri_api.search(requete_recherche)

# Accès au contenu du premier résultat
if resultats:
    premiere_decision = resultats[0]
    contenu = premiere_decision.text
```

## Obtenir différentes versions d'une décision

Vous pouvez également obtenir différentes versions d'une décision :

```python
# Obtenir la version à une date spécifique
version_a_date = decision.at("2022-01-01")

# Obtenir la dernière version
derniere_version = decision.latest()

# Obtenir toutes les versions
toutes_versions = decision.versions()
```

Chacune de ces méthodes renvoie un objet `JuriDecision` (ou une liste d'objets) que vous pouvez utiliser pour accéder au contenu comme indiqué ci-dessus.