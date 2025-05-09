# Guide de Contribution

Merci de votre intérêt pour ce projet ! Ce guide a pour but de garantir une collaboration efficace et cohérente.

Ce projet utilise :
- [**Python**](https://www.python.org/) comme langage principal
- [**UV**](https://github.com/astral-sh/uv) comme gestionnaire de paquets
- [**pre-commit**](https://pre-commit.com/) pour l'assurance qualité du code
- Le [**développement piloté par le comportement (BDD)**](https://behave.readthedocs.io/en/latest/) avec la syntaxe [**Cucumber**](https://cucumber.io/)

## Étapes pour contribuer

### 1. Ouvrir ou identifier une *issue*

- Vérifiez qu’une [issue](../../issues) existe pour le problème ou la fonctionnalité.
- Sinon, ouvrez une nouvelle issue en suivant le modèle proposé.

### 2. Créer une branche depuis GitHub

- Depuis l’issue, cliquez sur **"Create branch"** dans l’interface GitHub.
- Cela crée automatiquement une branche nommée selon l’issue et la lie à celle-ci.

> ⚠️ N'utilisez **pas** `main` ou `develop` pour vos modifications.

## Préparer votre environnement

1. **Installer les dépendances avec UV**

Assurez-vous que [UV](https://github.com/astral-sh/uv) est installé, puis synchronisez l'environnement :

```

uv sync --all-extras

```

Cette commande installe toutes les dépendances de base et optionnelles.

2. **Configurer les hooks pre-commit**

```

uv run pre-commit install
uv run pre-commit run --all-files

```

## Ouvrir une Pull Request

1. Poussez votre branche sur GitHub :

```

git push origin <nom-de-branche>

```

2. Créez une [Pull Request](https://docs.github.com/fr/pull-requests)

---

## Bonnes pratiques

- Une PR = une fonctionnalité ou un correctif
