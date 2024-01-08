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
        # Mettre le fichier dans le dossier "rapport d'erreurs"
        self.fichierErreur = os.path.join(
            folder_path, f"rapport d'erreur du {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.txt"
        )

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
                if not (planning[1] in maquette[3]):
                    rapport += f"La ressource {maquette[1]} n'existe pas ou n'a pas été placée au bon endroit.\n"
                else:
                    if planning[2] != maquette[4]:
                        print(f"erreur cm pour le semestre {semestre} et la ressource {maquette[3]}")
                        rapport += (f"Erreur CM: \n"
                                    f"  -ressource: {maquette[3]}\n "
                                    f"  -heure planning: {planning[2]}\n"
                                    f"  -heure maquette: {maquette[4]}\n")
                    if planning[3] != maquette[5]:
                        print("erreur td pour le semestre {semestre} et la ressource {maquette[3]}")
                        rapport += (f"Erreur TD: \n"
                                    f"  -ressource: {maquette[3]}\n"
                                    f"  -heure planning: {planning[3]}\n"
                                    f"  -heure maquette{maquette[5]}\n")

                    if planning[4] != maquette[6]:
                        print(f"erreur tp pour le semestre {semestre} et la ressource {maquette[3]}")
                        rapport += (f"Erreur TP: \n"
                                    f"  -ressource: {maquette[3]} \n"
                                    f"  -heure planning: {planning[4]} \n"
                                    f"  -heure maquette: {maquette[6]}\n")

                    if rapport:
                        # incrémentation du nombre d'erreur
                        self.nbErreur += 1
                        # Écriture de l'erreur dans un fichier de rapport
                        with open(self.fichierErreur, "a") as rapport_erreur:
                            rapport_erreur.write(f"Erreur: heures ne correspondent pas entre la maquette et le planning"
                                                 f"\n "
                                                 f" -semestre: {semestre} \n "
                                                 f" -ressource: {maquette[3]}\n")
                            rapport_erreur.write(rapport)
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
        '''
        Fonction pour récupérer le nombre d'erreurs
        :return:
        '''
        return self.nbErreur

    def renomFichierAvecNbErreur(self):
        '''
        Fonction pour renommer le fichier avec le nombre d'erreurs
        :return:
        '''
        nb_erreurs = self.getNbErreur()
        nom_fichier_base = os.path.splitext(self.fichierErreur)[0]
        date_modification = datetime.fromtimestamp(os.path.getmtime(self.fichierErreur)).strftime('%Y-%m-%d %H-%M')
        nouveau_nom_fichier = f"{nb_erreurs} erreurs -- {date_modification} -- rapport d'erreur.txt"
        nouveau_chemin_fichier = os.path.join(os.path.dirname(self.fichierErreur), nouveau_nom_fichier)
        os.rename(self.fichierErreur, nouveau_chemin_fichier)
        self.fichierErreur = nouveau_chemin_fichier

        print(f"Le fichier a été renommé {nouveau_nom_fichier}")


