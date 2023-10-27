import sqlite3
import openpyxl

# Demander à l'utilisateur la ressource à rechercher
resource = input("Entrez la ressource que vous souhaitez écrire dans le fichier Excel : ")

# Connexion à la base de données SQLite
try:
    with sqlite3.connect("database/database.db") as conn:
        cursor = conn.cursor()

        # Exécutez une requête SQL pour récupérer les données depuis la base de données en utilisant la ressource fournie par l'utilisateur
        cursor.execute("SELECT Ressource, H_CM, H_TD, H_TP, Resp FROM Planning WHERE Ressource LIKE ?", ('%' + resource + '%',))

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

        # Récupère les valeurs de la requête SQL et écrire les données spécifiques dans le fichier Excel
        worksheet.cell(row=row, column=col_h_cm, value=data_from_database[0][1])
        worksheet.cell(row=row, column=col_h_td, value=data_from_database[0][2])
        worksheet.cell(row=row, column=col_h_tp, value=data_from_database[0][3])

        # Écrire la ressource fournie par l'utilisateur dans la colonne 2, ligne 2
        worksheet.cell(row=2, column=2, value=resource)

        # Écrire le responsable dans la colonne 7, ligne 2
        worksheet.cell(row=2, column=7, value=data_from_database[0][4])

        # Sauvegarder le classeur Excel
        workbook.save("S2.xlsx")

        # Message pour confirmer les ajouts dans le fichier Excel
        print(f"Les données pour la ressource '{resource}' ont été ajoutées à S2.xlsx")

# Si une erreur survient lors de la connexion à la base de données, affichez un message d'erreur
except sqlite3.Error as e:
    print(f"Erreur lors de la connexion à la base de données : {e}")
