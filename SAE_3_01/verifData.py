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
        self.fichierErreur = f"rapport d'erreur du {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.txt"

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
                        print("erreur cm pour le semestre {semestre}")
                        rapport += f"Les heures de CM de la ressource {maquette[3]} ne correspondent pas entre le fichier de la maquette et celui du planning. Il y a {planning[2]} heures de CM sur le fichier planning et {maquette[4]} heures de CM sur le fichier maquette national\n"
                    if planning[3] != maquette[5]:
                        print("erreur td pour le semestre {semestre}")
                        rapport += f"Les heures de T.D de la ressource {maquette[3]} ne correspondent pas entre le fichier de la maquette et celui du planning. Il y a {planning[3]} heures de TD sur le fichier planning et {maquette[5]} heures de TD sur le fichier maquette national\n"
                    if planning[4] != maquette[6]:
                        print(f"erreur tp pour le semestre {semestre}")
                        rapport += f"Les heures de T.P de la ressource {maquette[3]} ne correspondent pas entre le fichier de la maquette et celui du planning. Il y a {planning[4]} heures de TP sur le fichier planning et {maquette[6]} heures de TP sur le fichier maquette national\n"

                    if rapport:
                        # Écriture de l'erreur dans un fichier de rapport
                        with open(self.fichierErreur, "a") as rapport_erreur:
                            rapport_erreur.write(f"erreur pour le semestre {semestre}\n")
                            rapport_erreur.write(rapport)
                            rapport_erreur.write("\n")

                    if planning[2] == maquette[4] and planning[3] == maquette[5] and planning[4] == maquette[6]:
                        print(f"pas d'erreur pour le semestre {semestre}")
