import os
import shutil
import sqlite3
import tkinter as tk
import webbrowser
from tkinter import messagebox, ttk
from selectfile import *
from scribefileprof import *
from mail import *
from showdata import *


class Utils:
    """
    Classe où se trouvent des fonctions utiles pour le programme
    """
    instance = None
    root = None
    selectFileInstance = None
    showDataInstance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(Utils, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def _setup(self):
        """
        "Setup" l'objet : initialise la connexion à la BD
        :return:
        """
        # Initialise la connexion à la base de données
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()
        self.selectFileInstance = SelectFile('utils')

    def create_main_window(self):
        """
        Afficher la fenêtre graphique principal pour laisser l'utilisateur choisir une action.
        :return:
        """
        self.root = tk.Tk()
        self.root.title("Gestion du programme")
        self.root.geometry("600x600")

        ttk.Label(self.root, text="Choisissez une action :").pack(pady=10)

        delete_bd_button = ttk.Button(self.root, text="Supprimer les données de la base de données",
                                      command=self.clear_bd)
        delete_bd_button.pack(pady=5)

        delete_files_button = ttk.Button(self.root, text="Supprimer les fichiers générés",
                                         command=self.clearAllFiles)
        delete_files_button.pack(pady=5)
        chose_file_button = ttk.Button(self.root, text="Choisir les fichiers utile pour le programme",
                                       command=self.selectFileInstance.open_select_file)

        chose_file_button.pack(pady=5)
        generer_fichier_prof_button = ttk.Button(self.root, text="Générer le fichier d'heures par professeurs",
                                                 command=self.generer_fichier_heure_prof)
        generer_fichier_prof_button.pack(pady=5)
        envoie_mail_prof_button = ttk.Button(self.root, text="Envoyer les fichiers par mail",
                                             command=run)
        envoie_mail_prof_button.pack(pady=5)

        open_link_button = ttk.Button(self.root, text="Ouvrir le manuel d'utilisation",
                                      command=self.open_link)
        open_link_button.pack(pady=5)

        self.root.mainloop()

    def open_link(self):
        """
        Fonction pour ouvrir le lien du manuel d'utilisation
        """
        webbrowser.open_new("https://chihebbr.notion.site/Manuel-d-utilisation-f730396ababa421796965488ed0aa194?pvs=4")

    def clear_bd(self):
        """
        Fonction pour supprimer toutes les données la BD
        :return:
        """
        confirmation = self.confirm_deletion("Les données de la base de données")
        # si l'utilisateur à confirmer la suppression de la BD
        if confirmation:
            # requête pour obtenir la liste des tables
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [table[0] for table in self.cursor.fetchall()]
            # Parcoure chaque table et supprimer toutes les données
            for table in tables:
                self.cursor.execute(f"DELETE FROM {table}")
            # Valide les modifications
            self.conn.commit()
            self.display_result(True)
        # si l'utilisateur n'as pas confirmé la suppression de la BD
        else:
            self.display_result(False)

    def confirm_deletion(self, arg):
        """
        Fonction pour confirmer la suppresion ou l'annuler
        :param arg: Argument à supprimer
        :return:
        """
        root = tk.Tk()
        root.withdraw()

        # créer une boîte de dialogue de confirmation
        response = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer {arg}?")

        root.destroy()  # ferme la fenêtre tkinter

        return response

    def clearAllFiles(self):
        """
        Fonction pour supprimer tout les fichiers généré par le programme
        :return:
        """
        confirmation = self.confirm_deletion("les fichiers générés")
        # si l'utilisateur a confirmé la suppression des fichiers
        if confirmation:
            # On définit les chemins des dossiers et fichiers à supprimer
            dossier_rap_err = 'rapport d\'erreurs'
            dossier_fich_genere = 'fichiers genere'
            dossier_fichere_mail = 'fichiers genere mail'
            dossier_stats = 'statistiques'
            # Supprimer le contenu du dossier "rapport d'erreurs"
            if os.path.exists(dossier_rap_err):
                shutil.rmtree(dossier_rap_err)
                os.makedirs(dossier_rap_err)  # Recréer le dossier vide

            # Supprimer le contenu du dossier "fichiers genere"
            if os.path.exists(dossier_fich_genere):
                shutil.rmtree(dossier_fich_genere)
                os.makedirs(dossier_fich_genere)  # Recréer le dossier vide

            # Supprimer le dossier "statistiques"
            if os.path.exists(dossier_stats):
                shutil.rmtree(dossier_stats)
                os.makedirs(dossier_stats)
            self.display_result(True)
            # si le dossier "fichiers genere mail" existe, le supprimer
            if os.path.exists(dossier_fichere_mail):
                shutil.rmtree(dossier_fichere_mail)
                os.makedirs(dossier_fichere_mail)
        # si l'utilisateur n'as pas confirmé la suppression des fichiers
        else:
            self.display_result(False)

    def display_result(self, is_deleted):
        """
        Fonction qui affiche la confirmation de suppression ou d'annulation
        :param is_deleted: Si les fichiers/données ont été supprimés
        :return:
        """
        root = tk.Tk()
        root.withdraw()

        if is_deleted:
            messagebox.showinfo("Suppression", "Tous les fichiers/données ont été supprimés.")
        else:
            messagebox.showinfo("Suppression", "Les fichiers/données n'ont pas été supprimés.")

        root.destroy()

    def recreate_file(self):
        """
        Fonction qui recrée les dossiers importants
        :return:
        """
        # Définition des chemins des dossiers et fichiers à supprimer
        dossierRapErr = 'rapport d\'erreurs'
        dossierFichGenere = 'fichiers genere'
        DossierStats = 'statistiques'
        # Si le dossier n'existe pas, le créer
        if not os.path.exists(dossierRapErr):
            os.makedirs(dossierRapErr)  # recrée le dossier

        # Si le dossier n'existe pas, le créer
        if not os.path.exists(dossierFichGenere):
            os.makedirs(dossierFichGenere)  # recrée le dossier vide

        # Si le dossier n'existe pas, le créer
        if not os.path.exists(DossierStats):
            os.makedirs(DossierStats)  # recrée le dossier

    def generer_fichier_heure_prof(self):
        """
        Fonction pour générer le fichier d'heure par professeur
        :return:
        """
        scribeFileProfInstance = ScribeFileProf()
        scribeFileProfInstance.run()


i = Utils()
i.create_main_window()
