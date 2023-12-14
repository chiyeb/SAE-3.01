import sqlite3
import math
import openpyxl as openpyxl
import pandas as pd


class scribeData:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(scribeData, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def _setup(self):
        # Initialise la connexion à la base de données
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()

    def scribeRessource(self, ressource):
        # requête SQL pour récupérer les données depuis la base de données en utilisant la ressource fournie
        self.cursor.execute(
            "SELECT Planning.Ressource, Planning.H_CM, Planning.H_TD, Planning.H_TP, Prof.NomProf FROM Planning "
            "JOIN Prof ON Planning.Resp = Prof.Acronyme "
            "WHERE Planning.Num_res = ?",
            (ressource,))

        data_from_database = self.cursor.fetchall()
        print(data_from_database)
        # récupérer un fichier Excel existant s'il existe, sinon créer un nouveau
        try:
            workbook = openpyxl.load_workbook("Documents/S2.xlsx")
        except FileNotFoundError:
            workbook = openpyxl.Workbook()
        # Sélectionner la feuille active
        worksheet = workbook.active
        # Définir les lignes et colonnes correspondantes
        row = 5
        col_h_cm = 2
        col_h_td = 3
        col_h_tp = 4
        if data_from_database:
            # Récupère les valeurs de la requête SQL et écrire les données spécifiques dans le fichier Excel
            worksheet.cell(row=row, column=col_h_cm, value=data_from_database[0][1])
            worksheet.cell(row=row, column=col_h_td, value=data_from_database[0][2])
            worksheet.cell(row=row, column=col_h_tp, value=data_from_database[0][3])

            # Écrire la ressource fournie par l'utilisateur dans la colonne 2, ligne 2
            worksheet.cell(row=2, column=2, value=ressource)

            # Écrire le responsable dans la colonne 7, ligne 2
            worksheet.cell(row=2, column=7, value=data_from_database[0][4])

            # Sauvegarder le classeur Excel
            workbook.save("S2.xlsx")

            # Message pour confirmer les ajouts dans le fichier Excel
            print(f"Les données pour la ressource '{ressource}' ont été ajoutées à S2.xlsx")
        else:
            print(f"Aucune donnée pour la ressource '{ressource}'")

    def __del__(self):
        # Ferme la connexion à la base de données lorsque l'objet est détruit
        self.conn.close()
# Crée une instance de la classe scribeData
scribe_instance = scribeData()

# Appelle la méthode scribeRessource sur l'instance créée
scribe_instance.scribeRessource("R1.01")
