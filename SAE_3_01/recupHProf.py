import pandas as pd
from sqlalchemy import create_engine


def Heures_ressources(df):
    """
    Extract, structure, and display the resource information from the DataFrame.

    Args:
    df (DataFrame): The DataFrame containing the Excel sheet data.
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

        if pd.notna(resource):
            current_resource = resource
            structured_data[current_resource] = []

        if pd.notna(intervenant):
            structured_data[current_resource].append({
                'Intervenant': intervenant,
                'CM': cm,
                'TD': td,
                'TP (non dédoublés)': tp_non_dedoubles,
                'TP (dédoublés)': tp_dedoubles,
                'Test': test
            })

    return structured_data


def create_db_connection():
    # SQLite database file
    db_file = 'database.db'

    # Creating a SQLite database engine
    engine = create_engine(f'sqlite:///{db_file}')

    # Returning the database engine
    return engine


def insert_data_into_db(engine, structured_data):
    # Establishing a database connection
    connection = engine.connect()

    # Iterating through the structured data and inserting into the database
    for resource, data in structured_data.items():
        for d in data:
            connection.execute('''
                INSERT INTO HeureRessource (NomRessource, NomIntervenants, hTD, hTP, hCM, hTEST)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                resource,
                d['Intervenant'],
                d['CM'],
                d['TD'],
                d['TP (non dédoublés)'],
                d['TP (dédoublés)'],
                d['Test']
            ))

    # Closing the database connection
    connection.close()


file_path = 'QuiFaitQuoi_beta.xlsx'
excel_data = pd.ExcelFile(file_path)

sheet_names = excel_data.sheet_names
structured_data = {}

for sheet in sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)
    structured_data.update(Heures_ressources(df))

# Creating a database connection
engine = create_db_connection()

# Inserting data into the 'resources' table
insert_data_into_db(engine, structured_data)
