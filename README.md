<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
-->

<br />
  <!--<div align="center">
 <a href="https://github.com/pylegifrance/pylegifrance">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

<!-- <h3 align="center">pylegifrance</h3>

  <p align="center">
    project_description
    <br />
    <a href="https://github.com/pylegifrance/pylegifrance/docs"><strong>Documentation  »</strong></a>
    <br />
    <br />
    <a href="https://github.com/pylegifrance/pylegifrance">View Demo</a>
    ·
    <a href="https://github.com/pylegifrance/pylegifrance/issues">Report Bug</a>
    ·
    <a href="https://github.com/pylegifrance/pylegifrance/issues">Request Feature</a>
  </p>
</div> -->
<!-- TABLE OF CONTENTS 

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

-->

<!-- ABOUT THE PROJECT -->
# PyLegifrance



### Built With

[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

https://dassignies.law

Librairie python qui simplifie l'interrogation des contenus de legifrance en créant des fonctions pythons prêtes à l'emploi pour la recherche ou la consultation de textes légaux et réglementaires.  
Elle repose sur l'utilisation de pydantic pour gérer les structures de données d'interrogation et de réponse de l'API legifrance. A terme l'intégralité des fonctions de l'API legifrance seront disponibles sous forme de fonctions python. 

Si vous souhaitez accéder directement à une API simplifiée, c'est par ici : [https://lab.dassignies.law](https://lab.dassignies.law/api/docs) 

Pour un serveur MCP Legifrance, c'est par ici : [https://github.com/rdassignies/mcp-server-legifrance](https://github.com/rdassignies/mcp-server-legifrance)


<!-- GETTING STARTED -->

## Démarrage

Pour installer la librairie : `uv pip install git+https://github.com/pylegifrance/pylegifrance `

Un package depuis PyPi sera accessible ultérieurement. 

### Pré requis

Pour obtenir votre accès à l'API legifrance (clé API et secret), vous devez créer un compte sur le portail PISTE : https://piste.gouv.fr

Pour des instructions détaillées sur la création d'un compte et l'obtention des clés API, consultez le [guide officiel du portail PISTE](https://piste.gouv.fr/en/help-center/guide) ou la [documentation complète](https://pylegifrance.github.io/pylegifrance/how-to/#comment-obtenir-un-compte-sur-le-portail-piste).

### Installation

Vous devez stocker les clés dans des variables d'environnement manuellement ou en utilisant python-dotenv (par exemple): 
: 
  ```py
  export LEGIFRANCE_CLIENT_ID="..."
  export LEGIFRANCE_CLIENT_SECRET="..."
  ```
sinon vous pouvez initialiser le client manuellement
```py
  from pylegifrance import LegiHandler
  client = LegiHandler()
  client.set_api_keys(legifrance_api_key=<votre clé>, legifrance_api_secret=<votre secret>)
```


<!-- USAGE EXAMPLES -->
## Usage

### Recherche dans les codes
Pour la liste des codes disponibles : https://www.legifrance.gouv.fr/liste/code?etatTexte=VIGUEUR

```py
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
La fonction recherche_CODE permet la recherche dans le fond CODE (CODE_DATE, CODE_ETAT) d'un article par son numéro, d'un terme de recherche ou d'un code dans son intégralité.

Cette fonction ne récupère que les codes en vigueur à la date actuelle. 
Par défaut, la facette "DATE_VERSION" est définie sur la date du jour, quel que soit le fond cible (CODE_DATE ou CODE_ETAT).

**! Attention** : Il est de la responsabilité exclusive de l'utilisateur de vérifier que les informations renvoyées par l'API sont pertinentes et à jour.

Certains paramètres comme "sort" ou "typepagination" ou le type de de recherche ne sont pas encore accessibles (roadmap *infra*).

Pour plus de détails, se référer à la documentation de la fonction. 


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Recherche dans le fond LODA (LOI, ORDONNANCE, DECRET, ARRETE)
```py
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

# Rechercher le mot "autorité" dans tous les contenus de la loi informatique et libertés en ne sélectionnant que certains champs spécifiques (formatter=True)
recherche_LODA(text_id="78-17", search="autorité", champ="ALL", formatter=True)

# Rechercher les arrêtés et les décrets dont la date de signature est entre le 09 août et le 12 août 2023 (format YYYY-MM-DD)
recherche_LODA(date_signature=["2023-08-09", "2023-08-12"], nature=["DECRET", "ARRETE"])

# Recherche l'expression complète "signature électronique" dans le champ ARTICLE des décrets signés entre le 09 août 2017 et le 12 août 2018 

recherche_LODA(search="signature électronique", champ='ARTICLE', type_recherche="TOUS_LES_MOTS_DANS_UN_CHAMP", nature=['DECRET'], date_signature=["2017-08-09", "2018-08-12"])

```
La fonction recherche LODA permet la recherche dans le fond LODA (LODA_DATE, LODA_ETAT) d'un texte par son numéro, d'un article dans un texte spécifique, ou d'un terme de recherche dans les champs d'un texte.
Il est possible de sélectionner le type de textes en modifiant la liste "nature" qui est par défaut ["LOI", "ORDONNANCE", "DECRET", "ARRETE"]. 

Cette fonction ne récupère que les textes en vigueur à la date actuelle. Par défaut, la facette "DATE_VERSION" est définie sur la date du jour, et les facettes "TEXT_LEGAL_STATUS" et "ARTICLE_LEGAL_STATUTS" sont définies sur "VIGEUR", quel que soit le fond cible (LODA_DATE ou LODA_ETAT).

**! Attention** : Il est de la responsabilité exclusive de l'utilisateur de vérifier que les informations renvoyées par l'API sont pertinentes et à jour.

Certains paramètres comme "sort" ou "typepagination" ou le type de de recherche ne sont pas encore accessibles (roadmap *infra*).

Pour plus de détails, se référer à la documentation de la fonction. 
<!-- ROADMAP -->
## Roadmap

- [ ] Ajout des fonctions recherche_JURI, rechercher_CETAT, KALI,...
- [ ] Implémentation des fonctions suggest, consult et list
- [ ] Ajout de fonctions de formattage avancé en sortie
- [ ] Ajout des paramètres de tri des résultats 

See the [open issues](https://github.com/pylegifrance/pylegifrance/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Raphael d'Assignies - email: rdassignies AT protonmail.ch

https://dassignies.law

Project Link: [https://github.com/pylegifrance/pylegifrance](https://github.com/pylegifrance/pylegifrance)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/rdassignies/pylegifrance.svg?style=for-the-badge
[contributors-url]: github.com/rdassignies/pylegifrance/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/rdassignies/pylegifrance.svg?style=for-the-badge
[forks-url]: https://github.com/pylegifrance/pylegifrance/network/members
[stars-shield]: https://img.shields.io/github/stars/rdassignies/pylegifrance.svg?style=for-the-badge
[stars-url]: https://github.com/pylegifrance/pylegifrance/stargazers
[issues-shield]: https://img.shields.io/github/issues/rdassignies/pylegifrance.svg?style=for-the-badge
[issues-url]: https://github.com/pylegifrance/pylegifrance/issues
[license-shield]: https://img.shields.io/github/license/rdassignies/pylegifrance.svg?style=for-the-badge
[license-url]: https://github.com/pylegifrance/pylegifrance/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://fr.linkedin.com/in/dassignies
