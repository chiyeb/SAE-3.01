import sqlite3
from openpyxl import load_workbook
from openpyxl.styles import Border, Side
from selectFile import selectFile

class ecriture_val:
    instance = None
    files = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(ecriture_val, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def __init__(self):
        # Définir les styles de bordure pour le tableau
        self.thick_border = Border(left=Side(style='thick'),
                                   right=Side(style='thick'),
                                   top=Side(style='thick'),
                                   bottom=Side(style='thick'))
        self.thin_border = Border(left=Side(style='thin'),
                                  right=Side(style='thin'),
                                  top=Side(style='thin'),
                                  bottom=Side(style='thin'))

    def _setup(self):
        self.files = selectFile()
        # Initialise la connexion à la base de données
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()

    def write_data_to_excel(self, excel_file_path):
        # Charger le classeur Excel existant
        wb = load_workbook(excel_file_path)
        worksheet = wb.active

        # Vérifier si le fichier Excel est vide
        is_empty = worksheet.max_row == 1 and worksheet.max_column == 1

        # Supprimer le contenu existant du fichier Excel
        if not is_empty:
            worksheet.delete_rows(2, worksheet.max_row)

        # Récupérer les données à partir de la base de données
        self.cursor.execute("SELECT Prof, Ressources, H_CM, H_TD, H_TP, Test FROM FichiersGenere")
        data_from_database = self.cursor.fetchall()

        if data_from_database:
            print(f"Traitement des données: {data_from_database}")

            # Déterminer le nombre de colonnes dans la base de données
            num_columns = len(data_from_database[0])

            last_prof = None  # Pour suivre le dernier professeur ajouté
            row_index = 2 if is_empty else worksheet.max_row + 1  # Commencer à la deuxième ligne ou à la ligne suivante

            for row_data in data_from_database:
                current_prof = row_data[0]

                if current_prof != last_prof:
                    # Insérer une ligne vide si le professeur actuel est différent du dernier professeur ajouté
                    if not is_empty:
                        worksheet.insert_rows(row_index)
                    last_prof = current_prof
                    row_index += 2 # Avancer à la nouvelle ligne insérée

                # Écrire les données dans les colonnes correspondantes et appliquer les styles de bordure
                for col_index, cell_data in enumerate(row_data, start=1):
                    cell_data = "" if cell_data is None else cell_data
                    cell = worksheet.cell(row=row_index, column=col_index, value=cell_data)
                    cell.border = self.thin_border  # Appliquer une bordure fine à toutes les cellules

                # Appliquer une bordure épaisse à la première ligne du groupe de professeurs
                if current_prof != last_prof:
                    for col in worksheet.iter_cols(min_col=1, max_col=num_columns, min_row=row_index,
                                                   max_row=row_index):
                        for cell in col:
                            cell.border = self.thick_border

                # Calculer la somme des valeurs H_CM, H_TD et H_TP et les écrire dans la colonne 7
                h_cm = row_data[2] if row_data[2] else 0
                h_td = row_data[3] if row_data[3] else 0
                h_tp = row_data[4] if row_data[4] else 0
                total_hours = h_cm + h_td + h_tp
                worksheet.cell(row=row_index, column=num_columns + 1, value=total_hours).border = self.thin_border

                # Appliquer une bordure fine à la colonne supplémentaire pour la continuité de la ligne

                row_index += 1  # Avancer à la ligne suivante

            # Sauvegarder le fichier Excel
            wb.save(excel_file_path)


Ecriture_val = ecriture_val()
Ecriture_val.write_data_to_excel("fichiers genere/Professeurs_Horaires.xlsx")
