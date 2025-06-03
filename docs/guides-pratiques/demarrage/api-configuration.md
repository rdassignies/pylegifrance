# Configuration des clés API

Deux options pour configurer vos identifiants API :

## 1. Variables d'environnement (ou `.env`)

```bash
LEGIFRANCE_CLIENT_ID=votre_client_id
LEGIFRANCE_CLIENT_SECRET=votre_client_secret
```

Le client s'initialise automatiquement :

```python
from pylegifrance import LegifranceClient

client = LegifranceClient()
```

## 2. Configuration manuelle

Utile si vos clés proviennent d'un vault ou d'un système externe :

```python
from pylegifrance import LegifranceClient
from pylegifrance.config import ApiConfig

client = LegifranceClient(ApiConfig(client_id="...", client_secret="..."))
```

⚠️ Les identifiants sont obligatoires dès l'instanciation, sinon une erreur est levée.