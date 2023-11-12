import math
import pandas as pd
import sqlite3
from database_handler import *

conn = sqlite3.connect('../database/database.db')
cursor = conn.cursor()

# Ouvre le fichier en mode lecture
with open("../Documents/NomProf.txt", "r") as fichier:
    # Lire chaque ligne du fichier
    for ligne in fichier:
        # Divise la ligne en utilisant le signe "=" comme séparateur
        parties = ligne.strip().split("=")
        # parties[0] = acronyme | parties[1] = Nom du prof
        # Vérifie si la ligne a été correctement divisée en deux parties
        if len(parties) == 2:
            resultat_requete = cursor.execute("SELECT Acronyme, NomProf FROM PROF WHERE Acronyme = ?",
                                                (parties[0],)).fetchall()
            # Vérifie si la requête a renvoyé des résultats
            if resultat_requete:
                # On update le nom du prof
                cursor.execute("UPDATE PROF SET NomProf = ? WHERE Acronyme = ?", (parties[1], parties[0]))
                conn.commit()

            else:
                # On insère le nouveau prof
                cursor.execute(
                    "INSERT INTO Prof (Acronyme, NomProf) VALUES (?, ?)",
                    (parties[0], parties[1],))
                # sauvegarder dans la base de données
                conn.commit()
        else:
            print(f"Erreur de format sur la ligne : {ligne}")
