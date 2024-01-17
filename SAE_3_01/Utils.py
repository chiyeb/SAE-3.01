import os
import shutil
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from selectFile import *


class Utils:
    """
    Classe où se trouvent des fonctions utiles pour le programme
    """
    instance = None
    root = None
    selectFileInstance = None

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
        self.selectFileInstance = selectFile('utils')

    def create_main_window(self):
        """
        Afficher la fenêtre graphique principal pour laisser l'utilisateur choisir une action.
        :return:
        """
        self.root = tk.Tk()
        self.root.title("Gestion du programme")
        self.root.geometry("600x600")

        ttk.Label(self.root, text="Choisissez une action :").pack(pady=10)

        delete_bd_button = ttk.Button(self.root, text="Supprimer la base de données",
                                      command=self.clearBD)
        delete_bd_button.pack(pady=5)

        delete_files_button = ttk.Button(self.root, text="Supprimer les fichiers générés",
                                         command=self.clearAllFiles)
        delete_files_button.pack(pady=5)
        chose_file_button = ttk.Button(self.root, text="Choisir les fichiers utile pour le programme",
                                       command=self.selectFileInstance.open_select_file)
        chose_file_button.pack(pady=5)

        self.root.mainloop()

    def clearBD(self):
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
        :return:
        """
        root = tk.Tk()
        root.withdraw()  # masquer la fenêtre principale de tkinter

        # créer une boîte de dialogue de confirmation
        response = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer {arg}?")

        root.destroy()  # ferme la fenêtre tkinter

        return response

    def clearAllFiles(self):
        """
        Fonction pour supprimer tout les fichiers généré par le programme
        :return:
        """
        confirmation = self.confirm_deletion("les fichiers")
        # si l'utilisateur a confirmé la suppression des fichiers
        if confirmation:
            # Définition des chemins des dossiers et fichiers à supprimer
            dossierRapErr = 'rapport d\'erreurs'
            dossierFichGenere = 'fichiers genere'
            DossierStats = 'statistiques'
            # Supprimer le contenu du dossier "rapport d'erreurs"
            if os.path.exists(dossierRapErr):
                shutil.rmtree(dossierRapErr)
                os.makedirs(dossierRapErr)  # Recréer le dossier vide

            # Supprimer le contenu du dossier "fichiers genere"
            if os.path.exists(dossierFichGenere):
                shutil.rmtree(dossierFichGenere)
                os.makedirs(dossierFichGenere)  # Recréer le dossier vide

            # Supprimer le dossier "statistiques"
            if os.path.exists(DossierStats):
                shutil.rmtree(DossierStats)
                os.makedirs(DossierStats)
            self.display_result(True)
        # si l'utilisateur n'as pas confirmé la suppression des fichiers
        else:
            self.display_result(False)

    def display_result(self, is_deleted):
        """
        Fonction qui affiche la confirmation de suppression ou d'annulation
        :param is_deleted:
        :return:
        """
        root = tk.Tk()
        root.withdraw()

        if is_deleted:
            messagebox.showinfo("Suppression", "Tous les fichiers ont été supprimés.")
        else:
            messagebox.showinfo("Suppression", "Les fichiers n'ont pas été supprimés.")

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


i = Utils()
i.create_main_window()
