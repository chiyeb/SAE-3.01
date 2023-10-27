import numpy as np
import pandas as pd
from ADEClass import ADEClass
from database_handler import insert_maquette
BUT1 = pd.ExcelFile('./BUT1_INFO_AIX.xlsx')


BUT1_1 = pd.read_excel(BUT1, 'BUT 1')

select_colonne_BUT1_S1 = BUT1_1.iloc[10:31, [0, 2, 17, 18, 19]]
liste_adeS1 = []
for index, row in select_colonne_BUT1_S1.iterrows():
    if row.isnull().iloc[0]:
        continue
    #On crée un objet ADE et on rentre les valeurs pour chaque ligne
    ADE = ADEClass(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
    #on insère chaque ligne dans la base de donnée
    insert_maquette("S1",row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
    liste_adeS1.append(ADE)




select_colonne_BUT1_S2 = BUT1_1.iloc[36:58, [0, 2, 17, 18, 19]]
liste_adeS2 = []
for index, row in select_colonne_BUT1_S2.iterrows():
    if row.isnull().iloc[0]:
        continue
    # on insère chaque ligne dans la base de donnée
    insert_maquette("S2", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])
    # On crée un objet ADE et on rentre les valeurs pour chaque ligne
    ADE = ADEClass(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4])

    liste_adeS2.append(ADE)
