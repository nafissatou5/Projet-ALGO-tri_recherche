## Module Python : Tri et Recherche dans une Table 2D

📚 Projet Analyse d’Algorithmes

Ce projet a été réalisé dans le cadre du module Analyse d’Algorithmes.

L’objectif est de concevoir un module Python réutilisable permettant
d’effectuer différentes opérations de tri et de recherche
dans une table à deux dimensions (liste de listes).

Le module est conçu pour être importé dans d'autres programmes Python
et utilisé comme une bibliothèque d’algorithmes.

---

## Objectifs du projet

- Implémenter plusieurs algorithmes classiques de tri.
- Implémenter différents algorithmes de recherche.
- Manipuler une structure de données 2D.
- Comprendre et analyser les complexités algorithmiques.
- Produire un module Python bien documenté et réutilisable.

---

## Fonctionnalités

Algorithmes de tri

- Tri à bulle (Bubble Sort)
- Tri rapide (Quick Sort)
- Tri par sélection (Selection Sort)
- Tri par insertion (Insertion Sort)
- Tri par fusion (Merge Sort)

Chaque tri peut être appliqué :

- sur une colonne spécifique
- en ordre croissant ou décroissant
- sans modifier la table originale

---

Algorithmes de recherche

- Recherche linéaire
- Recherche binaire
- Recherche par dichotomie (version récursive)

---

## Structure du projet
tri-recherche-2d/ │ ├── tri_recherche_2d.py → Module principal ├── test_module.py → Exemple d'utilisation du module ├── rapport.pdf → Rapport académique du projet ├── README.md → Documentation du projet └── .gitignore

## Utilisation du Module
1️. Importer le module
import tri_recherche_2d as t2d
2️. Générer une table aléatoire
table = t2d.generer_table_aleatoire()
3️. Trier une table
table_triee = t2d.tri_rapide(table, col=0)
4️. Effectuer une recherche
index = t2d.recherche_binaire(table_triee, col=0, valeur=50)
5️. Afficher une table
t2d.afficher_table(table)

## Concepts Informatiques Étudiés

Analyse d’algorithmes
Structures de données
Programmation modulaire
Récursivité
Complexité temporelle
Manipulation de tableaux multidimensionnels
Bonnes pratiques Python

## Équipe du Projet

Projet réalisé par :

Nafissatou Faye
Anta Diama Kama
Abdoul Wahab Sall
Mareme Tine
Cherif Younouss Diedhiou

Licence 3 Genie Logiciel et Systeme d'Information
École Supérieure Polytechnique (ESP)
Université Cheikh Anta Diop de Dakar
