import os
import shutil
import sqlite3
import tkinter as tk
from tkinter import messagebox


class Utils:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(Utils, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def _setup(self):
        # Initialise la connexion à la base de données
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()


    # supprimer toutes la BD
    def clearBD(self):
        confirmation = self.confirm_deletion()
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


    # confirmer la suppresion ou l'annuler
    def confirm_deletion(self):
        root = tk.Tk()
        root.withdraw()  # masquer la fenêtre principale de tkinter

        # créer une boîte de dialogue de confirmation
        response = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer les dossiers ?")

        root.destroy()  # ferme la fenêtre tkinter

        return response

    # supprimer tout les fichiers genere par le programme
    def clearAllFiles(self):
        confirmation = self.confirm_deletion()
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

    # afficher la confirmation de suppression ou d'annulation
    def display_result(self, is_deleted):
        root = tk.Tk()
        root.withdraw()

        if is_deleted:
            messagebox.showinfo("Suppression", "Tous les fichiers ont été supprimés.")
        else:
            messagebox.showinfo("Suppression", "Les fichiers n'ont pas été supprimés.")

        root.destroy()

    # recréer les dossiers importants
    def recreate_file(self):
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
            os.makedirs(DossierStats) # recrée le dossier



