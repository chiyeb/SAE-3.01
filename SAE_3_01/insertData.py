import sqlite3
import math
import pandas as pd

class insertData:
    def __init__(self, db_file):
        # Initialise la connexion à la base de données
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()
    def insert_maquette(self, Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP):
        # création d'un id unique pour chaque semestre par ressource
        id_res_formation = Semestre + Code_ressource
        espace = Libelle.index(" ")
        # récupération de seulement le numéro de la ressource sans le nom de la ressource
        num_ressource = Libelle[:espace]
        # éxécution de la requête SQL pour vérifier si il existe déjà dans la BD la ressource pour un semestre précis
        self.conn.execute("SELECT id_res_formation FROM Maquette WHERE id_res_formation = ?", (id_res_formation,))
        existing_row = self.cursor.fetchone()
        # si la requête renvoie quelque chose on update au lieu d'insérer
        if existing_row:
            self.cursor.execute(
                "UPDATE Maquette SET Semestre = ?, Libelle = ?, H_CM = ?, H_TD = ?, H_TP = ?, Num_Res = ? WHERE Code_ressource = ?",
                (Semestre, Libelle, H_CM, H_TD, H_TP, num_ressource, Code_ressource)
            )
            self.conn.commit()
        # sinon on insère au lieu d'update
        else:
            self.cursor.execute(
                "INSERT INTO Maquette (id_res_formation, Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP, Num_Res) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (id_res_formation, Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP, num_ressource))
            # commit les changements pour les sauvegarder dans la base de données
            self.conn.commit()

    def insert_planning(self, Semestre, Ressource, H_CM, H_TD, H_TP, Resp):
        # éxécution de la requête SQL pour vérifier si il existe déjà dans la BD la ressource pour un semestre précis
        self.cursor.execute("SELECT Semestre FROM Planning WHERE Semestre = ? AND Ressource = ?",
                            (Semestre, Ressource,))
        existing_row = self.cursor.fetchone()
        # si la requête renvoie quelque chose on update au lieu d'insérer
        if existing_row:
            self.cursor.execute(
                "UPDATE Planning SET H_CM = ?, H_TD = ?, H_TP = ?, Resp = ? WHERE Semestre = ? AND Ressource = ?",
                (H_CM, H_TD, H_TP, Resp, Semestre, Ressource)
            )
        # sinon on insère au lieu d'update
        else:
            self.cursor.execute(
                "INSERT INTO Planning (Semestre, Ressource, H_CM, H_TD, H_TP, Resp) VALUES (?, ?, ?, ?, ?, ?)",
                (Semestre, Ressource, H_CM, H_TD, H_TP, Resp))
            # commit les changements pour les sauvegarder dans la base de données
        self.conn.commit()