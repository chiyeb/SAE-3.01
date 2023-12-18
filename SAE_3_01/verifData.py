import os
import sqlite3
import math
from datetime import datetime

import pandas as pd


class verifData:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(verifData, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def _setup(self):
        # Initialise la connexion à la base de données
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()
        # Création du dossier "rapport d'erreurs"
        folder_path = "rapport d'erreurs"
        os.makedirs(folder_path, exist_ok=True)
        # Mettre le fichier dans le dossier "rapport d'erreurs"
        self.fichierErreur = os.path.join(
            folder_path, f"rapport d'erreur du {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.txt"
        )

    def concordance(self, semestre):
        print("Concordance pour le", semestre, ":")
        self.cursor.execute("SELECT * FROM Maquette WHERE Semestre = ?", (semestre,))
        rslt_maquette = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM Planning WHERE Semestre = ?", (semestre,))
        rslt_planning = self.cursor.fetchall()
        cpt = 0
        for maquette in rslt_maquette:
            for planning in rslt_planning:
                rapport = ""
                if not (planning[1] in maquette[3]):
                    rapport += f"La ressource {maquette[1]} n'existe pas ou n'a pas été placée au bon endroit.\n"
                else:
                    if planning[2] != maquette[4]:
                        print(f"erreur cm pour le semestre {semestre} et la ressource {maquette[3]}")
                        rapport += (f"Les heures de CM de la ressource {maquette[3]} ne correspondent pas entre le "
                                    f"fichier de la maquette et celui du planning. Il y a {planning[2]} heures de CM "
                                    f"sur le fichier planning et {maquette[4]} heures de CM sur le fichier maquette "
                                    f"national\n")
                    if planning[3] != maquette[5]:
                        print("erreur td pour le semestre {semestre} et la ressource {maquette[3]}")
                        rapport += (f"Les heures de T.D de la ressource {maquette[3]} ne correspondent pas entre le "
                                    f"fichier de la maquette et celui du planning. Il y a {planning[3]} heures de TD "
                                    f"sur le fichier planning et {maquette[5]} heures de TD sur le fichier maquette "
                                    f"national\n")
                    if planning[4] != maquette[6]:
                        print(f"erreur tp pour le semestre {semestre} et la ressource {maquette[3]}")
                        rapport += (f"Les heures de T.P de la ressource {maquette[3]} ne correspondent pas entre le "
                                    f"fichier de la maquette et celui du planning. Il y a {planning[4]} heures de TP "
                                    f"sur le fichier planning et {maquette[6]} heures de TP sur le fichier maquette "
                                    f"national\n")

                    if rapport:
                        # Écriture de l'erreur dans un fichier de rapport
                        with open(self.fichierErreur, "a") as rapport_erreur:
                            rapport_erreur.write(f"erreur pour le semestre {semestre} et la ressource {maquette[3]}\n")
                            rapport_erreur.write(rapport)
                            rapport_erreur.write("\n")

                    if planning[2] == maquette[4] and planning[3] == maquette[5] and planning[4] == maquette[6]:
                        print(f"pas d'erreur pour le semestre {semestre}")
    
    
    def concordancePlanning(self, semestre):
        with open(f"rapport d'erreur.txt", "w") as rapport_erreur:
            rapport_erreur.write("Erreur pour le semestre" + semestre + " dans le fichier planning")
            rapport_erreur.write("\n")
        print("Concordance pour le", semestre, ":")
        self.cursor.execute("SELECT * FROM Horaires WHERE Semestre = ?", (semestre,))
        rslt_horaires = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM Planning WHERE Semestre = ?", (semestre,))
        rslt_planning = self.cursor.fetchall()
        cpt = 0
        for horaires in rslt_horaires:
            for planning in rslt_planning:
                rapport = ""
                if not (planning[1] in horaires[1]):
                    rapport += f"La ressource {horaires[1]} n'existe pas ou n'a pas été placée au bon endroit.\n"
                else:
                    self.cursor.execute("SELECT nbCours FROM Horaires WHERE Semestre = ? AND Type_Cours = ?",
                                        (semestre, "Amphi"))
                    cmHoraire = self.cursor.fetchone()
                    if planning[2] != cmHoraire:
                        print("cm")
                        rapport += (f"Les heures de CM de la ressource {horaires[1]} ne correspondent pas entre les "
                                    f"heures écrite et les heures posé. Il y a {planning[2]} heures de CM écrites et "
                                    f"{cmHoraire} heures de CM posé\n")
                    self.cursor.execute("SELECT nbCours FROM Horaires WHERE Semestre = ? AND Type_Cours = ?",
                                        (semestre, "TD"))
                    tdHoraire = self.cursor.fetchone()
                    if planning[3] != tdHoraire:
                        print("td")
                        rapport += (f"Les heures de TD de la ressource {horaires[1]} ne correspondent pas entre les "
                                    f"heures écrite et les heures posé. Il y a {planning[2]} heures de CM écrites et "
                                    f"{tdHoraire} heures de TD posé\n")
                    self.cursor.execute("SELECT nbCours FROM Horaires WHERE Semestre = ? AND Type_Cours = ?",
                                        (semestre, "TP"))
                    tpHoraire = self.cursor.fetchone()
                    if planning[4] != tpHoraire:
                        print("tp")
                        rapport += (f"Les heures de TP de la ressource {horaires[1]} ne correspondent pas entre les "
                                    f"heures écrite et les heures posé. Il y a {planning[2]} heures de TP écrites et "
                                    f"{tpHoraire} heures de TP posé\n")

                    if rapport:
                        # Écriture de l'erreur dans un fichier de rapport
                        with open(f"rapport d'erreur.txt", "w") as rapport_erreur:
                            rapport_erreur.write(rapport)
                            rapport_erreur.write("\n")

                    if planning[2] == horaires[4] and planning[3] == horaires[5] and planning[4] == horaires[6]:
                        print("ok")
    def __del__(self):
        # Ferme la connexion à la base de données lorsque l'objet est détruit
        self.conn.close()