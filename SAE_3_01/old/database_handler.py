import sqlite3

# Initialiser la connexion à la base de donnée
conn = sqlite3.connect('../database/database.db')
cursor = conn.cursor()


def insert_maquette(Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP):
    # création d'un id unique pour chaque semestre par ressource
    id_res_formation = Semestre + Code_ressource
    espace = Libelle.index(" ")
    # récupération de seulement le numéro de la ressource sans le nom de la ressource
    num_ressource = Libelle[:espace]
    # éxécution de la requête SQL pour vérifier si il existe déjà dans la BD la ressource pour un semestre précis
    cursor.execute("SELECT id_res_formation FROM Maquette WHERE id_res_formation = ?", (id_res_formation,))
    existing_row = cursor.fetchone()
    # si la requête renvoie quelque chose on update au lieu d'insérer
    if existing_row:
        cursor.execute(
            "UPDATE Maquette SET Semestre = ?, Libelle = ?, H_CM = ?, H_TD = ?, H_TP = ?, Num_Res = ? WHERE Code_ressource = ?",
            (Semestre, Libelle, H_CM, H_TD, H_TP, num_ressource, Code_ressource)
        )
        conn.commit()
    # sinon on insère au lieu d'update
    else:
        cursor.execute(
            "INSERT INTO Maquette (id_res_formation, Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP, Num_Res) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (id_res_formation, Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP, num_ressource))
        # commit les changements pour les sauvegarder dans la base de données
        conn.commit()


def insert_planning(Semestre, Ressource, H_CM, H_TD, H_TP, Resp):
    # éxécution de la requête SQL pour vérifier si il existe déjà dans la BD la ressource pour un semestre précis
    cursor.execute("SELECT Semestre FROM Planning WHERE Semestre = ? AND Ressource = ?", (Semestre, Ressource,))
    existing_row = cursor.fetchone()
    # si la requête renvoie quelque chose on update au lieu d'insérer
    if existing_row:
        cursor.execute(
            "UPDATE Planning SET H_CM = ?, H_TD = ?, H_TP = ?, Resp = ? WHERE Semestre = ? AND Ressource = ?",
            (H_CM, H_TD, H_TP, Resp, Semestre, Ressource)
        )
    # sinon on insère au lieu d'update
    else:
        cursor.execute("INSERT INTO Planning (Semestre, Ressource, H_CM, H_TD, H_TP, Resp) VALUES (?, ?, ?, ?, ?, ?)",
            (Semestre, Ressource, H_CM, H_TD, H_TP, Resp))
        # commit les changements pour les sauvegarder dans la base de données
    conn.commit()
