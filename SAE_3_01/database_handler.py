import sqlite3
# Initialiser la connexion à la base de donnée
conn = sqlite3.connect('database/database.db')
cursor = conn.cursor()


def insert(Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP):
    id_res_formation = Semestre+Code_ressource
    cursor.execute("SELECT id_res_formation FROM Maquette WHERE id_res_formation = ?", (id_res_formation,))
    existing_row = cursor.fetchone()
    if existing_row:
        cursor.execute(
            "UPDATE Maquette SET Libelle = ?, H_CM = ?, H_TD = ?, H_TP = ? WHERE Code_ressource = ?",
            (Libelle, H_CM, H_TD, H_TP, Code_ressource)
        )
    else:
        cursor.execute(
            "INSERT INTO Maquette (id_res_formation, Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (id_res_formation, Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP))
        # Commit les changements pour les sauvegarder dans la base de données
        conn.commit()



