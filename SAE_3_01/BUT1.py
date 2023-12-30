from scribeData import *
from verifData import *
from recupData import *
from insertData import *
import pandas as pd

# from SAE_3_01.old.recupValPlanning import *

# lire le fichier maquette
BUT1 = pd.ExcelFile('Documents/BUT1_INFO_AIX.xlsx')
# récupérer l'onglet BUT 1
BUT1_1 = pd.read_excel(BUT1, 'BUT 1')
# instance de recupData
recupDataInstance = recupData()
# instance insertData
insertDataInstance = insertData()
# instance verifData
verifDataInstance = verifData()
# instance scribeData
scribeDataInstance = scribeData()
# Sélection des heures du premier semestre
select_colonne_BUT1_S1 = BUT1_1.iloc[10:31, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT1_S1.iterrows():
    if row.isnull().iloc[0]:
        continue
    # on insère chaque ligne dans la base de donnée
    insertDataInstance.insert_maquette("S1", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
# fonction pour récupérer les valeurs du premier semestre dans le fichier planning
recupDataInstance.trouverVal("S1", "S1")
# fonction pour vérifier les concordances entre le fichier planning et le fichier maquette national à partir de
# la base de données pour le premier semestre
verifDataInstance.concordance("S1")
# fonction pour récupérer les valeurs du premier semestre dans le fichier planning
recupDataInstance.trouverVal("S1", "S1")
# écrire les informations du S1
scribeDataInstance.scribeRessource("S1")
# Récupérer les cours par date dans le fichier planning
recupDataInstance.recupXetY("S1", "S1")
# Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
verifDataInstance.concordancePlanning("S1")

# Sélection des heures du deuxième semestre
select_colonne_BUT1_S2 = BUT1_1.iloc[36:58, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT1_S2.iterrows():
    if row.isnull().iloc[0]:
        continue
    # on insère chaque ligne dans la base de donnée
    insertDataInstance.insert_maquette("S2", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
# fonction pour récupérer les valeurs du deuxième semestre dans le fichier planning
recupDataInstance.trouverVal("S2", "S2")
# fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
# la base de données pour le deuxième semestre
verifDataInstance.concordance("S2")
# fonction pour récupérer les valeurs du deuxième semestre dans le fichier planning
recupDataInstance.trouverVal("S2", "S2")
# écrire les informations du S2
scribeDataInstance.scribeRessource("S2")
# Récupérer les cours par date dans le fichier planning
recupDataInstance.recupXetY("S2", "S2")
# Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
verifDataInstance.concordancePlanning("S2")