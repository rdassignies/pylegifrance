# Exécution des Tests pour PyLegifrance

Ce document explique comment exécuter les tests pour le paquet PyLegifrance.

## Prérequis

Avant d’exécuter les tests, assurez-vous d’avoir :

1. Installé le paquet et ses dépendances :

```bash
  uv sync
```

2. Configuré les variables d’environnement pour l’API Legifrance (pour les tests API).

### Variables d’Environnement

Copiez le fichier `.env.example` situé à la racine du projet vers un nouveau fichier nommé `.env`, puis saisissez vos identifiants API Legifrance :

```
# Legifrance API configuration
LEGIFRANCE_CLIENT_ID=your_client_id
LEGIFRANCE_CLIENT_SECRET=your_client_secret
```

> 💡 Alternativement, vous pouvez passer les identifiants directement via `ApiConfig` dans votre code de test :

```python
from pylegifrance import LegifranceClient
from pylegifrance.config import ApiConfig

client = LegifranceClient(ApiConfig(client_id="your_client_id", client_secret="your_client_secret"))
```

Ces identifiants sont nécessaires pour que les tests API fonctionnent correctement.

## Exécution des Tests

Pour exécuter tous les tests :

```bash
  uv run pytest
```

## Approche de Test

Ce projet suit l'approche de [Behaviour-Driven Development (BDD)](https://behave.readthedocs.io/en/latest/) en utilisant le framework [Cucumber](https://cucumber.io/).

## Documentation Officielle Pytest

Pour plus d’informations sur l’utilisation de pytest, consultez la documentation officielle :  
👉 [pytest Documentation](https://docs.pytest.org/)
