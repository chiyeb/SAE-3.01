import pandas as pd
from ADEClass import ADEClass
from insertData import *
from recupData import *
from verifData import *
from scribeData import *
# from SAE_3_01.old.database_handler import insert_maquette
# On importe la bible BUT3
BUT3 = pd.ExcelFile('Documents/BUT3 _INFO_AIX.xlsx')

# On affiche le parcours A FA pour ensuite prendre les données 
BUT3_A_FA = pd.read_excel(BUT3, 'BUT 3 Parcours A FA')

# instance de recupData
recupDataInstance = recupData()

# instance insertData
insertDataInstance = insertData()

# instance verifData
verifDataInstance = verifData()

# instance scribeData
scribeDataInstance = scribeData()

# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S5_A_FA = BUT3_A_FA.iloc[9:27, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S5_A_FA.iterrows():
    if row.isnull().iloc[0]:
        continue
    # on insère chaque ligne dans la base de donnée
    insertDataInstance.insert_maquette("S5AFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
# fonction pour récupérer les valeurs du premier semestre dans le fichier planning
recupDataInstance.trouverVal("S5AFA", "S5.A")
# fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
# la base de données pour le premier semestre
verifDataInstance.concordance("S5AFA")
scribeDataInstance.scribeRessource("S5AFA")

# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S6_A_FA = BUT3_A_FA.iloc[32:43, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S6_A_FA.iterrows():
    if row.isnull().iloc[0]:
        continue
    insertDataInstance.insert_maquette("S6AFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
# fonction pour récupérer les valeurs du premier semestre dans le fichier planning
recupDataInstance.trouverVal("S6AFA", "S6.A")
# fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
# la base de données pour le premier semestre
verifDataInstance.concordance("S6AFA")
scribeDataInstance.scribeRessource("S6AFA")

# On affiche le parcours A FI pour ensuite prendre les données 
BUT3_A_FI = pd.read_excel(BUT3, 'BUT 3 Parcours A FI')
# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S5_A_FI = BUT3_A_FI.iloc[9:27, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S5_A_FI.iterrows():
    if row.isnull().iloc[0]:
        continue
    insertDataInstance.insert_maquette("S5AFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
# fonction pour récupérer les valeurs du premier semestre dans le fichier planning
recupDataInstance.trouverVal("S5AFI", "S5.A")
# fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
# la base de données pour le premier semestre
verifDataInstance.concordance("S5AFI")
scribeDataInstance.scribeRessource("S5AFI")

# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S6_A_FI = BUT3_A_FI.iloc[32:42, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S6_A_FI.iterrows():
    if row.isnull().iloc[0]:
        continue
    insertDataInstance.insert_maquette("S6AFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
# fonction pour récupérer les valeurs du premier semestre dans le fichier planning
recupDataInstance.trouverVal("S6AFI", "S6.A")
# fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
# la base de données pour le premier semestre
verifDataInstance.concordance("S6AFI")
scribeDataInstance.scribeRessource("S6AFI")

# On affiche le parcours B FA pour ensuite prendre les données 
BUT3_B_FA = pd.read_excel(BUT3, 'BUT 3 Parcours B FA')
# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S5_B_FA = BUT3_B_FA.iloc[9:25, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S5_B_FA.iterrows():
    if row.isnull().iloc[0]:
        continue
    insertDataInstance.insert_maquette("S5BFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])

# fonction pour récupérer les valeurs du premier semestre dans le fichier planning
recupDataInstance.trouverVal("S5BFA", "S5.B")
# fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
# la base de données pour le premier semestre
verifDataInstance.concordance("S5BFA")
scribeDataInstance.scribeRessource("S5BFA")

# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S6_B_FA = BUT3_B_FA.iloc[30:41, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S6_B_FA.iterrows():
    if row.isnull().iloc[0]:
        continue
    insertDataInstance.insert_maquette("S6BFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
# fonction pour récupérer les valeurs du premier semestre dans le fichier planning
recupDataInstance.trouverVal("S6BFA", "S6.B")
# fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
# la base de données pour le premier semestre
verifDataInstance.concordance("S6BFA")
scribeDataInstance.scribeRessource("S6BFA")

# On affiche le parcours B FI pour ensuite prendre les données
BUT3_B_FI = pd.read_excel(BUT3, 'BUT 3 Parcours B FI')
# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S5_B_FI = BUT3_B_FI.iloc[9:25, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S5_B_FI.iterrows():
    if row.isnull().iloc[0]:
        continue
    insertDataInstance.insert_maquette("S5BFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
# fonction pour récupérer les valeurs du premier semestre dans le fichier planning
recupDataInstance.trouverVal("S5BFI", "S5.A")
# fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
# la base de données pour le premier semestre
verifDataInstance.concordance("S5BFI")
scribeDataInstance.scribeRessource("S5BFI")

# On récupère les lignes et colonnes utiles
select_colonne_BUT3_S6_B_FI = BUT3_B_FI.iloc[30:40, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT3_S6_B_FI.iterrows():
    if row.isnull().iloc[0]:
        continue
    insertDataInstance.insert_maquette("S6BFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
# fonction pour récupérer les valeurs du premier semestre dans le fichier planning
recupDataInstance.trouverVal("S6BFI", "S6.B")
# fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
# la base de données pour le premier semestre
verifDataInstance.concordance("S6BFI")
scribeDataInstance.scribeRessource("S6BFI")