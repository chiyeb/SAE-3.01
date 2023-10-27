import numpy as np
import pandas as pd
from ADEClass import ADEClass
from database_handler import insert_maquette

# On importe la bible BUT2
BUT2 = pd.ExcelFile('./BUT2_INFO_AIX.xlsx')


# On affiche le parcours A FA pour ensuite prendre les données 
BUT2_A_FA = pd.read_excel(BUT2, 'BUT 2 Parcours A FA')

# On récupère les lignes et colonnes utiles
select_colonne_BUT2_S3_A_FA = BUT2_A_FA.iloc[11:29, [0, 2, 17, 18, 19]] 
for index, row in select_colonne_BUT2_S3_A_FA.iterrows():
    if row.isnull().iloc[0]:
        continue
    #On crée un objet ADE et on rentre les valeurs pour chaque ligne
    ADE = ADEClass(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
    #on insère chaque ligne dans la base de donnée
    insert_maquette("S3AFA",row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])

select_colonne_BUT2_S4_A_FA = BUT2_A_FA.iloc[34:51, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT2_S4_A_FA.iterrows():
    if row.isnull().iloc[0]:
        continue
    #On crée un objet ADE et on rentre les valeurs pour chaque ligne
    ADE = ADEClass(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
    #on insère chaque ligne dans la base de donnée
    insert_maquette("S4AFA",row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])




# On affiche le parcours A FI pour ensuite prendre les données 
BUT2_A_FI = pd.read_excel(BUT2, 'BUT 2 Parcours A FI')
# On récupère les lignes et colonnes utiles
select_colonne_BUT2_S3_A_FI = BUT2_A_FI.iloc[11:29, [0, 2, 17, 18, 19]] 
for index, row in select_colonne_BUT2_S3_A_FI.iterrows():
    if row.isnull().iloc[0]:
        continue
    #On crée un objet ADE et on rentre les valeurs pour chaque ligne
    ADE = ADEClass(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
    #on insère chaque ligne dans la base de donnée
    insert_maquette("S3AFI",row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])


# On récupère les lignes et colonnes utiles
select_colonne_BUT2_S4_A_FI = BUT2_A_FI.iloc[34:51, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT2_S4_A_FI.iterrows():
    if row.isnull().iloc[0]:
        continue
    #On crée un objet ADE et on rentre les valeurs pour chaque ligne
    ADE = ADEClass(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
    #on insère chaque ligne dans la base de donnée
    insert_maquette("S4AFI",row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])



# On affiche le parcours B FA pour ensuite prendre les données 
BUT2_B_FA = pd.read_excel(BUT2, 'BUT 2 Parcours B FA')

# On récupère les lignes et colonnes utiles
select_colonne_BUT2_S3_B_FA = BUT2_B_FA.iloc[11:29, [0, 2, 17, 18, 19]] 
for index, row in select_colonne_BUT2_S3_B_FA.iterrows():
    if row.isnull().iloc[0]:
        continue
    #On crée un objet ADE et on rentre les valeurs pour chaque ligne
    ADE = ADEClass(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
    #on insère chaque ligne dans la base de donnée
    insert_maquette("S3BFA",row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])

# On récupère les lignes et colonnes utiles
select_colonne_BUT2_S4_B_FA = BUT2_B_FA.iloc[34:51, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT2_S4_B_FA.iterrows():

    if row.isnull().iloc[0]:
        continue
    #On crée un objet ADE et on rentre les valeurs pour chaque ligne
    ADE = ADEClass(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
    #on insère chaque ligne dans la base de donnée
    insert_maquette("S4BFA",row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])


# On affiche le parcours B FI pour ensuite prendre les données 
BUT2_B_FI = pd.read_excel(BUT2, 'BUT 2 Parcours B FI')

# On récupère les lignes et colonnes utiles
select_colonne_BUT2_S3_B_FI = BUT2_B_FI.iloc[10:28, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT2_S3_B_FI.iterrows():
    if row.isnull().iloc[0]:
        continue
    #On crée un objet ADE et on rentre les valeurs pour chaque ligne
    ADE = ADEClass(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
    #on insère chaque ligne dans la base de donnée
    insert_maquette("S3BFI",row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])

# On récupère les lignes et colonnes utiles
select_colonne_BUT2_S4_B_FI = BUT2_B_FI.iloc[33:50, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT2_S4_B_FI.iterrows():
    if row.isnull().iloc[0]:
        continue
    #On crée un objet ADE et on rentre les valeurs pour chaque ligne
    ADE = ADEClass(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
    #on insère chaque ligne dans la base de donnée
    insert_maquette("S4BFI",row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])






