import glob
import os
import openpyxl
import pandas as pd
from openpyxl.workbook import Workbook
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from collections import defaultdict

# Connexion à la base de données
db_url = 'sqlite:///database/database.db'
table_name = 'Prof'

# Paramètres de l'e-mail
email_host = 'smtp.gmail.com'
email_port = 587
email_user = 'rugierotymeo@gmail.com'
email_password = 'igtd loyc dyff suxj'

def check_db_connection():
    try:
        engine = create_engine(db_url)
        with engine.connect() as connection:
            return True
    except SQLAlchemyError as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return False

def fetch_prof_email(prof_name, engine):
    try:
        sql_query = f"SELECT MailProf FROM {table_name} WHERE NomProf = '{prof_name}'"
        df = pd.read_sql(sql_query, engine)
        if not df.empty:
            return df.iloc[0]['MailProf']
        else:
            print(f"Aucun e-mail trouvé pour {prof_name}")
            return None
    except Exception as e:
        print(f"Une erreur est survenue lors de la récupération de l'email : {e}")
        return None

def send_email(server, receiver_email, file_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = receiver_email
        msg['Subject'] = 'Votre fichier Excel'

        part = MIMEBase('application', "octet-stream")
        with open(file_path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
        msg.attach(part)

        server.send_message(msg)
        print(f"Email envoyé à {receiver_email}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

def save_sheet_to_new_file(original_file_path, sheet_name, new_file_path):
    wb = openpyxl.load_workbook(original_file_path)
    original_sheet = wb[sheet_name]

    new_wb = Workbook()
    new_sheet = new_wb.active
    new_sheet.title = sheet_name

    for row in original_sheet.iter_rows(values_only=True):
        new_sheet.append(row)

    new_wb.save(new_file_path)

def process_excel_files(file_paths, directory="fichiers genere mail"):  # Modification ici
    if not check_db_connection():
        print("Impossible de se connecter à la base de données. Vérifiez la configuration.")
        return

    engine = create_engine(db_url)
    prof_sheets = defaultdict(list)

    for file_path in file_paths:
        wb = openpyxl.load_workbook(file_path)
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            prof_name = sheet['G2'].value
            if prof_name:
                prof_sheets[prof_name].append((wb, sheet_name))

    for prof_name, sheets in prof_sheets.items():
        new_wb = Workbook()
        new_wb.remove(new_wb.active)
        for wb, sheet_name in sheets:
            original_sheet = wb[sheet_name]
            new_sheet = new_wb.create_sheet(title=sheet_name)
            for row in original_sheet.iter_rows(values_only=True):
                new_sheet.append(row)

        new_file_name = f"{prof_name.replace(' ', '_')}_sheets.xlsx"
        new_file_path = os.path.join(directory, new_file_name)
        new_wb.save(new_file_path)

        receiver_email = fetch_prof_email(prof_name, engine)
        if receiver_email:
            with smtplib.SMTP(email_host, email_port) as server:
                server.starttls()
                server.login(email_user, email_password)
                send_email(server, receiver_email, new_file_path)
        else:
            print(f"Email non trouvé pour {prof_name}")

def find_excel_files(directory):
    return glob.glob(f"{directory}/*.xlsx")

excel_files = find_excel_files('fichiers genere')

process_excel_files(excel_files)
