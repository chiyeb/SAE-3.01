import sqlite3
# Initialiser la connexion à la base de donnée
conn = sqlite3.connect('database/database.db')
cursor = conn.cursor()


def insert_maquette(Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP):
    id_res_formation = Semestre+Code_ressource
    espace = Libelle.index(" ")
    num_ressource = Libelle[:espace]
    print(num_ressource)
    cursor.execute("SELECT id_res_formation FROM Maquette WHERE id_res_formation = ?", (id_res_formation,))
    existing_row = cursor.fetchone()
    if existing_row:
        cursor.execute(
            "UPDATE Maquette SET Semestre = ?, Libelle = ?, H_CM = ?, H_TD = ?, H_TP = ?, Num_Res = ? WHERE Code_ressource = ?",
            (Semestre, Libelle, H_CM, H_TD, H_TP, num_ressource,Code_ressource)
        )
        conn.commit()
    else:
        cursor.execute(
            "INSERT INTO Maquette (id_res_formation, Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP, Num_Res) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (id_res_formation, Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP, num_ressource))
        # Commit les changements pour les sauvegarder dans la base de données
        conn.commit()

def insert_planning(Semestre, Ressource, H_CM, H_TD, H_TP, Resp):
    cursor.execute("SELECT Semestre FROM Planning WHERE Semestre = ? AND Ressource = ?", (Semestre, Ressource,))
    existing_row = cursor.fetchone()
    if existing_row:
        cursor.execute(
            "UPDATE Planning SET H_CM = ?, H_TD = ?, H_TP = ?, Resp = ? WHERE Semestre = ? AND Ressource = ?",
            (H_CM, H_TD, H_TP, Resp, Semestre, Ressource)
        )
    else:
        cursor.execute(
            "INSERT INTO Planning (Semestre, Ressource, H_CM, H_TD, H_TP, Resp) VALUES (?, ?, ?, ?, ?, ?)",
            (Semestre, Ressource, H_CM, H_TD, H_TP, Resp)
        )
        # Commit les changements pour les sauvegarder dans la base de données
    conn.commit()

