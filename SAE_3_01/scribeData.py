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
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()

    def scribeRessource(self, semestre):
        try:
            # On récupère les semestres unique de planning
            self.cursor.execute("SELECT DISTINCT Semestre FROM Planning WHERE Semestre = ?", (semestre,))
            semesters = [row[0] for row in self.cursor.fetchall()]

            # On ouvre le fichier "fichier_vierge.xlxs"
            try:
                fichier_vierge = openpyxl.load_workbook("fichier_vierge.xlsx", read_only=False)
            except FileNotFoundError:
                print("Le fichier fichier_vierge.xlsx n'a pas été trouvé.")
                exit()
            for semester in semesters:
                # Récupération des ressources pour le semestre actuel
                self.cursor.execute("SELECT DISTINCT Ressource FROM Planning WHERE Semestre = ?", (semester,))
                resources = [row[0] for row in self.cursor.fetchall()]

                for resource in resources:
                    base_sheet = fichier_vierge["Feuil1"]

                    # Création d'une nouvelle feuille Excel avec le nom de la ressource
                    worksheet = fichier_vierge.copy_worksheet(base_sheet)
                    worksheet.title = resource

                    # Récupération des données de la ressource actuelle
                    self.cursor.execute(
                        "SELECT Ressource, H_CM, H_TD, H_TP, Prof.NomProf FROM Planning "
                        "JOIN Prof ON Planning.Resp = Prof.Acronyme "
                        "WHERE Ressource = ? AND Semestre = ?",
                        (resource, semester))
                    data_from_database = self.cursor.fetchall()

                    # Écriture des données dans la nouvelle feuille Excel
                    if data_from_database:
                        worksheet.cell(row=5, column=2, value=data_from_database[0][1])
                        worksheet.cell(row=5, column=3, value=data_from_database[0][2])
                        worksheet.cell(row=5, column=4, value=data_from_database[0][3])
                        worksheet.cell(row=2, column=2, value=resource)
                        worksheet.cell(row=2, column=7, value=data_from_database[0][4])
            fichier_vierge.save(f"{semestre}.xlsx")

            print(f"Les données ont été ajoutées à {semestre}.xlsx")
        except sqlite3.Error as e:
            print(f"Erreur lors de la connexion à la base de données : {e}")

