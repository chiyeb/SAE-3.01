import sqlite3
import math
import pandas as pd

from insertData import insertData


class recupData:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(recupData, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def _setup(self):
        # Initialise la connexion à la base de données
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()

    def trouverVal(self, semestre, semestre_onglet):
        print("trouver val appelé")
        planning = pd.ExcelFile('Documents/Planning 2023-2024.xlsx')
        self.cursor.execute("SELECT Libelle, Num_Res FROM Maquette WHERE Semestre = ?", (semestre,))
        resultats = self.cursor.fetchall()  # Récupérer toutes les valeurs de "Num_Res" pour le semestre donné
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
                        insertdata = insertData()
                        insertdata.insert_planning(semestre, libelle, valeur_case_3, valeur_case_5, valeur_case_7,
                                                   valeur_case_12)

    def recupNomProf(self):
        # Ouvre le fichier en mode lecture
        with open("Documents/NomProf.txt", "r") as fichier:
            # Lire chaque ligne du fichier
            for ligne in fichier:
                # Divise la ligne en utilisant le signe "=" comme séparateur
                parties = ligne.strip().split("=")

                # Vérifie si la ligne a été correctement divisée en deux parties
                if len(parties) == 2:
                    # Exécute la requête SQL
                    resultat_requete = self.cursor.execute("SELECT Acronyme, NomProf FROM PROF WHERE Acronyme = ?",
                                                           (parties[0],)).fetchall()
                    # Vérifie si la requête a renvoyé des résultats
                    if resultat_requete:
                        # On update le nom du prof
                        self.cursor.execute("UPDATE PROF SET NomProf = ? WHERE Acronyme = ?", (parties[1], parties[0]))
                        self.conn.commit()
                    else:
                        # On insère le nouveau prof
                        self.cursor.execute(
                            "INSERT INTO Prof (Acronyme, NomProf) VALUES (?, ?)",
                            (parties[0], parties[1],))
                        # sauvegarder dans la base de données
                        self.conn.commit()
                else:
                    print(f"Erreur de format sur la ligne : {ligne}")

    def __del__(self):
        # Ferme la connexion à la base de données lorsque l'objet est détruit
        self.conn.close()


recupdata = recupData()
recupdata.recupNomProf()
