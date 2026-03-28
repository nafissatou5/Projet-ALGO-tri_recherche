import tri_recherche_2d as t2d

# Génération d'une table
table = t2d.generer_table_aleatoire(graine=10)

t2d.afficher_table(table, "Table originale")

# Tri rapide
table_triee = t2d.tri_rapide(table, col=0)

t2d.afficher_table(table_triee, "Table triée")

# Recherche binaire
valeur = table_triee[2][0]
index = t2d.recherche_binaire(table_triee, col=0, valeur=valeur)

print("Valeur recherchée :", valeur)
print("Index trouvé :", index)
