import sqlite3
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from selectFile import selectFile


class ecriture_val:
    instance = None
    files = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(ecriture_val, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def _setup(self):
        self.files = selectFile()
        # Initialise la connexion à la base de données
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()

    def write_data_to_excel(self, excel_file_path):
        # Charger le classeur Excel existant
        wb = load_workbook(excel_file_path)
        worksheet = wb.active

        # Récupérer les données à partir de la base de données
        self.cursor.execute("SELECT Ressources, Prof, H_CM, H_TD, H_TP, Test FROM FichiersGenere")
        data_from_database = self.cursor.fetchall()

        if data_from_database:
            print(f"Traitement des données: {data_from_database}")

            # Déterminer le nombre de colonnes dans la base de données
            num_columns = len(data_from_database[0])

            for row_index, row_data in enumerate(data_from_database, start=2):
                for col_index, cell_data in enumerate(row_data, start=1):
                    cell_data = "" if cell_data is None else cell_data
                    # Écrire uniquement dans les colonnes correspondant aux données de la base de données
                    if col_index <= num_columns:
                        worksheet.cell(row=row_index, column=col_index, value=cell_data)

                    # Calculer la somme des valeurs H_CM, H_TD et H_TP et les écrire dans la colonne 7
                    if col_index == 6:
                        h_cm = row_data[2] if row_data[2] else 0
                        h_td = row_data[3] if row_data[3] else 0
                        h_tp = row_data[4] if row_data[4] else 0
                        total_hours = h_cm + h_td + h_tp
                        worksheet.cell(row=row_index, column=7, value=total_hours)

        # Sauvegarder le fichier Excel
        wb.save(excel_file_path)

Ecriture_val = ecriture_val()
Ecriture_val.write_data_to_excel("fichiers genere/Professeurs_Horaires.xlsx")
