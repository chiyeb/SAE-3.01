import pandas as pd
from SAE_3_01.old.database_handler import *

conn = sqlite3.connect('../database/database.db')
cursor = conn.cursor()
planning = pd.ExcelFile('../Documents/Planning 2023-2024.xlsx')

def trouverVal(semestre, semestre_onglet):
    cursor.execute("SELECT Libelle, Num_Res FROM Maquette WHERE Semestre = ?", (semestre,))
    resultats = cursor.fetchall()  # Récupérer toutes les valeurs de "Num_Res" pour le semestre donné
    print(resultats)
    for row in resultats:
        num_res = row[1]
        libelle = row[0]
        S = pd.read_excel(planning, semestre_onglet)

        for index, row in S.iterrows():
            if num_res in row.values:
                index_num_res = row.values.tolist().index(num_res)
                if index_num_res + 12 < len(row) and row.iloc[index_num_res + 3] >= 0:
                    valeur_case_3 = row.iloc[index_num_res + 3]
                    valeur_case_5 = row.iloc[index_num_res + 5]
                    valeur_case_7 = row.iloc[index_num_res + 7]
                    valeur_case_12 = row.iloc[index_num_res + 10]
                    # Vérifie si les valeurs sont NaN ou vides et remplace par 0 si nécessaire
                    if pd.isna(valeur_case_3) or valeur_case_3 == "":
                        valeur_case_3 = 0
                    if pd.isna(valeur_case_5) or valeur_case_5 == "":
                        valeur_case_5 = 0
                    if pd.isna(valeur_case_7) or valeur_case_7 == "":
                        valeur_case_7 = 0
                    if pd.isna(valeur_case_12) or valeur_case_12 == "":
                        valeur_case_12 = 0
                    print(f"Num_Res trouvé: {num_res}")
                    print(f"3e case après le mot: {valeur_case_3}")
                    print(f"5e case: {valeur_case_5}")
                    print(f"7e case: {valeur_case_7}")
                    print(f"12e case: {valeur_case_12}")
                    insert_planning(semestre, libelle, valeur_case_3, valeur_case_5, valeur_case_7, valeur_case_12)

trouverVal("S1", "S1")