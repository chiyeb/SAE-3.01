import sqlite3
import openpyxl as openpyxl
import os
import pandas as pd
from datetime import datetime

from insertData import insertData


class scribeData:
    """
    Classe qui permet d'écrire les données dans des fichiers
    """
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(scribeData, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def _setup(self):
        """
        "Setup" l'objet : initialise la connexion à la BD
        :return:
        """
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()

    def clean_sheet_title(self, title):
        """
        Nettoie le titre de la feuille Excel en supprimant ou remplaçant les caractères spéciaux.
        Les caractères spéciaux non autorisés dans Excel sont : \, /, ?, *, [, ] et :
        Remplace ces caractères par un espace et tronque le titre à 31 caractères si nécessaire.
        """
        # Remplace les caractères spéciaux par un espace
        for char in ['\\', '/', '?', '*', '[', ']', ':']:
            title = title.replace(char, ' ')

        # Tronquer à 31 caractères si nécessaire
        return title[:31]

    def scribeRessource(self, semestre):
        """
        Fonction qui écrit les informations de chaque ressources, dans le fichier final
        :param semestre:
        :return:
        """
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

                    cleaned_resource = self.clean_sheet_title(resource)

                    # Création d'une nouvelle feuille Excel avec le nom de la ressource nettoyé
                    worksheet = fichier_vierge.copy_worksheet(base_sheet)
                    worksheet.title = cleaned_resource

                    # On récupère des données de la base de données (Planning)
                    self.cursor.execute(
                        "SELECT Ressource, H_CM, H_TD, H_TP, COALESCE(Prof.NomProf, Planning.Resp) FROM Planning "
                        "LEFT JOIN Prof ON Planning.Resp = Prof.Acronyme "
                        "WHERE Ressource = ? AND Semestre = ?",
                        (resource, semester))
                    data_from_database = self.cursor.fetchall()

                    # On écrit les données de la base de données dans la nouvelle feuille Excel
                    if data_from_database:
                        print(f"Traitement des données ({resource}, {semester}): {data_from_database}")
                        worksheet.cell(row=5, column=2, value=data_from_database[0][1])
                        worksheet.cell(row=5, column=3, value=data_from_database[0][2])
                        worksheet.cell(row=5, column=4, value=data_from_database[0][3])
                        worksheet.cell(row=2, column=2, value=resource)
                        worksheet.cell(row=2, column=7, value=data_from_database[0][4])

                    # On récupère les données de la base de données HoraireProf
                    self.cursor.execute(
                        "SELECT Intervenant, TD, TP_Dedoubles,TP_Non_Dedoubles FROM HoraireProf WHERE ressource = ? "
                        "AND TD IS NOT NULL AND TP_dedoubles IS NOT NULL AND TP_non_dedoubles IS NOT NULL",
                        (resource,))
                    data_from_database = self.cursor.fetchall()

                    # On écrit les données dans la feuille Excel
                    if data_from_database:
                        print(f"Traitement des données ({resource}): {data_from_database}")

                        row_index0 = 8
                        row_index1 = 18
                        row_index2 = 23
                        row_index3 = 28

                        for intervenant in data_from_database:
                            # ceci permet d'écrire les intervenant
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

                    # On récupère les noms des intervenants ayant un chiffre dans la colonne CM pour afficher les
                    # profs qui font les CM
                    self.cursor.execute(
                        "SELECT Intervenant,CM FROM HoraireProf WHERE Ressource = ? AND CM IS NOT NULL",
                        (resource,))
                    data_from_database = self.cursor.fetchall()

                    # On écrit les données dans la feuille Excel
                    if data_from_database:
                        print(f"Traitement des données ({resource}): {data_from_database}")
                        row_index = 15
                        for intervenant in data_from_database:
                            worksheet.cell(row=row_index, column=1, value=intervenant[0])
                            row_index += 1

                    self.cursor.execute(
                        "SELECT Date_Cours, Type_Cours FROM Cours WHERE Semestre = ? AND ? LIKE Ressource || '%'",
                        (semester, resource))
                    data_from_database = self.cursor.fetchall()

                    if data_from_database:
                        print(
                            f"Données de la base de données Cours ({resource}, {semester}): {data_from_database}")
                        date_type_rows = {}
                        dict_date_cours = {}
                        for i, cours_actuel in enumerate(data_from_database):
                            date_actuelle = cours_actuel[0]
                            type_cours = cours_actuel[1]
                            if date_actuelle in dict_date_cours:
                                dict_date_cours[date_actuelle].append(type_cours)
                            # Ajouter le type de cours à la liste s'il n'est pas déjà présent
                            if type_cours not in dict_date_cours.get(date_actuelle, []):
                                dict_date_cours.setdefault(date_actuelle, []).append(type_cours)
                            # Parcourir les éléments suivants pour vérifier les doublons
                        print(dict_date_cours)
                        for cle, types_cours in dict_date_cours.items():
                            # Vérifier si la date a déjà été traitée
                            if cle not in date_type_rows:
                                # Si la date n'a pas encore été traitée, obtenir un nouvel index de ligne
                                row_index5 = max(date_type_rows.values(), default=34) + 1
                                date_type_rows[cle] = row_index5
                            else:
                                row_index5 = date_type_rows[cle]
                            # Écrire la date dans la première colonne de la ligne identifiée
                            worksheet.cell(row=row_index5, column=1, value=cle)
                            t_cours_traite = {}
                            for type_cours in types_cours:
                                # Vérifie si le type de cours existe déjà dans le dictionnaire
                                if type_cours in t_cours_traite:
                                    # Augmente le compteur existant pour ce type de cours
                                    t_cours_traite[type_cours] += 2
                                else:
                                    # Initialise le compteur pour ce type de cours
                                    t_cours_traite[type_cours] = 2
                            for type_cours in set(types_cours):
                                # Concaténer le type de cours avec son compteur
                                type_cours_et_nombre = f"{type_cours} {t_cours_traite[type_cours]}H"

                                # Choix du column_index en fonction du type de cours
                                if type_cours == 'Amphi':
                                    column_index = 2
                                elif type_cours == 'TD':
                                    column_index = 3
                                elif type_cours == 'TP':
                                    column_index = 4
                                else:
                                    continue  # Si le type de cours n'est pas reconnu on passe au suivant

                                # Écrire les données dans la feuille Excel
                                worksheet.cell(row=row_index5, column=column_index, value=type_cours_et_nombre)

                    # On récupère les données de la base de données Planning pour multiplier les valeurs de HorraireProf
                    self.cursor.execute(
                        "SELECT H_CM, H_TD, H_TP FROM Planning WHERE ressource = ?",
                        (resource,))
                    multiplication_values = self.cursor.fetchone()

                    if multiplication_values:
                        print(f"Traitement des données Planning ({resource}): {multiplication_values}")

                    # On récupère les données de la base de données HoraireProf
                    self.cursor.execute(
                        "SELECT Intervenant, CM, TD, TP_Dedoubles, TP_Non_Dedoubles, Test FROM HoraireProf WHERE ressource = ?",
                        (resource,))
                    data_from_database = self.cursor.fetchall()

                    # On écrit les données dans la feuille Excel
                    if data_from_database:
                        print(f"Traitement des données GroupeProf ({resource}): {data_from_database}")

                    row_index0 = 56
                    row_index1 = 56
                    row_index2 = 56
                    row_index3 = 56
                    row_index4 = 56
                    row_index5 = 56

                    for intervenant in data_from_database:

                        # ceci permet d'écrire les intervenant
                        worksheet.cell(row=row_index0, column=1, value=intervenant[0])
                        row_index0 += 1
                        if intervenant[1] is not None:
                            worksheet.cell(row=row_index1, column=12, value=intervenant[1] * multiplication_values[0])
                        row_index1 += 1

                        # ceci permet d'écrire le nombre de TD
                        if intervenant[2] is not None:
                            worksheet.cell(row=row_index2, column=13, value=intervenant[2] * multiplication_values[1])
                        row_index2 += 1

                        # ceci permet d'écrire le nombre de TP dédoublés
                        if intervenant[3] is not None:
                            worksheet.cell(row=row_index3, column=14, value=intervenant[3] * multiplication_values[2])
                        row_index3 += 1

                        # ceci permet d'écrire le nombre de TP non dédoublés
                        if intervenant[4] is not None:
                            worksheet.cell(row=row_index4, column=15, value=intervenant[4] * multiplication_values[2])
                        row_index4 += 1

                        # ceci permet d'écrire le nombre de test
                        worksheet.cell(row=row_index5, column=16, value=intervenant[5])
                        row_index5 += 1

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

    def scribeHoraireTotalProf(self):
        """
        Fonction qui écrit les heures de chaque professeur pour chaque type de cours dans un fichier Excel.
        :return:
        """
        try:
            insertdata_instance = insertData()
            insertdata_instance.insertNombreHeureProf()
            # récupération du nombres d'heures de chaque profs
            self.cursor.execute("SELECT * FROM HoraireTotalProf")
            heures = self.cursor.fetchall()
            colones = [description[0] for description in self.cursor.description]
            excel = pd.DataFrame(heures, columns=colones)
            # calcul du nombre total d'heure pour chaque prof (somme de toutes les heures)
            excel['Total_Hours'] = excel[['H_CM', 'H_TD', 'H_TP_D', 'H_TP_ND', 'H_TEST']].sum(axis=1)
            # on renomme les colonnes du fichier excel
            excel.rename(columns={
                'Prof': 'Nom du prof',
                'H_CM': 'Nombre d\'heure de CM',
                'H_TD': 'Nombre d\'heure de TD',
                'H_TP_D': 'Nombre d\'heure de TP Dedoubles',
                'H_TP_ND': 'Nombre d\'heure de TP Non Dedoubles',
                'H_TEST': 'Nombre d\'heure de test',
                'Total_Hours': 'Nombre d\'heure total'
            }, inplace=True)

            dossier = 'fichiers genere'
            if not os.path.exists(dossier):
                os.makedirs(dossier)
            fichier = "Professeurs_Horaires.xlsx"
            lieu_enregistrement = os.path.join(dossier, fichier)
            excel.to_excel(lieu_enregistrement, index=False)
            print(f"Les données ont été écrites dans le fichier {lieu_enregistrement}")

        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des données : {e}")
