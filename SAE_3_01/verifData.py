import os
import sqlite3
import math
from datetime import datetime

import pandas as pd

from insertData import insertData


class verifData:
    """
    Classe permettant de vérifier la concordance des données
    """
    instance = None
    fichierErreur = None
    nbErreur = 0
    nbErreurWarning = 0
    fichierWarning = None

    def __new__(cls):
        nbErreur = 0
        if cls.instance is None:
            cls.instance = super(verifData, cls).__new__(cls)
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
        self.fichierErreur = os.path.join(
            folder_path, f"rapport d'erreur du {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.txt"
        )
        self.fichierWarning = os.path.join(folder_path,
                                           f"rapport de warnings du {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.txt")

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
        cpt = 0
        for maquette in rslt_maquette:
            for planning in rslt_planning:
                rapport = ""
                rapport_warning = ""
                if not (planning[1] in maquette[3]):
                    rapport += f"La ressource {maquette[1]} n'existe pas ou n'a pas été placée au bon endroit.\n"
                else:
                    if planning[2] > maquette[4]:
                        print(f"erreur cm pour le semestre {semestre}")
                        rapport += (f"Erreur CM écrite dans le planning supérieur à celle prévu nationalement: \n"
                                    f"  -Ressource: {maquette[3]}\n "
                                    f"  -Heure planning: {planning[2]}\n"
                                    f"  -Heure maquette: {maquette[4]}\n")
                    if planning[2] < maquette[4]:
                        print(f"Warning CM pour le semestre {semestre}")
                        rapport_warning += (f"Warning : Heures différentes entre le fichier planning et maquette\n"
                                            f"  -Ressource: {maquette[3]}\n"
                                            f"  -Heure planning: {planning[2]}\n"
                                            f"  - Heure maquette: {maquette[4]}\n")
                    if planning[3] > maquette[5]:
                        print(f"Erreur TD pour le semestre {semestre}")
                        rapport += (f"Erreur TD écrite dans le planning supérieur à celle prévu nationalement: \n"
                                    f"  -Ressource: {maquette[3]}\n"
                                    f"  -Heure planning: {planning[3]}\n"
                                    f"  -Heure maquette: {maquette[5]}\n")
                    if planning[3] < maquette[5]:
                        print(f"Warning TD pour le semestre {semestre}")
                        rapport_warning += (f"Warning : Heures différentes entre le fichier planning et maquette\n"
                                            f"  -Ressource: {maquette[3]}\n"
                                            f"  -Heure planning: {planning[3]}\n"
                                            f"  - Heure maquette: {maquette[5]}\n")
                    if planning[4] > maquette[6]:
                        print(f"erreur TP pour le semestre {semestre}")
                        rapport += (f"Erreur TP écrite dans le planning supérieur à celle prévu nationalement: \n"
                                    f"  -Hessource: {maquette[3]} \n"
                                    f"  -Heure planning: {planning[4]} \n"
                                    f"  -Heure maquette: {maquette[6]}\n")
                    if planning[4] < maquette[6]:
                        print(f"Warning Tp pour le semestre {semestre}")
                        rapport_warning += (f"Warning : Heures différentes entre le fichier planning et maquette\n"
                                            f"  -Ressource: {maquette[3]}\n"
                                            f"  -Heure planning: {planning[4]}\n"
                                            f"  - Heure maquette: {maquette[6]}\n")
                    if rapport:
                        # incrémentation du nombre d'erreur
                        self.nbErreur += 1
                        # Écriture de l'erreur dans un fichier de rapport
                        with open(self.fichierErreur, "a") as rapport_erreur:
                            rapport_erreur.write(rapport)
                            rapport_erreur.write("\n")
                    if rapport_warning:
                        # incrémentation du nombre d'erreurs
                        self.nbErreurWarning += 1
                        # Écriture de l'erreur dans un fichier de rapport
                        with open(self.fichierWarning, "a") as rapport_erreur:
                            rapport_erreur.write(rapport_warning)
                            rapport_erreur.write("\n")

                    if planning[2] == maquette[4] and planning[3] == maquette[5] and planning[4] == maquette[6]:
                        print(f"pas d'erreur pour le semestre {semestre}")

    def concordancePlanning(self, semestre):
        """
        Fonction qui vérifie la concordance entre les cours écrit(les heures) et posé dans le fichier planning
        :param semestre:
        :return:
        """
        cursor_tmp = self.cursor
        conn_tmp = self.conn
        print("Concordance pour le", semestre, ":")
        cursor_tmp.execute("SELECT * FROM Horaires WHERE Semestre = ?", (semestre,))
        rslt_horaires = cursor_tmp.fetchall()
        cursor_tmp.execute("SELECT * FROM Planning WHERE Semestre = ?", (semestre,))
        rslt_planning = cursor_tmp.fetchall()
        cpt = 0
        for planning in rslt_planning:
            rapport = ""
            cursor_tmp.execute("SELECT Ressource FROM Horaires WHERE Semestre = ? AND Ressource = ?",
                               (semestre, planning[6]))
            ressource = cursor_tmp.fetchone()
            print(ressource)
            if ressource is None or not (ressource[0] in planning[6]):
                rapport += f"La ressource {planning[6]} n'existe pas ou n'a pas été placée au bon endroit.\n"
            else:
                cursor_tmp.execute(
                    "SELECT nbCours FROM Horaires WHERE Semestre = ? AND Type_Cours = ? AND Ressource = ?",
                    (semestre, "Amphi", ressource[0]))
                cmHoraire = cursor_tmp.fetchone()
                if cmHoraire is not None and planning[2] != cmHoraire[0]:
                    print("cm")
                    rapport += (f"Erreur CM: \n "
                                f"  -ressource: {ressource[0]}"
                                f"  -heures écrite: {planning[2]}, "
                                f"  -heure posé: {cmHoraire[0]}\n")
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

                cursor_tmp.execute("SELECT nbCours FROM Horaires WHERE Semestre = ? AND Type_Cours = ? AND Ressource "
                                   "= ?", (semestre, "TD", ressource[0]))
                tdHoraire = cursor_tmp.fetchone()
                if tdHoraire is not None and planning[3] != tdHoraire[0]:
                    print("td")
                    rapport += (f"Erreur TD:\n "
                                f"  -ressource: {ressource[0]}\n"
                                f"  -heure écrites: {planning[3]}\n"
                                f"  -heure posé: {tdHoraire[0]}\n")
                    cursor_tmp.execute(
                        "SELECT Commentaire FROM Cours WHERE Semestre = ? AND Ressource = ? AND Type_Cours = ?",
                        (semestre, ressource[0], "TD"))
                    commentaire = cursor_tmp.fetchall()
                    if commentaire is not None:
                        print(commentaire)
                        rapport += f"- Commentaire(s) : \n"
                        for coms in commentaire:
                            if coms[0] is not None and coms[0] not in [None, "", "None", "None,", "(None,)"]:
                                rapport += f"-{coms[0]}\n"

                cursor_tmp.execute("SELECT nbCours FROM Horaires WHERE Semestre = ? AND Type_Cours = ? AND Ressource "
                                   "= ?", (semestre, "TP", ressource[0]))
                tpHoraire = cursor_tmp.fetchone()
                if tpHoraire is not None and planning[4] != tpHoraire[0]:
                    print("tp")
                    rapport += (f"Erreur TP\n "
                                f"  -ressource: {ressource[0]} \n"
                                f"  -heures écrites: {planning[4]} \n "
                                f"  -heures posés: {tpHoraire[0]} \n")
                    cursor_tmp.execute(
                        "SELECT Commentaire FROM Cours WHERE Semestre = ? AND Ressource = ? AND Type_Cours = ?",
                        (semestre, ressource[0], "TP"))
                    commentaire = cursor_tmp.fetchall()
                    if commentaire is not None:
                        print(commentaire)
                        rapport += f"- Commentaire(s) : \n"
                        for coms in commentaire:
                            if coms[0] is not None and coms[0] not in [None, "", "None", "None,", "(None,)"]:
                                rapport += f"-{coms[0]}\n"
                if rapport:
                    # incrémentation du nombre d'erreurs
                    self.nbErreur += 1
                    # Écriture de l'erreur dans un fichier de rapport
                    with open(self.fichierErreur, "a") as rapport_erreur:
                        rapport_erreur.write(f"\n \n Erreur: heure posé et écrites différentes dans le planning"
                                             f"\n "
                                             f" -semestre: {semestre} \n "
                                             f" -ressource: {ressource[0]}\n")
                        rapport_erreur.write(rapport)
                        rapport_erreur.write("\n")

    def getNbErreur(self):
        """
        Fonction pour récupérer le nombre d'erreurs
        :return:
        """
        return self.nbErreur

    def getNbWarning(self):
        """
        Fonction pour récupérer le nombre d'erreurs
        :return:
        """
        return self.nbErreurWarning

    def renomFichierAvecNbErreur(self):
        """
        Fonction pour renommer les fichiers de rapport d'erreurs et de warnings avec le nombre respectif d'erreurs et de warnings.
        """
        # Renommage du fichier d'erreurs
        nb_erreurs = self.getNbErreur()
        nom_fichier_base_erreur = os.path.splitext(self.fichierErreur)[0]
        date_modification_erreur = datetime.fromtimestamp(os.path.getmtime(self.fichierErreur)).strftime(
            '%Y-%m-%d %H-%M')
        nouveau_nom_fichier_erreur = f"{nb_erreurs} erreurs -- {date_modification_erreur} -- rapport d'erreur.txt"
        nouveau_chemin_fichier_erreur = os.path.join(os.path.dirname(self.fichierErreur), nouveau_nom_fichier_erreur)
        os.rename(self.fichierErreur, nouveau_chemin_fichier_erreur)
        self.fichierErreur = nouveau_chemin_fichier_erreur

        # Renommage du fichier de warnings
        nb_warnings = self.getNbWarning()
        nom_fichier_base_warning = os.path.splitext(self.fichierWarning)[0]
        date_modification_warning = datetime.fromtimestamp(os.path.getmtime(self.fichierWarning)).strftime(
            '%Y-%m-%d %H-%M')
        nouveau_nom_fichier_warning = f"{nb_warnings} warnings -- {date_modification_warning} -- rapport de warnings.txt"
        nouveau_chemin_fichier_warning = os.path.join(os.path.dirname(self.fichierWarning), nouveau_nom_fichier_warning)
        os.rename(self.fichierWarning, nouveau_chemin_fichier_warning)
        self.fichierWarning = nouveau_chemin_fichier_warning