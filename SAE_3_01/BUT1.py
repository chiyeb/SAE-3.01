import numpy as np
import pandas as pd
from ADEClass import ADEClass
from recupValPlanning import *
from database_handler import insert_maquette
from Planning import *
#lire le fichier maquette
BUT1 = pd.ExcelFile('./BUT1_INFO_AIX.xlsx')
#récuperer l'onglet BUT 1
BUT1_1 = pd.read_excel(BUT1, 'BUT 1')

#Sélection des heures du premier semestre
select_colonne_BUT1_S1 = BUT1_1.iloc[10:31, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT1_S1.iterrows():
    if row.isnull().iloc[0]:
        continue
    #fonction pour récupérer les valeurs du premier semestre dans le fichier planning
    trouverVal("S1", "S1")
    # on insère chaque ligne dans la base de donnée
    insert_maquette("S1", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
    # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
    # la base de données pour le premier semestre
    concordance("S1")

#Sélection des heures du deuxième semestre
select_colonne_BUT1_S2 = BUT1_1.iloc[36:58, [0, 2, 17, 18, 19]]
for index, row in select_colonne_BUT1_S2.iterrows():
    if row.isnull().iloc[0]:
        continue
    # on insère chaque ligne dans la base de donnée
    insert_maquette("S2", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
    # fonction pour récupérer les valeurs du deuxième semestre dans le fichier planning
    trouverVal("S2", "S2")
    # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
    # la base de données pour le deuxième semestre
    concordance("S2")
