# Documentation PyLegifrance

Ce répertoire contient la documentation du projet PyLegifrance, générée avec MkDocs et le thème Material for MkDocs.

## Prérequis

- Python 3.12+

## Installation et exécution

Assurez-vous d'avoir Python 3.8 ou supérieur installé, puis :

```bash
# Installation des dépendances de documentation
uv pip install --extra docs -e .

# Lancement du serveur de documentation local
uv run --extra docs mkdocs serve
```

Le serveur sera accessible à l'adresse [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Structure de la documentation

La documentation suit l'approche [Diátaxis](https://diataxis.fr/) avec quatre sections principales :

- **Tutoriels** : Guides pas à pas pour les débutants
- **Guides Pratiques** : Instructions pour résoudre des problèmes spécifiques
- **Référence** : Documentation technique détaillée de l'API
- **Explication** : Discussions approfondies sur les concepts
