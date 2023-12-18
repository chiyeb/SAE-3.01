import pandas as pd
import sqlite3

# Établir la connexion à la base de données (cela crée également le fichier de base de données s'il n'existe pas)
conn = sqlite3.connect('database/database.db')

# Créer un objet curseur pour exécuter des requêtes SQL
cursor = conn.cursor()

def extract_and_display_resource_info(df, conn):
    """
    Extraire, structurer et afficher les informations sur la ressource à partir du DataFrame.

    Args:
    df (DataFrame): Le DataFrame contenant les données de la feuille Excel.
    """
    structured_data = {}
    current_resource = None

    for _, row in df.iterrows():
        resource = row['Ressource']
        intervenant = row['Intervenants']
        cm = row['CM']
        td = row['TD']
        tp_non_dedoubles = row['TP (non dédoublés)']
        tp_dedoubles = row['TP (dédoublés)']
        test = row['Test']

        # Vérifier si une nouvelle ressource commence
        if pd.notna(resource):
            current_resource = resource
            structured_data[current_resource] = {}

        # Vérifier si la ligne contient des données d'intervenant
        if pd.notna(intervenant):
            if current_resource not in structured_data:
                structured_data[current_resource] = {}
            if intervenant not in structured_data[current_resource]:
                structured_data[current_resource][intervenant] = []

            structured_data[current_resource][intervenant].append({
                'CM': cm,
                'TD': td,
                'TP (non dédoublés)': tp_non_dedoubles,
                'TP (dédoublés)': tp_dedoubles,
                'Test': test
            })


    # Insérer ou mettre à jour les enregistrements dans la base de données
    for resource, intervenant_data in structured_data.items():
        if resource not in structured_data:
            structured_data[resource] = {None: [{}]}  # Insérer un enregistrement avec des valeurs nulles si la ressource n'est pas présente


        for intervenant, data_list in intervenant_data.items():
            print(f"Ressource: {resource} - Intervenant : {intervenant} ")


            if data_list:
                for d in data_list:
                    # Vérifier si l'enregistrement existe déjà dans la base de données
                    cursor.execute("SELECT * FROM RecupHProf WHERE Ressource = ? AND Intervenant = ?",
                                   (resource, intervenant))
                    existing_record = cursor.fetchone()

                    if existing_record:
                        # Mettre à jour l'enregistrement existant
                        cursor.execute(
                            "UPDATE RecupHProf SET CM = ?, TD = ?, TP_non_dedoubles = ?, TP_dedoubles = ?, Test = ? WHERE Ressource = ? AND Intervenant = ?",
                            (d['CM'], d['TD'], d['TP (non dédoublés)'], d['TP (dédoublés)'], d['Test'], resource,
                             intervenant))
                    else:
                        # Insérer un nouvel enregistrement
                        cursor.execute(
                            "INSERT INTO RecupHProf (Ressource, Intervenant, CM, TD, TP_non_dedoubles, TP_dedoubles, Test) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (resource, intervenant, d['CM'], d['TD'], d['TP (non dédoublés)'], d['TP (dédoublés)'],
                             d['Test']))

                    conn.commit()


                    print(f"    - CM : {d['CM']} heure" if pd.notna(d['CM']) else "    - CM : Non spécifié")
                    print(f"    - TD : {d['TD']} heure" if pd.notna(d['TD']) else "    - TD : Non spécifié")
                    print(f"    - TP (non dédoublés) : {d['TP (non dédoublés)']} heure" if pd.notna(
                        d['TP (non dédoublés)']) else "    - TP (non dédoublés) : Non spécifié")
                    print(f"    - TP (dédoublés) : {d['TP (dédoublés)']} heure" if pd.notna(
                        d['TP (dédoublés)']) else "    - TP (dédoublés) : Non spécifié")
                    print(f"    - Test : {d['Test']} heure" if pd.notna(d['Test']) else "    - Test : Non spécifié")
            else:
                print("Aucune donnée")
                print("\n")







# Charger le fichier Excel
chemin_fichier = 'QuiFaitQuoi_beta.xlsx'
donnees_excel = pd.ExcelFile(chemin_fichier)

# Afficher les noms des feuilles et les premières lignes de chaque feuille pour comprendre la structure
noms_feuilles = donnees_excel.sheet_names
apercus_feuilles = {}

for feuille in noms_feuilles:
    df = pd.read_excel(chemin_fichier, sheet_name=feuille)
    apercus_feuilles[feuille] = df.head()
df_s1 = pd.read_excel(chemin_fichier, sheet_name=noms_feuilles[0])

# Extraire et afficher les informations sur la ressource
extract_and_display_resource_info(df_s1, conn)
