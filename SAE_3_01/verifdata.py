import os
import sqlite3
from datetime import datetime


class VerifData:
    """
    Classe permettant de vérifier la concordance des données
    """
    instance = None
    fichier_erreur = None
    nb_erreur = 0
    nb_erreur_warning = 0
    fichier_warning = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(VerifData, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def _setup(self):
        """
        "Setup" l'objet : initialise la connexion à la BD, initialise le chemin du dossier "rapport d'erreurs"
        et créer le fichier rapports d'erreurs avec la date et l'heure exact de génération.
        :return:
        """
        # Initialise la connexion à la base de données
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()
        # Création du dossier "rapport d'erreurs"
        folder_path = "rapport d'erreurs"
        os.makedirs(folder_path, exist_ok=True)
        # Mettre les fichiers dans le dossier "rapport d'erreurs"
        self.fichier_erreur = os.path.join(
            folder_path, f"rapport d'erreur du {datetime.now().strftime('%Y-%m-%d %H:%M')}.txt"
        )
        self.fichier_warning = os.path.join(folder_path,
                                            f"rapport de warnings du {datetime.now().strftime('%Y-%m-%d %H:%M')}.txt")

    def concordance(self, semestre):
        """
        Fonction pour vérifier la concordance entre les données du fichier planning et maquette
        :param semestre:
        :return:
        """
        cursor_tmp = self.cursor
        conn_tmp = self.conn
        print("Concordance pour le", semestre, ":")
        cursor_tmp.execute("SELECT * FROM Maquette WHERE Semestre = ?", (semestre,))
        rslt_maquette = cursor_tmp.fetchall()
        cursor_tmp.execute("SELECT * FROM Planning WHERE Semestre = ?", (semestre,))
        rslt_planning = cursor_tmp.fetchall()
        for maquette in rslt_maquette:
            for planning in rslt_planning:
                rapport = ""
                rapport_warning = ""
                libelle = ""
                type_erreur = ""
                ressource = ""
                heure_planning = 0
                heure_maquette = 0
                commentaire = ""
                if not (planning[1] in maquette[3]):
                    rapport += f"La ressource {maquette[1]} n'existe pas ou n'a pas été placée au bon endroit.\n"
                else:

                    if planning[2] > maquette[4]:
                        print(f"erreur cm pour le semestre {semestre}")
                        rapport += (f"Erreur CM écrite dans le planning supérieur à celle prévu nationalement: \n"
                                    f"  -Ressource: {maquette[3]}\n "
                                    f"  -Heure planning: {planning[2]}\n"
                                    f"  -Heure maquette: {maquette[4]}\n")
                        libelle = "CM écrite dans le planning supérieur à celle prévu nationalement"
                        type_erreur = "Erreur"
                        ressource = maquette[3]
                        heure_planning = planning[2]
                        heure_maquette = maquette[4]
                    if planning[2] < maquette[4]:
                        print(f"Warning CM pour le semestre {semestre}")
                        rapport_warning += (f"Warning : Heures différentes entre le fichier planning et maquette\n"
                                            f"  -Ressource: {maquette[3]}\n"
                                            f"  -Heure planning: {planning[2]}\n"
                                            f"  -Heure maquette: {maquette[4]}\n")
                        libelle = "Heures différentes entre le fichier planning et maquette"
                        type_erreur = "Warning"
                        ressource = maquette[3]
                        heure_planning = planning[2]
                        heure_maquette = maquette[4]
                    if planning[3] > maquette[5]:
                        print(f"Erreur TD pour le semestre {semestre}")
                        rapport += (f"Erreur TD écrite dans le planning supérieur à celle prévu nationalement: \n"
                                    f"  -Ressource: {maquette[3]}\n"
                                    f"  -Heure planning: {planning[3]}\n"
                                    f"  -Heure maquette: {maquette[5]}\n")
                        libelle = "TD écrite dans le planning supérieur à celle prévu nationalement"
                        type_erreur = "Erreur"
                        ressource = maquette[3]
                        heure_planning = planning[3]
                        heure_maquette = maquette[5]
                    if planning[3] < maquette[5]:
                        print(f"Warning TD pour le semestre {semestre}")
                        rapport_warning += (f"Warning : Heures différentes entre le fichier planning et maquette\n"
                                            f"  -Ressource: {maquette[3]}\n"
                                            f"  -Heure planning: {planning[3]}\n"
                                            f"  -Heure maquette: {maquette[5]}\n")
                        libelle = "Heures différentes entre le fichier planning et maquette"
                        type_erreur = "Warning"
                        ressource = maquette[3]
                        heure_planning = planning[3]
                        heure_maquette = maquette[5]

                    if planning[4] > maquette[6]:
                        print(f"erreur TP pour le semestre {semestre}")
                        rapport += (f"Erreur TP écrite dans le planning supérieur à celle prévu nationalement: \n"
                                    f"  -Hessource: {maquette[3]} \n"
                                    f"  -Heure planning: {planning[4]} \n"
                                    f"  -Heure maquette: {maquette[6]}\n")
                        libelle = "TP écrite dans le planning supérieur à celle prévu nationalement"
                        type_erreur = "Erreur"
                        ressource = maquette[3]
                        heure_planning = planning[4]
                        heure_maquette = maquette[6]
                    if planning[4] < maquette[6]:
                        print(f"Warning Tp pour le semestre {semestre}")
                        rapport_warning += (f"Warning : Heures différentes entre le fichier planning et maquette\n"
                                            f"  -Ressource: {maquette[3]}\n"
                                            f"  -Heure planning: {planning[4]}\n"
                                            f"  -Heure maquette: {maquette[6]}\n")
                        libelle = "Heures différentes entre le fichier planning et maquette"
                        type_erreur = "Warning"
                        ressource = maquette[3]
                        heure_planning = planning[4]
                        heure_maquette = maquette[6]
                    if rapport and not self.is_deleted((type_erreur + semestre + ressource + str(heure_planning) + str(heure_maquette))):
                        # incrémentation du nombre d'erreur
                        self.nb_erreur += 1
                        if self.is_deleted((type_erreur + semestre + ressource + str(heure_planning) + str(heure_maquette))):
                            print("RESSOURCE :       " + ressource)
                            continue
                        self.insert_error(libelle, type_erreur, semestre, ressource, heure_planning, heure_maquette,
                                          commentaire)
                        # Écriture de l'erreur dans un fichier de rapport
                        with open(self.fichier_erreur, "a") as rapport_erreur:
                            rapport_erreur.write(rapport)
                            rapport_erreur.write("\n")
                    if rapport_warning and not self.is_deleted((type_erreur + semestre + ressource + str(heure_planning) + str(heure_maquette))):
                        # incrémentation du nombre d'erreurs
                        self.nb_erreur_warning += 1
                        if self.is_deleted((type_erreur + semestre + ressource + str(heure_planning) + str(heure_maquette))):
                            print("RESSOURCE :       " + ressource)
                            continue
                        self.insert_error(libelle, type_erreur, semestre, ressource, heure_planning, heure_maquette,
                                          commentaire)
                        # Écriture de l'erreur dans un fichier de rapport
                        with open(self.fichier_warning, "a") as rapport_warn:
                            rapport_warn.write(rapport_warning)
                            rapport_warn.write("\n")

                    if planning[2] == maquette[4] and planning[3] == maquette[5] and planning[4] == maquette[6]:
                        print(f"pas d'erreur pour le semestre {semestre}")

    def concordancePlanning(self, semestre):
        """
        Fonction qui vérifie la concordance entre les cours écrit(les heures) et posé dans le fichier planning
        :param semestre:
        :return:
        """
        cursor_tmp = self.cursor
        print("Concordance pour le", semestre, ":")
        cursor_tmp.execute("SELECT * FROM Horaires WHERE Semestre = ?", (semestre,))
        rslt_horaires = cursor_tmp.fetchall()
        cursor_tmp.execute("SELECT * FROM Planning WHERE Semestre = ?", (semestre,))
        rslt_planning = cursor_tmp.fetchall()
        for planning in rslt_planning:
            libelle_bd = ""
            type_erreur_bd = ""
            ressource_bd = ""
            heure_ecrites_bd = 0
            heure_poses_bd = 0
            rapport = ""
            rapport_warning = ""
            commentaire_str_bd = ""
            cursor_tmp.execute("SELECT Ressource FROM Horaires WHERE Semestre = ? AND Ressource = ?",
                               (semestre, planning[6]))
            ressource = cursor_tmp.fetchone()
            if ressource is None or not (ressource[0] in planning[6]):
                rapport += f"La ressource {planning[6]} n'existe pas ou n'a pas été placée au bon endroit.\n"
            else:
                cursor_tmp.execute(
                    "SELECT nbCours FROM Horaires WHERE Semestre = ? AND Type_Cours = ? AND Ressource = ?",
                    (semestre, "Amphi", ressource[0]))
                cmHoraire = cursor_tmp.fetchone()
                if cmHoraire is not None and planning[2] < cmHoraire[0]:
                    rapport += (f"Erreur CM: \n "
                                f"  -ressource: {ressource[0]},\n"
                                f"  -heures écrite: {planning[2]},\n "
                                f"  -heure posé: {cmHoraire[0]}\n")
                    ressource_bd = ressource[0]
                    type_erreur_bd = "Erreur"
                    heure_ecrites_bd = planning[2]
                    heure_poses_bd = cmHoraire[0]
                    cursor_tmp.execute(
                        "SELECT Commentaire FROM Cours WHERE Semestre = ? AND Ressource = ? AND Type_Cours = ?",
                        (semestre, ressource[0], "Amphi"))
                    commentaire = cursor_tmp.fetchall()
                    if commentaire is not None:
                        print(commentaire)
                        rapport += f"- Commentaire(s) : \n"
                        for coms in commentaire:
                            if coms[0] is not None and coms[0] not in [None, "", "None", "None,", "(None,)"]:
                                rapport += f"-{coms[0]}\n"
                                commentaire_str_bd += f"-{coms[0]}\n"
                if cmHoraire is not None and planning[2] > cmHoraire[0]:
                    rapport_warning += (f"Warning CM: \n "
                                        f"  -ressource: {ressource[0]} \n"
                                        f"  -heures écrite: {planning[2]}, \n"
                                        f"  -heure posé: {cmHoraire[0]}\n")
                    ressource_bd = ressource[0]
                    type_erreur_bd = "Warning"
                    heure_ecrites_bd = planning[2]
                    heure_poses_bd = cmHoraire[0]
                    cursor_tmp.execute(
                        "SELECT Commentaire FROM Cours WHERE Semestre = ? AND Ressource = ? AND Type_Cours = ?",
                        (semestre, ressource[0], "Amphi"))
                    commentaire = cursor_tmp.fetchall()
                    if commentaire is not None:
                        rapport_warning += f"- Commentaire(s) : \n"
                        for coms in commentaire:
                            if coms[0] is not None and coms[0] not in [None, "", "None", "None,", "(None,)"]:
                                rapport_warning += f"-{coms[0]}\n"
                                commentaire_str_bd += f"-{coms[0]}\n"
                cursor_tmp.execute("SELECT nbCours FROM Horaires WHERE Semestre = ? AND Type_Cours = ? AND Ressource "
                                   "= ?", (semestre, "TD", ressource[0]))
                tdHoraire = cursor_tmp.fetchone()
                if tdHoraire is not None and planning[3] < tdHoraire[0]:
                    rapport += (f"Erreur TD:\n "
                                f"  -ressource: {ressource[0]}\n"
                                f"  -heure écrites: {planning[3]}\n"
                                f"  -heure posé: {tdHoraire[0]}\n")
                    ressource_bd = ressource[0]
                    type_erreur_bd = "Erreur"
                    heure_ecrites_bd = planning[3]
                    heure_poses_bd = tdHoraire[0]
                    cursor_tmp.execute(
                        "SELECT Commentaire FROM Cours WHERE Semestre = ? AND Ressource = ? AND Type_Cours = ?",
                        (semestre, ressource[0], "TD"))
                    commentaire = cursor_tmp.fetchall()
                    if commentaire is not None:
                        rapport += f"- Commentaire(s) : \n"
                        for coms in commentaire:
                            if coms[0] is not None and coms[0] not in [None, "", "None", "None,", "(None,)"]:
                                rapport += f"-{coms[0]}\n"
                                commentaire_str_bd += f"-{coms[0]}\n"
                if tdHoraire is not None and planning[3] > tdHoraire[0]:
                    rapport_warning += (f"Warning TD:\n "
                                        f"  -ressource: {ressource[0]}\n"
                                        f"  -heure écrites: {planning[3]}\n"
                                        f"  -heure posé: {tdHoraire[0]}\n")
                    ressource_bd = ressource[0]
                    type_erreur_bd = "Warning"
                    heure_ecrites_bd = planning[3]
                    heure_poses_bd = tdHoraire[0]
                    cursor_tmp.execute(
                        "SELECT Commentaire FROM Cours WHERE Semestre = ? AND Ressource = ? AND Type_Cours = ?",
                        (semestre, ressource[0], "TD"))
                    commentaire = cursor_tmp.fetchall()
                    if commentaire is not None:
                        rapport_warning += f"- Commentaire(s) : \n"
                        for coms in commentaire:
                            if coms[0] is not None and coms[0] not in [None, "", "None", "None,", "(None,)"]:
                                rapport_warning += f"-{coms[0]}\n"
                                commentaire_str_bd += f"-{coms[0]}\n"
                cursor_tmp.execute("SELECT nbCours FROM Horaires WHERE Semestre = ? AND Type_Cours = ? AND Ressource "
                                   "= ?", (semestre, "TP", ressource[0]))
                tpHoraire = cursor_tmp.fetchone()
                if tpHoraire is not None and planning[4] < tpHoraire[0]:
                    rapport += (f"Erreur TP\n "
                                f"  -ressource: {ressource[0]} \n"
                                f"  -heures écrites: {planning[4]} \n "
                                f"  -heures posés: {tpHoraire[0]} \n")
                    ressource_bd = ressource[0]
                    type_erreur_bd = "Erreur"
                    heure_ecrites_bd = planning[4]
                    cursor_tmp.execute(
                        "SELECT Commentaire FROM Cours WHERE Semestre = ? AND Ressource = ? AND Type_Cours = ?",
                        (semestre, ressource[0], "TP"))
                    commentaire = cursor_tmp.fetchall()
                    if commentaire is not None:
                        rapport += f"- Commentaire(s) : \n"
                        for coms in commentaire:
                            if coms[0] is not None and coms[0] not in [None, "", "None", "None,", "(None,)"]:
                                rapport += f"-{coms[0]}\n"
                                commentaire_str_bd += f"-{coms[0]}\n"
                if tpHoraire is not None and planning[4] > tpHoraire[0]:
                    rapport_warning += (f"Warning TP\n "
                                        f"  -ressource: {ressource[0]} \n"
                                        f"  -heures écrites: {planning[4]} \n "
                                        f"  -heures posés: {tpHoraire[0]} \n")
                    ressource_bd = ressource[0]
                    type_erreur_bd = "Warning"
                    heure_ecrites_bd = planning[4]
                    heure_poses_bd = tpHoraire[0]
                    cursor_tmp.execute(
                        "SELECT Commentaire FROM Cours WHERE Semestre = ? AND Ressource = ? AND Type_Cours = ?",
                        (semestre, ressource[0], "TP"))
                    commentaire = cursor_tmp.fetchall()
                    if commentaire is not None:
                        rapport_warning += f"- Commentaire(s) : \n"
                        for coms in commentaire:
                            if coms[0] is not None and coms[0] not in [None, "", "None", "None,", "(None,)"]:
                                rapport_warning += f"-{coms[0]}\n"
                                commentaire_str_bd += f"-{coms[0]}\n"
                if rapport and not self.is_deleted((type_erreur_bd + semestre + ressource_bd + str(heure_ecrites_bd) + str(heure_poses_bd))):
                    print(commentaire_str_bd)
                    # incrémentation du nombre d'erreurs
                    self.nb_erreur += 1
                    libelle_bd = "Heure posé et écrites différentes dans le planning"
                    self.insert_error(libelle_bd, type_erreur_bd, semestre, ressource_bd, heure_ecrites_bd,
                                      heure_poses_bd,
                                      commentaire_str_bd)
                    # Écriture de l'erreur dans un fichier de rapport
                    with open(self.fichier_erreur, "a") as rapport_erreur:
                        rapport_erreur.write(f"\n \n Erreur: heure posé et écrites différentes dans le planning"
                                             f"\n "
                                             f" -semestre: {semestre} \n "
                                             f" -ressource: {ressource[0]}\n")
                        rapport_erreur.write(rapport)
                        rapport_erreur.write("\n")
                if rapport_warning and not self.is_deleted((type_erreur_bd + semestre + ressource_bd + str(heure_ecrites_bd) + str(heure_poses_bd))):
                    libelle = "Heure posé et écrites différentes dans le planning"
                    self.insert_error(libelle_bd, type_erreur_bd, semestre, ressource_bd, heure_ecrites_bd,
                                      heure_poses_bd,
                                      commentaire_str_bd)
                    # incrémentation du nombre d'erreurs
                    self.nb_erreur_warning += 1
                    # Écriture de l'erreur dans un fichier de rapport
                    with open(self.fichier_warning, "a") as rapport_w:
                        rapport_w.write(f"\n \n Warning: heure posé et écrites différentes dans le planning"
                                        f"\n "
                                        f" -semestre: {semestre} \n "
                                        f" -ressource: {ressource[0]}\n")
                        rapport_w.write(rapport_warning)
                        rapport_w.write("\n")

    def get_nb_erreur(self):
        """
        Fonction pour récupérer le nombre d'erreurs
        :return:
        """
        return self.nb_erreur

    def get_nb_warning(self):
        """
        Fonction pour récupérer le nombre d'erreurs
        :return:
        """
        return self.nb_erreur_warning

    def renom_fichier_avec_nb_erreur(self):
        """
        Fonction pour renommer les fichiers de rapport d'erreurs et de warnings avec le nombre respectif d'erreurs et de warnings.
        """
        # Renommage du fichier d'erreurs
        nb_erreurs = self.get_nb_erreur()
        nom_fichier_base_erreur = os.path.splitext(self.fichier_erreur)[0]
        date_modification_erreur = datetime.fromtimestamp(os.path.getmtime(self.fichier_erreur)).strftime(
            '%Y-%m-%d %H:%M')
        nouveau_nom_fichier_erreur = f"{nb_erreurs} erreurs -- {date_modification_erreur} -- rapport d'erreur.txt"
        nouveau_chemin_fichier_erreur = os.path.join(os.path.dirname(self.fichier_erreur), nouveau_nom_fichier_erreur)
        os.rename(self.fichier_erreur, nouveau_chemin_fichier_erreur)
        self.fichier_erreur = nouveau_chemin_fichier_erreur

        # Renommage du fichier de warnings
        nb_warnings = self.get_nb_warning()
        nom_fichier_base_warning = os.path.splitext(self.fichier_warning)[0]
        date_modification_warning = datetime.fromtimestamp(os.path.getmtime(self.fichier_warning)).strftime(
            '%Y-%m-%d %H:%M')
        nouveau_nom_fichier_warning = f"{nb_warnings} warnings -- {date_modification_warning} -- rapport de warnings.txt"
        nouveau_chemin_fichier_warning = os.path.join(os.path.dirname(self.fichier_warning),
                                                      nouveau_nom_fichier_warning)
        os.rename(self.fichier_warning, nouveau_chemin_fichier_warning)
        self.fichier_warning = nouveau_chemin_fichier_warning

    def is_deleted(self, id_erreur):
        """
        Fonction pour vérifier si l'erreur/le warning à été supprimé (ignoré)
        :return: Booléen
        """
        self.cursor.execute("SELECT is_delete FROM Erreurs WHERE Id_Erreur = ?", (id_erreur,))
        result = self.cursor.fetchone()
        if result and result[0] == 1:
            return True
        else:
            return False

    def insert_error(self, libelle, type_erreur, semestre, ressource, heure_ecrites, heure_poses, commentaires,
                     is_delete=0):
        """Méthode pour insérer ou mettre à jour une erreur dans la base de données en fonction de l'Id_Erreur."""
        id_erreur = type_erreur + semestre + ressource + str(heure_ecrites) + str(heure_poses)
        # Vérifie si l'Id_Erreur existe déjà
        self.cursor.execute("SELECT COUNT(*) FROM Erreurs WHERE Id_Erreur = ?", (id_erreur,))
        exists = self.cursor.fetchone()[0] > 0

        if exists:
            sql_update = '''UPDATE Erreurs SET Libelle=?, Type_Erreur=?, Semestre=?, Ressource=?, Heure_ecrites=?, 
                            Heure_poses=?, Commentaires=? WHERE Id_Erreur=?'''
            try:
                self.cursor.execute(sql_update, (libelle, type_erreur, semestre, ressource, heure_ecrites,
                                                 heure_poses, commentaires, id_erreur))
                self.conn.commit()
                print("Erreur mise à jour avec succès dans la base de données.")
            except sqlite3.Error as e:
                print("Erreur lors de la mise à jour de l'erreur dans la base de données.", e)
        else:
            sql_insert = '''INSERT INTO Erreurs(Id_Erreur, Libelle, Type_Erreur, Semestre, Ressource, Heure_ecrites, 
                            Heure_poses, Commentaires, is_delete) VALUES(?,?,?,?,?,?,?,?,?)'''
            try:
                self.cursor.execute(sql_insert, (id_erreur, libelle, type_erreur, semestre, ressource, heure_ecrites,
                                                 heure_poses, commentaires, is_delete))
                self.conn.commit()
                print("Erreur ajoutée avec succès dans la base de données.")
            except sqlite3.Error as e:
                print("Erreur lors de l'insertion de l'erreur dans la base de données.", e)


if __name__ == "__main__":
    VerifData().concordance("S2")
    VerifData().concordancePlanning("S2")