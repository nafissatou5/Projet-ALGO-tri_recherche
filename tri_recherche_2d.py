"""
====================================================================
Module : tri_recherche_2d
====================================================================
Ce module fournit des algorithmes de tri et de recherche pour des
tables à deux dimensions (listes de listes Python).

Convention adoptée :
  - Une table 2D est une liste de lignes : table[i][j]
  - Le tri porte sur une colonne-clé (paramètre `col`).
  - La recherche cherche une valeur dans une colonne donnée.

Utilisation rapide
------------------
    import tri_recherche_2d as t2d

    table = [
        [3, "Charlie", 85],
        [1, "Alice",   92],
        [2, "Bob",     78],
    ]

    # --- Tri ---
    triee = t2d.tri_bulle(table, col=0)
    triee = t2d.tri_rapide(table, col=2)
    triee = t2d.tri_selection(table, col=1)
    triee = t2d.tri_insertion(table, col=0)
    triee = t2d.tri_fusion(table, col=2)

    # --- Recherche ---
    idx = t2d.recherche_lineaire(table, col=1, valeur="Alice")
    idx = t2d.recherche_binaire(table_triee, col=0, valeur=2)
    idx = t2d.recherche_dichotomie(table_triee, col=2, valeur=85)
====================================================================
"""

import copy  # Pour copier la table sans modifier l'originale
import sys
sys.stdout.reconfigure(encoding='utf-8')


# ====================================================================
#  UTILITAIRES INTERNES
# ====================================================================

def _copier(table):
    """
    Retourne une copie profonde de la table afin de ne jamais
    modifier la table passée en argument par l'utilisateur.
    """
    return copy.deepcopy(table)


def _valider_table(table, col):
    """
    Vérifie que la table est non vide et que la colonne `col` existe.
    Lève une ValueError si la validation échoue.
    """
    if not table or not isinstance(table, list):
        raise ValueError("La table doit être une liste non vide.")
    if not isinstance(table[0], list):
        raise ValueError("Chaque élément de la table doit être une liste (ligne).")
    nb_cols = len(table[0])
    if not (0 <= col < nb_cols):
        raise ValueError(
            f"Colonne {col} invalide. La table possède {nb_cols} colonne(s) (0 à {nb_cols - 1})."
        )


# ====================================================================
#  ALGORITHMES DE TRI
# ====================================================================

# --------------------------------------------------------------------
# 1. TRI À BULLE (Bubble Sort)
# --------------------------------------------------------------------
def tri_bulle(table, col=0, croissant=True):
    """
    Trie la table selon la colonne `col` par la méthode du tri à bulle.

    Principe :
      On parcourt le tableau plusieurs fois de gauche à droite.
      À chaque passage, on compare deux lignes adjacentes et on les
      échange si elles sont dans le mauvais ordre.
      Après chaque passage, l'élément le plus grand « remonte »
      (comme une bulle) à sa place définitive en fin de tableau.
      On répète jusqu'à ce qu'aucun échange ne soit nécessaire.

    Complexité : O(n²) dans le pire cas, O(n) si déjà trié.

    Paramètres
    ----------
    table    : list[list]  – table 2D source (non modifiée)
    col      : int         – index de la colonne de tri (défaut 0)
    croissant: bool        – True = ordre croissant (défaut True)

    Retourne
    --------
    list[list] – nouvelle table triée
    """
    _valider_table(table, col)
    t = _copier(table)          # On travaille sur une copie
    n = len(t)

    for i in range(n):
        # `echange` permet d'arrêter tôt si le tableau est déjà trié
        echange = False

        # Chaque passage réduit la zone utile de 1 (les i derniers
        # éléments sont déjà en place)
        for j in range(0, n - i - 1):

            # Comparer la valeur de la colonne-clé de deux lignes voisines
            val_j     = t[j][col]
            val_j_sui = t[j + 1][col]

            # Déterminer si on doit échanger selon l'ordre souhaité
            doit_echanger = (val_j > val_j_sui) if croissant else (val_j < val_j_sui)

            if doit_echanger:
                t[j], t[j + 1] = t[j + 1], t[j]   # Échange des lignes entières
                echange = True

        # Si aucun échange n'a eu lieu, le tableau est trié : on sort
        if not echange:
            break

    return t


# --------------------------------------------------------------------
# 2. TRI RAPIDE (Quick Sort)
# --------------------------------------------------------------------
def tri_rapide(table, col=0, croissant=True):
    """
    Trie la table selon la colonne `col` par la méthode du tri rapide.

    Principe :
      On choisit un élément « pivot » (ici le dernier de la liste).
      On partitionne le tableau en deux sous-listes :
        - les lignes dont la valeur est ≤ pivot
        - les lignes dont la valeur est > pivot
      On applique récursivement le même algorithme sur chaque sous-liste,
      puis on concatène : [petits] + [pivot] + [grands].

    Complexité : O(n log n) en moyenne, O(n²) dans le pire cas.

    Paramètres
    ----------
    table    : list[list]  – table 2D source (non modifiée)
    col      : int         – index de la colonne de tri (défaut 0)
    croissant: bool        – True = ordre croissant (défaut True)

    Retourne
    --------
    list[list] – nouvelle table triée
    """
    _valider_table(table, col)
    t = _copier(table)
    return _tri_rapide_rec(t, col, croissant)


def _tri_rapide_rec(t, col, croissant):
    """Fonction récursive interne du tri rapide (travaille sur la liste t)."""

    # Cas de base : 0 ou 1 élément → déjà trié
    if len(t) <= 1:
        return t

    # Choix du pivot : dernière ligne de la (sous-)liste
    pivot = t[-1]
    val_pivot = pivot[col]

    # Séparation en trois groupes selon la valeur de la colonne-clé
    if croissant:
        inferieurs = [ligne for ligne in t[:-1] if ligne[col] <= val_pivot]
        superieurs = [ligne for ligne in t[:-1] if ligne[col]  > val_pivot]
    else:
        inferieurs = [ligne for ligne in t[:-1] if ligne[col] >= val_pivot]
        superieurs = [ligne for ligne in t[:-1] if ligne[col]  < val_pivot]

    # Récursion sur chaque groupe + concaténation avec le pivot au centre
    return _tri_rapide_rec(inferieurs, col, croissant) + [pivot] + _tri_rapide_rec(superieurs, col, croissant)


# --------------------------------------------------------------------
# 3. TRI PAR SELECTION (Selection Sort)
# --------------------------------------------------------------------
def tri_selection(table, col=0, croissant=True):
    """
    Trie la table selon la colonne `col` par la méthode du tri par sélection.

    Principe :
      On divise mentalement le tableau en deux parties :
        - la partie gauche (triée, construite progressivement)
        - la partie droite (non triée)
      À chaque étape, on recherche le minimum (ou maximum) dans la
      partie non triée, puis on l'échange avec le premier élément
      de cette partie non triée. La zone triée grandit d'un élément
      à chaque itération.

    Complexité : O(n²) quelle que soit l'entrée.

    Paramètres
    ----------
    table    : list[list]  – table 2D source (non modifiée)
    col      : int         – index de la colonne de tri (défaut 0)
    croissant: bool        – True = ordre croissant (défaut True)

    Retourne
    --------
    list[list] – nouvelle table triée
    """
    _valider_table(table, col)
    t = _copier(table)
    n = len(t)

    for i in range(n):
        # `idx_extremum` est l'index de l'élément min (ou max) trouvé
        # dans la partie non triée t[i:]
        idx_extremum = i

        for j in range(i + 1, n):
            # Comparer la valeur de la colonne-clé
            val_j   = t[j][col]
            val_ext = t[idx_extremum][col]

            # Mise à jour si on trouve un candidat plus petit (croissant)
            # ou plus grand (décroissant)
            if croissant and val_j < val_ext:
                idx_extremum = j
            elif not croissant and val_j > val_ext:
                idx_extremum = j

        # Placer l'élément sélectionné à la position i (début de la zone non triée)
        t[i], t[idx_extremum] = t[idx_extremum], t[i]

    return t


# --------------------------------------------------------------------
# 4. TRI PAR INSERTION (Insertion Sort)
# --------------------------------------------------------------------
def tri_insertion(table, col=0, croissant=True):
    """
    Trie la table selon la colonne `col` par la méthode du tri par insertion.

    Principe :
      Similaire à la façon dont on trie des cartes à jouer dans la main.
      On considère que le premier élément est déjà trié.
      Pour chaque nouvel élément (à partir du deuxième), on le « retire »
      et on le réinsère à la bonne position dans la partie déjà triée
      en décalant vers la droite les éléments plus grands que lui.

    Complexité : O(n²) dans le pire cas, O(n) si déjà trié (très efficace
                 sur des données quasi-triées).

    Paramètres
    ----------
    table    : list[list]  – table 2D source (non modifiée)
    col      : int         – index de la colonne de tri (défaut 0)
    croissant: bool        – True = ordre croissant (défaut True)

    Retourne
    --------
    list[list] – nouvelle table triée
    """
    _valider_table(table, col)
    t = _copier(table)
    n = len(t)

    for i in range(1, n):
        # On mémorise la ligne courante à insérer
        ligne_courante = t[i]
        val_courante   = ligne_courante[col]

        # `j` va reculer dans la partie triée pour trouver la bonne position
        j = i - 1

        # Décaler vers la droite tant que l'élément en t[j] est
        # « plus grand » que la ligne courante (en croissant)
        while j >= 0 and (
            (croissant     and t[j][col] > val_courante) or
            (not croissant and t[j][col] < val_courante)
        ):
            t[j + 1] = t[j]   # Décalage d'une position vers la droite
            j -= 1

        # Insérer la ligne courante à la position trouvée
        t[j + 1] = ligne_courante

    return t


# --------------------------------------------------------------------
# 5. TRI PAR FUSION (Merge Sort)
# --------------------------------------------------------------------
def tri_fusion(table, col=0, croissant=True):
    """
    Trie la table selon la colonne `col` par la méthode du tri par fusion.

    Principe (diviser pour régner) :
      1. DIVISER  : couper récursivement le tableau en deux moitiés égales
                   jusqu'à obtenir des sous-tableaux de taille 1.
      2. CONQUÉRIR: un tableau de taille 1 est trivialement trié.
      3. FUSIONNER: regrouper deux sous-tableaux triés en un seul tableau
                   trié en comparant leurs éléments un à un.

    Complexité : O(n log n) dans tous les cas — algorithme optimal pour
                 les tris par comparaison.

    Paramètres
    ----------
    table    : list[list]  – table 2D source (non modifiée)
    col      : int         – index de la colonne de tri (défaut 0)
    croissant: bool        – True = ordre croissant (défaut True)

    Retourne
    --------
    list[list] – nouvelle table triée
    """
    _valider_table(table, col)
    t = _copier(table)
    return _tri_fusion_rec(t, col, croissant)


def _tri_fusion_rec(t, col, croissant):
    """Fonction récursive interne du tri par fusion."""

    # Cas de base : tableau vide ou d'un seul élément → déjà trié
    if len(t) <= 1:
        return t

    # --- PHASE DIVISER ---
    milieu = len(t) // 2
    gauche = _tri_fusion_rec(t[:milieu], col, croissant)   # Moitié gauche (récursif)
    droite = _tri_fusion_rec(t[milieu:], col, croissant)   # Moitié droite (récursif)

    # --- PHASE FUSIONNER ---
    return _fusionner(gauche, droite, col, croissant)


def _fusionner(gauche, droite, col, croissant):
    """
    Fusionne deux sous-listes déjà triées en une seule liste triée.
    On compare tête à tête les éléments des deux listes et on ajoute
    le plus petit (ou grand) dans le résultat, jusqu'à épuisement
    d'une des deux listes. Le reste de l'autre est ajouté tel quel.
    """
    resultat = []
    i = j = 0   # Pointeurs sur les deux listes

    while i < len(gauche) and j < len(droite):
        val_g = gauche[i][col]
        val_d = droite[j][col]

        # Choisir l'élément dont la valeur est la plus petite (croissant)
        if (croissant and val_g <= val_d) or (not croissant and val_g >= val_d):
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1

    # Ajouter les éléments restants de la liste non épuisée
    resultat.extend(gauche[i:])
    resultat.extend(droite[j:])

    return resultat


# ====================================================================
#  ALGORITHMES DE RECHERCHE
# ====================================================================

# --------------------------------------------------------------------
# 6. RECHERCHE LINEAIRE (Linear Search)
# --------------------------------------------------------------------
def recherche_lineaire(table, col, valeur):
    """
    Recherche `valeur` dans la colonne `col` de la table.

    Principe :
      On parcourt chaque ligne du tableau, de la première à la dernière,
      et on compare la valeur de la colonne-clé avec `valeur`.
      Dès qu'une correspondance est trouvée, on retourne l'index de la ligne.
      Si aucune ligne ne correspond, on retourne -1.

    Avantage : fonctionne sur toute table, qu'elle soit triée ou non.
    Complexité : O(n) — on peut examiner toutes les lignes dans le pire cas.

    Paramètres
    ----------
    table  : list[list] – table 2D à parcourir
    col    : int        – index de la colonne où chercher
    valeur : any        – valeur recherchée

    Retourne
    --------
    int – index de la première ligne trouvée, -1 si absente
    """
    _valider_table(table, col)

    for i, ligne in enumerate(table):
        # Comparer la valeur de la colonne-clé de chaque ligne
        if ligne[col] == valeur:
            return i   # Trouvé : retourner l'index immédiatement

    return -1   # Non trouvé après parcours complet


# --------------------------------------------------------------------
# 7. RECHERCHE BINAIRE (Binary Search)
# --------------------------------------------------------------------
def recherche_binaire(table, col, valeur):
    """
    Recherche `valeur` dans la colonne `col` d'une table DÉJÀ TRIÉE
    par ordre croissant sur cette colonne.

    Principe :
      On maintient deux bornes : gauche (début) et droite (fin).
      À chaque itération, on calcule le milieu et on compare :
        - si table[milieu][col] == valeur → trouvé !
        - si table[milieu][col]  < valeur → la valeur est dans la moitié droite
        - si table[milieu][col]  > valeur → la valeur est dans la moitié gauche
      On réduit ainsi l'espace de recherche de moitié à chaque étape.

    ⚠ PRÉREQUIS : la table DOIT être triée par ordre croissant sur `col`.
       Utiliser l'un des algorithmes de tri avant d'appeler cette fonction.

    Complexité : O(log n) — beaucoup plus rapide que la recherche linéaire.

    Paramètres
    ----------
    table  : list[list] – table 2D TRIÉE (croissant) sur la colonne `col`
    col    : int        – index de la colonne de recherche
    valeur : any        – valeur recherchée (doit être comparable avec <, >)

    Retourne
    --------
    int – index de la ligne trouvée, -1 si absente
    """
    _valider_table(table, col)

    gauche = 0              # Borne inférieure de la zone de recherche
    droite = len(table) - 1 # Borne supérieure

    while gauche <= droite:
        milieu = (gauche + droite) // 2   # Index central
        val_milieu = table[milieu][col]

        if val_milieu == valeur:
            return milieu          # Valeur trouvée exactement au centre

        elif val_milieu < valeur:
            # La valeur est plus grande : chercher dans la moitié droite
            gauche = milieu + 1

        else:
            # La valeur est plus petite : chercher dans la moitié gauche
            droite = milieu - 1

    return -1   # Non trouvé


# --------------------------------------------------------------------
# 8. RECHERCHE PAR DICHOTOMIE (Dichotomic Search — version récursive)
# --------------------------------------------------------------------
def recherche_dichotomie(table, col, valeur):
    """
    Recherche `valeur` dans la colonne `col` d'une table DÉJÀ TRIÉE
    par ordre croissant sur cette colonne — version récursive.

    Principe (identique à la recherche binaire, mais implémenté de façon
    récursive pour illustrer l'approche « diviser pour régner ») :
      On divise l'espace de recherche en deux à chaque appel récursif.
      Le cas de base est atteint quand la zone est vide (non trouvé)
      ou quand la valeur centrale est égale à `valeur` (trouvé).

    ⚠ PRÉREQUIS : la table DOIT être triée par ordre croissant sur `col`.

    Complexité : O(log n) — même efficacité que la recherche binaire
                 itérative, mais avec une pile d'appels récursifs.

    Paramètres
    ----------
    table  : list[list] – table 2D TRIÉE (croissant) sur la colonne `col`
    col    : int        – index de la colonne de recherche
    valeur : any        – valeur recherchée

    Retourne
    --------
    int – index ABSOLU (dans la table originale) de la ligne trouvée,
          -1 si absente
    """
    _valider_table(table, col)
    return _dichotomie_rec(table, col, valeur, gauche=0, droite=len(table) - 1)


def _dichotomie_rec(table, col, valeur, gauche, droite):
    """
    Fonction récursive interne.
    `gauche` et `droite` délimitent la zone de recherche courante.
    """

    # Cas de base : zone de recherche vide → valeur absente
    if gauche > droite:
        return -1

    # Calculer l'index du milieu de la zone courante
    milieu = (gauche + droite) // 2
    val_milieu = table[milieu][col]

    if val_milieu == valeur:
        # Cas de base : valeur trouvée au centre
        return milieu

    elif val_milieu < valeur:
        # Recurser sur la moitié droite (les valeurs plus grandes)
        return _dichotomie_rec(table, col, valeur, milieu + 1, droite)

    else:
        # Recurser sur la moitié gauche (les valeurs plus petites)
        return _dichotomie_rec(table, col, valeur, gauche, milieu - 1)


# ====================================================================
#  UTILITAIRES D'AFFICHAGE
# ====================================================================

def afficher_table(table, titre="Table 2D"):
    """
    Affiche la table de manière lisible dans la console.

    Paramètres
    ----------
    table : list[list] – table à afficher
    titre : str        – titre affiché au-dessus (défaut "Table 2D")
    """
    print(f"\n{'=' * 50}")
    print(f"  {titre}")
    print(f"{'=' * 50}")
    for i, ligne in enumerate(table):
        print(f"  [{i:>2}]  {ligne}")
    print(f"{'=' * 50}\n")


# ====================================================================
#  GÉNÉRATION ALÉATOIRE D'UNE TABLE 2D
# ====================================================================

def generer_table_aleatoire(nb_lignes=8, nb_cols=3, val_min=1, val_max=100, graine=None):
    """
    Génère une table 2D remplie de valeurs entières aléatoires.

    Principe :
      On utilise le module `random` de Python pour produire des entiers
      entre val_min et val_max. La graine (seed) permet de reproduire
      exactement le même tableau lors d'appels successifs, ce qui est
      utile pour les tests et le débogage.

    Paramètres
    ----------
    nb_lignes : int  – nombre de lignes (défaut 8)
    nb_cols   : int  – nombre de colonnes (défaut 3)
    val_min   : int  – valeur minimale possible (défaut 1)
    val_max   : int  – valeur maximale possible (défaut 100)
    graine    : int  – graine pour le générateur aléatoire (défaut None = aléatoire pur)

    Retourne
    --------
    list[list[int]] – table 2D remplie aléatoirement
    """
    import random

    # Initialiser le générateur avec la graine fournie (reproductibilité)
    if graine is not None:
        random.seed(graine)

    # Construire la table ligne par ligne, colonne par colonne
    table = [
        [random.randint(val_min, val_max) for _ in range(nb_cols)]
        for _ in range(nb_lignes)
    ]

    return table


# ====================================================================
#  BLOC DE TEST (execute uniquement si ce fichier est lancé directement)
# ====================================================================
if __name__ == "__main__":

    # ------------------------------------------------------------------
    # GÉNÉRATION ALÉATOIRE DE LA TABLE
    # La table contient 8 lignes et 3 colonnes d'entiers entre 1 et 99.
    # La graine 42 garantit un résultat reproductible à chaque exécution.
    # ------------------------------------------------------------------
    TABLE_ORIGINALE = generer_table_aleatoire(
        nb_lignes=8,
        nb_cols=3,
        val_min=1,
        val_max=99,
        graine=42          # Supprimer ou changer pour un tableau différent à chaque run
    )

    afficher_table(TABLE_ORIGINALE, "Table 2D générée aléatoirement  [col0 | col1 | col2]")

    # ==================================================================
    # DÉMONSTRATION DES ALGORITHMES DE TRI
    # Chaque algorithme trie une copie de la table → l'originale est
    # préservée et réutilisable pour tous les tests.
    # ==================================================================
    print("=" * 60)
    print("  ALGORITHMES DE TRI  (colonne 0 — ordre croissant)")
    print("=" * 60)

    # --- Tri à bulle ---
    # Compare et échange des voisins adjacents jusqu'à stabilisation.
    res_bulle = tri_bulle(TABLE_ORIGINALE, col=0)
    afficher_table(res_bulle, "Tri à bulle (col=0, croissant)")

    # --- Tri rapide ---
    # Partitionne autour d'un pivot et trie récursivement chaque moitié.
    res_rapide = tri_rapide(TABLE_ORIGINALE, col=0)
    afficher_table(res_rapide, "Tri rapide (col=0, croissant)")

    # --- Tri par sélection ---
    # Sélectionne le minimum de la zone non triée et le place en tête.
    res_selection = tri_selection(TABLE_ORIGINALE, col=0)
    afficher_table(res_selection, "Tri par sélection (col=0, croissant)")

    # --- Tri par insertion ---
    # Insère chaque élément à sa bonne place dans la partie déjà triée.
    res_insertion = tri_insertion(TABLE_ORIGINALE, col=0)
    afficher_table(res_insertion, "Tri par insertion (col=0, croissant)")

    # --- Tri par fusion (ordre décroissant pour varier) ---
    # Divise, trie récursivement, puis fusionne les deux moitiés triées.
    res_fusion = tri_fusion(TABLE_ORIGINALE, col=0, croissant=False)
    afficher_table(res_fusion, "Tri par fusion (col=0, décroissant)")

    # ==================================================================
    # DÉMONSTRATION DES ALGORITHMES DE RECHERCHE
    # Les recherches binaire et dichotomique nécessitent une table triée.
    # On utilise le résultat du tri rapide (croissant, col=0).
    # ==================================================================
    print("=" * 60)
    print("  ALGORITHMES DE RECHERCHE")
    print("=" * 60)

    # Table triée (croissant, col=0) pour la recherche binaire/dichotomie
    table_triee = tri_rapide(TABLE_ORIGINALE, col=0)

    # Récupérer des valeurs réelles de la table pour les tests
    valeur_existante = TABLE_ORIGINALE[3][0]    # Valeur présente en ligne 3
    valeur_absente   = 9999                     # Valeur à coup sûr absente

    # --- Recherche linéaire ---
    # Parcourt toutes les lignes une à une — fonctionne sans tri préalable.
    idx_lin_ok = recherche_lineaire(TABLE_ORIGINALE, col=0, valeur=valeur_existante)
    idx_lin_ko = recherche_lineaire(TABLE_ORIGINALE, col=0, valeur=valeur_absente)
    print(f"\n[Recherche linéaire]  valeur={valeur_existante!r:>6}  →  index trouvé : {idx_lin_ok}")
    print(f"[Recherche linéaire]  valeur={valeur_absente!r:>6}  →  index trouvé : {idx_lin_ko}  (non trouvé = -1)")

    # --- Recherche binaire ---
    # Divise l'espace de recherche en deux à chaque étape — table triée requise.
    idx_bin_ok = recherche_binaire(table_triee, col=0, valeur=valeur_existante)
    idx_bin_ko = recherche_binaire(table_triee, col=0, valeur=valeur_absente)
    print(f"\n[Recherche binaire]   valeur={valeur_existante!r:>6}  →  index trouvé : {idx_bin_ok}")
    print(f"[Recherche binaire]   valeur={valeur_absente!r:>6}  →  index trouvé : {idx_bin_ko}  (non trouvé = -1)")

    # --- Recherche par dichotomie (récursive) ---
    # Même principe que la binaire mais via la récursion — table triée requise.
    idx_dic_ok = recherche_dichotomie(table_triee, col=0, valeur=valeur_existante)
    idx_dic_ko = recherche_dichotomie(table_triee, col=0, valeur=valeur_absente)
    print(f"\n[Recherche dichotomie] valeur={valeur_existante!r:>6}  →  index trouvé : {idx_dic_ok}")
    print(f"[Recherche dichotomie] valeur={valeur_absente!r:>6}  →  index trouvé : {idx_dic_ko}  (non trouvé = -1)")

    print("\n" + "=" * 60)
    print("  FIN DES TESTS — Module tri_recherche_2d opérationnel ✓")
    print("=" * 60)
