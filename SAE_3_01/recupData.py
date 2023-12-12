import sqlite3
import pandas as pd


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
                        insertdata.insert_planning(semestre, libelle, valeur_case_3, valeur_case_5, valeur_case_7, valeur_case_12)
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

    def recupHoraire(self, semestre, semestre_onglet):
        print("recupHoraire appelé")

        # Chargement du fichier Excel
        horaire = pd.ExcelFile('Documents/Planning 2023-2024.xlsx')

        # Récupère les données de la table Maquette
        self.cursor.execute("SELECT Libelle, Num_Res FROM Maquette WHERE Semestre = ?", (semestre,))
        resultats = self.cursor.fetchall()
        print(resultats)

        # Lecture du fichier Excel en dehors de la boucle pour éviter de le charger à chaque itération
        S = pd.read_excel(horaire, semestre_onglet)

        # Recherche du mot "Date" dans les colonnes
        for col in S.columns:
            if 'Date' in col:
                # Récupère les dates à partir de la 2ème ligne
                dates_list = S[col].head(23).iloc[1:].tolist()

                for date in dates_list:
                    # Vérifie si la date existe dans la colonne
                    if date in S[col].values:
                        index_date = S[S[col] == date].index[0]
                        start_col_index = max(0, S.columns.get_loc(col) - 23)
                        row_data = S.iloc[index_date, start_col_index: S.columns.get_loc(col) + 1].tolist()
                        print(f"Date: {date}, Ligne à gauche: {row_data}")
                    else:
                        print(f"La date {date} n'a pas été trouvée dans la colonne {col}")















    def __del__(self):
        # Ferme la connexion à la base de données lorsque l'objet est détruit
        self.conn.close()



recupdata = recupData()
recupdata.recupNomProf()
recupdata.recupHoraire("S1", "S1")

