import sqlite3
import openpyxl as openpyxl
import os


class ScribeData:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(ScribeData, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def _setup(self):
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()

    def scribeRessource(self, semestre):
        try:
            print("Début de la méthode scribeRessource")

            # On récupère les semestres uniques du planning
            self.cursor.execute("SELECT DISTINCT Semestre FROM Planning WHERE Semestre = ?", (semestre,))
            semesters = [row[0] for row in self.cursor.fetchall()]
            print(f"Semestres trouvés : {semesters}")

            # On ouvre le fichier "fichier_vierge.xlsx"
            try:
                fichier_vierge = openpyxl.load_workbook("fichiers necessaires/fichier_vierge.xlsx", read_only=False)
            except FileNotFoundError:
                print("Le fichier fichier_vierge.xlsx n'a pas été trouvé.")
                exit()



            for semester in semesters:
                print(f"Traitement du semestre : {semester}")

                # On récupère des ressources pour le semestre actuel
                self.cursor.execute("SELECT DISTINCT Ressource FROM Planning WHERE Semestre = ?", (semester,))
                resources = [row[0] for row in self.cursor.fetchall()]
                print(f"Ressources trouvées : {resources}")

                for resource in resources:
                    print(f"Traitement de la ressource : {resource}")

                    base_sheet = fichier_vierge["Feuil1"]

                    # Création d'une nouvelle feuille Excel avec le nom de la ressource
                    worksheet = fichier_vierge.copy_worksheet(base_sheet)
                    worksheet.title = resource

                    # On récupère des données de la première base de données (Planning)
                    self.cursor.execute(
                        "SELECT Ressource, H_CM, H_TD, H_TP, COALESCE(Prof.NomProf, Planning.Resp) FROM Planning "
                        "LEFT JOIN Prof ON Planning.Resp = Prof.Acronyme "
                        "WHERE Ressource = ? AND Semestre = ?",
                        (resource, semester))
                    data_from_database = self.cursor.fetchall()

                    # On écrit les données de la première base de données dans la nouvelle feuille Excel
                    if data_from_database:
                        print(f"Données de la première base de données ({resource}, {semester}): {data_from_database}")
                        worksheet.cell(row=5, column=2, value=data_from_database[0][1])
                        worksheet.cell(row=5, column=3, value=data_from_database[0][2])
                        worksheet.cell(row=5, column=4, value=data_from_database[0][3])
                        worksheet.cell(row=2, column=2, value=resource)
                        worksheet.cell(row=2, column=7, value=data_from_database[0][4])

# select date from la base where semestre =? and ressource =?

                    self.cursor.execute(
                        "SELECT * FROM RecupHProf WHERE Ressource = ?",
                        (data_from_database[0][0],))
                    data_from_second_db_resultat = self.cursor.fetchall()

                    if data_from_second_db_resultat:


                        # On récupère les données de la deuxième base de données pour écrire
                        self.cursor.execute(
                            "SELECT Intervenant FROM RecupHProf WHERE Ressource = ?",
                            (resource,))
                        data_from_database = self.cursor.fetchall()



                         # On écrit les données intervenant de la deuxième base de données
                        if data_from_database:
                            print(f"Données de la deuxième base de données ({resource}): {data_from_database}")

                            row_index = 8
                            for intervenant in data_from_database:
                                worksheet.cell(row=row_index, column=1, value=intervenant[0])
                                row_index += 1

                        # On récupère les noms des intervenants ayant un chiffre dans la colonne CM pour afficher les profs qui font les CM
                        self.cursor.execute(
                            "SELECT Intervenant,CM FROM RecupHProf WHERE Ressource = ? AND CM IS NOT NULL",
                            (resource,))

                        data_from_database = self.cursor.fetchall()

                        # On écrit les données dans la feuille Excel
                        if data_from_database:
                            print(f"Données de la deuxième base de données ({resource}): {data_from_database}")
                            row_index = 15
                            for intervenant in data_from_database:
                                worksheet.cell(row=row_index, column=1, value=intervenant[0])
                                row_index += 1

                        # On récupère les noms Intervenant ayant un chiffre dans la colonne TD pour afficher qui fait les TD et combien chaque personne a de groupe
                        self.cursor.execute(
                            "SELECT Intervenant, TD FROM RecupHProf WHERE ressource = ? AND Intervenant IS NOT NULL  AND TD IS NOT NULL ",
                            (resource,))
                        data_from_database = self.cursor.fetchall()

                                # On écrit les données dans la feuille Excel
                        if data_from_database:
                            print(
                                f"Données des TD de la deuxième base de données ({resource}): {data_from_database}")
                            row_index = 18
                            for intervenant in data_from_database:
                                worksheet.cell(row=row_index, column=1, value=intervenant[0])
                                worksheet.cell(row=row_index, column=2, value=intervenant[1])
                                row_index += 1

                        # On récupère les noms des intervenants ayant un chiffre dans la colonne Tp_dedoubles pour les afficher
                        self.cursor.execute(
                            "SELECT Intervenant, TP_dedoubles FROM RecupHProf WHERE ressource = ? AND Intervenant IS NOT NULL  AND TP_dedoubles IS NOT NULL ",
                            (resource,))
                        data_from_database = self.cursor.fetchall()

                        # On écrit les données dans la feuille Excel
                        if data_from_database:
                            print(
                                f"Données des TD de la deuxième base de données ({resource}): {data_from_database}")
                            row_index = 23
                            for intervenant in data_from_database:
                                worksheet.cell(row=row_index, column=1, value=intervenant[0])
                                worksheet.cell(row=row_index, column=2, value=intervenant[1])
                                row_index += 1

                        # On récupère les noms des intervenants ayant un chiffre dans la colonne Tp_non_dedoubles pour les afficher
                        self.cursor.execute(
                            "SELECT Intervenant, TP_non_dedoubles FROM RecupHProf WHERE ressource = ? AND Intervenant IS NOT NULL  AND TP_non_dedoubles IS NOT NULL ",
                            (resource,))
                        data_from_database = self.cursor.fetchall()

                        # On écrit les données dans la feuille Excel
                        if data_from_database:
                            print(
                                f"Données des TD de la deuxième base de données ({resource}): {data_from_database}")
                            row_index = 28
                            for intervenant in data_from_database:
                                worksheet.cell(row=row_index, column=1, value=intervenant[0])
                                worksheet.cell(row=row_index, column=2, value=intervenant[1])
                                row_index += 1




            filename = f"{semestre}.xlsx"
            save_directory = 'fichiers genere'
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            save_path = os.path.join(save_directory, filename)
            # Sauvegarde du fichier Excel
            fichier_vierge.save(save_path)
            print(f"Les données ont été ajoutées à {save_path}")

        except sqlite3.Error as e:
            print(f"Erreur lors de la connexion à la base de données : {e}")

# appel de la méthode
scribeData = ScribeData()
scribeData.scribeRessource("S1")
