import sqlite3
import openpyxl

# Connexion à la base de données SQLite
try:
    with sqlite3.connect("database/database.db") as conn:
        cursor = conn.cursor()

        # Exécutez une requête SQL pour récupérer les données depuis la base de données
        cursor.execute("SELECT Libelle, H_CM, H_TD, H_TP FROM Maquette WHERE Libelle LIKE '%R1.01%'")

        # Récupérez les données dans une liste de tuples
        data_from_database = cursor.fetchall()

        # Charger un classeur Excel existant s'il existe, sinon créer un nouveau
        try:
            workbook = openpyxl.load_workbook("S2.xlsx")
        except FileNotFoundError:
            workbook = openpyxl.Workbook()

        # Sélectionner la feuille active
        worksheet = workbook.active

        # Définir les lignes et colonnes correspondantes
        row = 5
        col_h_cm = 2
        col_h_td = 3
        col_h_tp = 4

        # Récupère les valeur de la requetes SQL écrire les données spécifiques à la ligne 5, colonnes 2, 3 et 4
        worksheet.cell(row=row, column=col_h_cm, value=data_from_database[0][1])
        worksheet.cell(row=row, column=col_h_td, value=data_from_database[0][2])
        worksheet.cell(row=row, column=col_h_tp, value=data_from_database[0][3])

        # Écrire "R1.01 Initiation au développement" dans la colonne 2, ligne 2
        worksheet.cell(row=2, column=2, value=data_from_database[0][0])

        # Écrire "test" dans la colonne 7, ligne 2 à remplacer par la suite avec la base de donnée pour le responsable
        worksheet.cell(row=2, column=7, value="test")

        # Sauvegarder le classeur Excel
        workbook.save("S2.xlsx")

        # Message pour comfirmer les ajouts dans le fichier excel
        print("Les données ont été ajoutées à S2.xlsx")

# Si il y a un problème lors de la connexion on affiche un message d'erreur
except sqlite3.Error as e:
    print(f"Erreur lors de la connexion à la base de données : {e}")
