import sqlite3
from datetime import datetime

import openpyxl
import pandas as pd
from openpyxl.reader.excel import load_workbook

from insertData import insertData


class recupData:
    def __init__(self):
        # Initialise la connexion à la base de données
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()

    def trouverVal(self, semestre, semestre_onglet):
        print("trouver val appelé")
        planning = pd.ExcelFile('Documents/Planning 2023-2024.xlsx')
        self.cursor.execute("SELECT Libelle, Num_Res FROM Maquette WHERE Semestre = ?", (semestre,))
        resultats = self.cursor.fetchall()  # Récupère les résultats de la requête
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

    def recupRCouleur(self, semestre, semestre_onglet):
        ressourceCouleur = {}
        self.cursor.execute("SELECT Num_Res FROM Maquette WHERE Semestre = ?", (semestre,))
        resultats = [item[0] for item in self.cursor.fetchall()]
        fichier = openpyxl.load_workbook('Documents/Planning 2023-2024.xlsx')
        fichierOngletSemestre = fichier[semestre_onglet]
        for row in fichierOngletSemestre.iter_rows():
            for cell in row:
                if cell.value in resultats:
                    couleur = cell.fill.start_color.rgb
                    print(couleur)
                    if couleur != '00000000' and couleur:
                        ressourceCouleur[cell.value] = couleur
        print(ressourceCouleur)
        return ressourceCouleur

    def recupXetY(self, semestre, semestre_onglet, ressourceCouleur):
        fichier = openpyxl.load_workbook('Documents/Planning 2023-2024.xlsx', data_only=True)
        fichierOngletSemestre = fichier[semestre_onglet]
        for col in fichierOngletSemestre.iter_cols():
            if col[0].value is not None and 'Date' in col[0].value:
                # Parcourir les lignes pour cette colonne de date
                for cell in col:
                    cell_value = cell.value
                    if isinstance(cell_value, datetime):
                        date = cell_value.date()  # Récupérer seulement la partie date
                    else:
                        date = cell_value
                    if date:
                        row_index = cell.row
                        for row_cell in fichierOngletSemestre[row_index]:
                            # Récupérer la valeur et la couleur de chaque cellule de la ligne
                            if row_cell.value == "X" or row_cell.value == "Y":
                                if row_cell.value == "X":
                                    tCours = "TD"
                                else:
                                    tCours = "TP"
                                valeur = row_cell.value
                                couleur = row_cell.fill.start_color.rgb
                                idCours = row_cell.coordinate
                                print(date)
                                for cle, valeur in ressourceCouleur.items():
                                    if valeur == couleur:
                                        self.cursor.execute("SELECT IdCours, Semestre FROM Cours WHERE IdCours = ? "
                                                            "AND Semestre = ?", (idCours,semestre))
                                        resultCours = self.cursor.fetchone()
                                        self.cursor.execute(
                                            "SELECT Ressource, Type_Cours FROM Horaires WHERE Ressource "
                                            "= ? AND Type_Cours = ?",
                                            (cle, tCours))
                                        resultHoraires = self.cursor.fetchone()
                                        if not resultCours:
                                            if row_cell.comment:
                                                commentaire = row_cell.comment.text
                                                self.cursor.execute("INSERT INTO Cours (IdCours, Semestre, Ressource, "
                                                                    "Date, Commentaire, Type_Cours) VALUES (?, ?, "
                                                                    "?, ?,"
                                                                    " ?, ?)",
                                                                    (idCours, semestre, cle, date, commentaire, tCours))
                                            else:
                                                self.cursor.execute("INSERT INTO Cours (IdCours, Semestre, Ressource, "
                                                                    "Date, Type_Cours) VALUES (?, ?, "
                                                                    "?, ?, ?)",
                                                                    (idCours, semestre, cle, date, tCours))
                                            self.conn.commit()
                                        else:
                                            if row_cell.comment:
                                                commentaire = row_cell.comment.text
                                                self.cursor.execute("UPDATE Cours SET Ressource = ?, Date = ?, "
                                                                    "Commentaire = ?, Type_Cours = ? WHERE IdCours = ? ",
                                                                    (cle, date, commentaire, tCours, idCours))
                                            else:
                                                self.cursor.execute("UPDATE Cours SET Ressource = ?, Date = ?, "
                                                                    "Type_Cours = ? WHERE IdCours = ? ",
                                                                    (cle, date, tCours, idCours))
                                            self.conn.commit()
                                        if resultHoraires:
                                            self.cursor.execute("UPDATE Horaires SET NbCours = NbCours+1 WHERE "
                                                                "Ressource = ? AND Type_Cours = ?",
                                                                (cle, tCours))
                                        else:
                                            self.cursor.execute("INSERT INTO Horaires (Semestre, Ressource, Dates, "
                                                                "Type_Cours, nbCours) VALUES (?, ?, ?, ?,"
                                                                " 1)",
                                                                (semestre, cle, date, tCours))
                                        self.cursor.connection.commit()
                                        print(f"Cle: {cle} Valeur: {valeur}, Couleur: {couleur}")

    def __del__(self):
        # Ferme la connexion à la base de données lorsque l'objet est détruit
        self.conn.close()


recupdata = recupData()
recupdata.recupNomProf()
# recupdata.recupRCouleur("S1", "S1")
# recupdata.recupHoraire("S1", "S1")
recupdata.recupXetY("S1", "S1", recupdata.recupRCouleur("S1", "S1"))
