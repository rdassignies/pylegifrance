# Explications

PyLegifrance est une bibliothèque Python qui simplifie l'accès aux données juridiques françaises disponibles via l'API Legifrance.

## Structure

- `client.py` : Gestion de l'authentification et des appels API
- `models` : Définition des structures de données avec Pydantic
- `pipeline` : Traitement des requêtes et réponses

## Fonctionnalités

- `recherche_CODE` : Recherche dans les codes français
- `recherche_LODA` : Recherche dans les lois, ordonnances, décrets et arrêtés
- `recherche_JURI` : Recherche dans la jurisprudence (en développement)

## Roadmap

- [ ] Ajout des fonctions recherche_JURI, rechercher_CETAT, KALI,...
- [ ] Implémentation des fonctions suggest, consult et list
- [ ] Ajout de fonctions de formattage avancé en sortie
- [ ] Ajout des paramètres de tri des résultats 

Pour une liste complète des fonctionnalités proposées et des problèmes connus, consultez les [issues ouvertes](https://github.com/pylegifrance/pylegifrance/issues).
