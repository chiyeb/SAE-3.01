import openpyxl
import pandas as pd
import smtplib
from sqlalchemy import create_engine
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Paramètres de la base de données
db_url = 'sqlite:///Documents/GitHub/SAE-3.01/SAE_3_01/database/database.db'
table_name = 'Prof'

# Paramètres de l'e-mail
email_host = 'smtp.gmail.com'
email_port = 587
email_user = 'rugierotymeo@gmail.com'
email_password = 'Tym0302San1005'

def fetch_prof_email(prof_name):
    # Création de l'engine SQL
    engine = create_engine(db_url)
    # Utiliser pandas pour récupérer l'adresse e-mail du professeur
    sql_query = f"SELECT MailProf FROM {table_name} WHERE NomProf = '{prof_name}'"
    df = pd.read_sql(sql_query, engine)
    return df.iloc[0]['MailProf'] if not df.empty else None

def send_email(receiver_email, file_path):
    # Configuration du serveur SMTP
    server = smtplib.SMTP(email_host, email_port)
    server.starttls()
    server.login(email_user, email_password)

    # Création du message
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = receiver_email
    msg['Subject'] = 'Votre fichier Excel'

    # Ajout du fichier Excel
    part = MIMEBase('application', "octet-stream")
    with open(file_path, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(file_path.split('/')[-1]))
    msg.attach(part)

    # Envoi de l'e-mail
    server.send_message(msg)
    server.quit()

def process_excel_files(file_paths):
    for file_path in file_paths:
        wb = openpyxl.load_workbook(file_path)
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            prof_name = sheet['G2'].value
            receiver_email = fetch_prof_email(prof_name)
            if receiver_email:
                send_email(receiver_email, file_path)
            else:
                print(f"Email non trouvé pour {prof_name}")

# Liste des chemins vers les fichiers Excel à traiter
excel_files = ['fichiers genere/S1.xlsx', 'fichiers genere/S2.xlsx']

process_excel_files(excel_files)
