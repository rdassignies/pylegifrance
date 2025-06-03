# Fonds

Façades de domaine qui organisent l’API publique de Legifrance par fonds (LEGI, JORF, KALI, JURI, CNIL). Chaque 
sous‑module expose des objets Python de haut niveau (par exemple Code, Article, JORFIssue) et masque la complexité des 
requêtes HTTP ainsi que l’orchestration entre plusieurs points d’extrémité.

## 1. Pourquoi ce dossier existe
• Les routes REST sont regroupées dans des contrôleurs techniques (Consult, Search, List, Chrono, etc.) sans cohérence 
fonctionnelle pour l’utilisateur.

• Les praticiens du droit raisonnent en termes de fonds. Les rassembler sous une même arborescence simplifie la 
découverte et l’autocomplétion.

• Les points d’extrémité exposés par ce module peuvent être renommés ou dépréciés sans rupture de contrat. L’interface 
publique (façades) reste stable et redirige automatiquement vers les implémentations de remplacement.

• Certaines opérations juridiques nécessitent plusieurs appels réseau. Une seule méthode haut niveau (par exemple 
Article.at(date)) les orchestre de manière transparente.