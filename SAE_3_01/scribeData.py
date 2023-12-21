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

                    # On récupère des données de la base de données (Planning)
                    self.cursor.execute(
                        "SELECT Ressource, H_CM, H_TD, H_TP, COALESCE(Prof.NomProf, Planning.Resp) FROM Planning "
                        "LEFT JOIN Prof ON Planning.Resp = Prof.Acronyme "
                        "WHERE Ressource = ? AND Semestre = ?",
                        (resource, semester))
                    data_from_database = self.cursor.fetchall()

                    # On écrit les données de la base de données dans la nouvelle feuille Excel
                    if data_from_database:
                        print(f"Données de la données ({resource}, {semester}): {data_from_database}")
                        worksheet.cell(row=5, column=2, value=data_from_database[0][1])
                        worksheet.cell(row=5, column=3, value=data_from_database[0][2])
                        worksheet.cell(row=5, column=4, value=data_from_database[0][3])
                        worksheet.cell(row=2, column=2, value=resource)
                        worksheet.cell(row=2, column=7, value=data_from_database[0][4])


                    # On récupère les données de la base de données HoraireProf
                    self.cursor.execute(
                        "SELECT Intervenant, TD, TP_Dedoubles,TP_Non_Dedoubles FROM HoraireProf WHERE ressource = ? AND TD IS NOT NULL AND TP_dedoubles IS NOT NULL AND TP_non_dedoubles IS NOT NULL",
                        (resource,))
                    data_from_database = self.cursor.fetchall()

                    # On écrit les données dans la feuille Excel
                    if data_from_database:
                        print(f"Données de la données ({resource}): {data_from_database}")

                        row_index0 = 8
                        row_index1 = 18
                        row_index2 = 23
                        row_index3 = 28

                        for intervenant in data_from_database:
                            #ceci permet d'écrire les intervenant
                            worksheet.cell(row=row_index0, column=1, value=intervenant[0])
                            row_index0 += 1
                            # ceci permet d'écrire les intervenant ainsi que leurs nombre de TD
                            worksheet.cell(row=row_index1, column=1, value=intervenant[0])
                            worksheet.cell(row=row_index1, column=2, value=intervenant[1])
                            row_index1 += 1
                            # ceci permet d'écrire les intervenant ainsi que leurs nombre de TD dédoublés
                            worksheet.cell(row=row_index2, column=1, value=intervenant[0])
                            worksheet.cell(row=row_index2, column=2, value=intervenant[2])
                            row_index2 += 1
                            # ceci permet d'écrire les intervenant ainsi que leurs nombre de TD non dédoublés
                            worksheet.cell(row=row_index3, column=1, value=intervenant[0])
                            worksheet.cell(row=row_index3, column=2, value=intervenant[3])
                            row_index3 += 1


                    # On récupère les noms des intervenants ayant un chiffre dans la colonne CM pour afficher les profs qui font les CM
                    self.cursor.execute(
                        "SELECT Intervenant,CM FROM HoraireProf WHERE Ressource = ? AND CM IS NOT NULL",
                        (resource,))
                    data_from_database = self.cursor.fetchall()

                    # On écrit les données dans la feuille Excel
                    if data_from_database:
                        print(f"Données de la données ({resource}): {data_from_database}")
                        row_index = 15
                        for intervenant in data_from_database:
                            worksheet.cell(row=row_index, column=1, value=intervenant[0])
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
