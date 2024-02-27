import openpyxl
import pandas as pd
import smtplib

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Connexion à la base de données
db_url = 'sqlite:///database/database.db'
table_name = 'Prof'

# Paramètres de l'e-mail
email_host = 'smtp.gmail.com'
email_port = 587
email_user = 'rugierotymeo@gmail.com'
email_password = 'igtd loyc dyff suxj'

# Vérifier la connexion à la base de données
def check_db_connection():
    try:
        engine = create_engine(db_url)
        # Tentative de connexion à la base de données
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
        part.add_header('Content-Disposition', f'attachment; filename="{file_path.split("/")[-1]}"')
        msg.attach(part)

        server.send_message(msg)
        print(f"Email envoyé à {receiver_email}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

def process_excel_files(file_paths):
    if check_db_connection():
        engine = create_engine(db_url)
        server = smtplib.SMTP(email_host, email_port)
        server.starttls()
        server.login(email_user, email_password)
        try:
            for file_path in file_paths:
                wb = openpyxl.load_workbook(file_path)
                for sheet_name in wb.sheetnames:
                    sheet = wb[sheet_name]
                    prof_name = sheet['G2'].value
                    receiver_email = fetch_prof_email(prof_name, engine)
                    if receiver_email:
                        send_email(server, receiver_email, file_path)
                    else:
                        print(f"Email non trouvé pour {prof_name}")
        finally:
            server.quit()
    else:
        print("Impossible de se connecter à la base de données. Vérifiez la configuration.")

excel_files = ['fichiers genere/S1.xlsx', 'fichiers genere/S2.xlsx']
process_excel_files(excel_files)
