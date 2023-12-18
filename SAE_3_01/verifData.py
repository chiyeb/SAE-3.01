import sqlite3
import math
import pandas as pd


class verifData:
    def __init__(self):
        # Initialise la connexion à la base de données
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()

    def concordance(self, semestre):
        with open(f"rapport d'erreur.txt", "w") as rapport_erreur:
            rapport_erreur.write("Erreur pour le semestre" + semestre)
            rapport_erreur.write("\n")
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
                        print("cm")
                        rapport += f"Les heures de CM de la ressource {maquette[3]} ne correspondent pas entre le fichier de la maquette et celui du planning. Il y a {planning[2]} heures de CM sur le fichier planning et {maquette[4]} heures de CM sur le fichier maquette national\n"
                    if planning[3] != maquette[5]:
                        print("td")
                        rapport += f"Les heures de T.D de la ressource {maquette[3]} ne correspondent pas entre le fichier de la maquette et celui du planning. Il y a {planning[3]} heures de TD sur le fichier planning et {maquette[5]} heures de TD sur le fichier maquette national\n"
                    if planning[4] != maquette[6]:
                        print("tp")
                        rapport += f"Les heures de T.P de la ressource {maquette[3]} ne correspondent pas entre le fichier de la maquette et celui du planning. Il y a {planning[4]} heures de TP sur le fichier planning et {maquette[6]} heures de TP sur le fichier maquette national\n"

                    if rapport:
                        # Écriture de l'erreur dans un fichier de rapport
                        with open(f"rapport d'erreur.txt", "w") as rapport_erreur:
                            rapport_erreur.write(rapport)
                            rapport_erreur.write("\n")

                    if planning[2] == maquette[4] and planning[3] == maquette[5] and planning[4] == maquette[6]:
                        print("ok")

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
