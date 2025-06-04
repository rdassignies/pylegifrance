# Référence API

Cette section contient la documentation technique détaillée de l'API PyLegifrance.


## Fonctions principales

- [recherche_code](fonctions/recherche_code.md) - Recherche dans les codes français
- [recherche_LODA](fonctions/recherche_loda.md) - Recherche dans les lois, ordonnances, décrets et arrêtés

## Classes principales

- [LegifranceClient](classes/legifrance_client.md) - Gère l'authentification et les appels à l'API Legifrance
- [ApiConfig](classes/api_config.md) - Gère la configuration d'accès à l'API (identifiants, URLs, timeouts)
- [JuriAPI](classes/juri_api.md) - Fournit des méthodes pour récupérer et rechercher des décisions de jurisprudence
- [JuriDecision](classes/juri_decision.md) - Représente une décision de jurisprudence avec des méthodes pour accéder à ses propriétés et versions
