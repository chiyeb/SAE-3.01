import pandas as pd
from ADEClass import ADEClass
from insertData import insertData
from recupData import recupData
from verifData import verifData

# from SAE_3_01.old.database_handler import insert_maquette
# On importe la bible BUT3
BUT3 = pd.ExcelFile('Documents/BUT3 _INFO_AIX.xlsx')

# On affiche le parcours A FA pour ensuite prendre les données 
BUT3_A_FA = pd.read_excel(BUT3, 'BUT 3 Parcours A FA')
# instance de recupData
recupdata = recupData()
# instance insertData
insertdata = insertData()
# instance verifData
verifdata = verifData()
# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S5_A_FA = BUT3_A_FA.iloc[9:27, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S5_A_FA.iterrows():
    if row.isnull().iloc[0]:
        continue
    # on insère chaque ligne dans la base de donnée
    insertdata.insert_maquette("S5AFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])

    # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
    # la base de données pour le premier semestre
    verifdata.concordance("S5AFA")

# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S6_A_FA = BUT3_A_FA.iloc[32:43, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S6_A_FA.iterrows():
    if row.isnull().iloc[0]:
        continue
    insertdata.insert_maquette("S6AFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])

    # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
    # la base de données pour le premier semestre
    verifdata.concordance("S6AFA")

# On affiche le parcours A FI pour ensuite prendre les données 
BUT3_A_FI = pd.read_excel(BUT3, 'BUT 3 Parcours A FI')

# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S5_A_FI = BUT3_A_FI.iloc[9:27, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S5_A_FI.iterrows():
    if row.isnull().iloc[0]:
        continue
    insertdata.insert_maquette("S5AFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])

    # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
    # la base de données pour le premier semestre
    verifdata.concordance("S5AFI")

# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S6_A_FI = BUT3_A_FI.iloc[32:42, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S6_A_FI.iterrows():
    if row.isnull().iloc[0]:
        continue
    insertdata.insert_maquette("S6AFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])

    # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
    # la base de données pour le premier semestre
    verifdata.concordance("S6AFI")

# On affiche le parcours B FA pour ensuite prendre les données 
BUT3_B_FA = pd.read_excel(BUT3, 'BUT 3 Parcours B FA')

# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S5_B_FA = BUT3_B_FA.iloc[9:25, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S5_B_FA.iterrows():
    if row.isnull().iloc[0]:
        continue
    insertdata.insert_maquette("S5BFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])

    # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
    # la base de données pour le premier semestre
    verifdata.concordance("S5BFA")

# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S6_B_FA = BUT3_B_FA.iloc[30:41, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S6_B_FA.iterrows():
    if row.isnull().iloc[0]:
        continue
    insertdata.insert_maquette("S6BFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])

    # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
    # la base de données pour le premier semestre
    verifdata.concordance("S6BFA")

# On affiche le parcours B FI pour ensuite prendre les données
BUT3_B_FI = pd.read_excel(BUT3, 'BUT 3 Parcours B FI')

# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S5_B_FI = BUT3_B_FI.iloc[9:25, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S5_B_FI.iterrows():
    if row.isnull().iloc[0]:
        continue
    insertdata.insert_maquette("S5BFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])

    # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
    # la base de données pour le premier semestre
    verifdata.concordance("S5BFI")

# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S6_B_FI = BUT3_B_FI.iloc[30:40, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S6_B_FI.iterrows():
    if row.isnull().iloc[0]:
        continue
    insertdata.insert_maquette("S6BFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])

    # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
    # la base de données pour le premier semestre
    verifdata.concordance("S6BFI")
