# Explications

PyLegifrance est une bibliothèque Python qui simplifie l'accès aux données juridiques françaises disponibles via l'API Legifrance.

## Structure

- `client.api` : Gestion de l'authentification et des appels API
- `models` : Définition des structures de données avec Pydantic
- `pipeline` : Traitement des requêtes et réponses

## Fonctionnalités

- `recherche_CODE` : Recherche dans les codes français
- `recherche_LODA` : Recherche dans les lois, ordonnances, décrets et arrêtés
- `recherche_JURI` : Recherche dans la jurisprudence (en développement)
