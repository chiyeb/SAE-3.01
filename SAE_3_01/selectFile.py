import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pandas as pd


class selectFile:
    """
    Classe qui permet de faire choisir à l'utilisateur l'endroit où se trouve chaque fichier nécessaire au programme
    """
    instance = None
    maquette_BUT1 = None
    maquette_BUT2 = None
    maquette_BUT3 = None
    nom_prof = None
    planning = None
    QFQ = None
    maquette_BUT1_file = None
    maquette_BUT2_file = None
    maquette_BUT3_file = None
    nom_prof_file = None
    planning_file = None
    QFQ_file = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(selectFile, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def _setup(self):
        # vérifie si le fichier existe
        if os.path.exists("fichiers necessaires/file_destination.txt"):
            # vérifie si le fichier est rempli (si sa taille est supérieur à 0)
            if os.path.getsize("fichiers necessaires/file_destination.txt") > 0:
                self.recup_destination_file()

    def verify_before_open(self, file, nom_fichier):
        if nom_fichier == "Nom des professeurs":
            try:
                open(file, "w")
            except:
                messagebox.showwarning("ERREUR",
                                     f"Le fichier {nom_fichier} n'a pas été reconnu, veuillez le re sélectionner")
                self.open_select_file_nom_prof()
        else:
            try:
                pd.ExcelFile(file)
            except:
                messagebox.showwarning("ERREUR", f"Le fichier {nom_fichier} n'a pas été reconnu, veuillez le re sélectionner")
                match nom_fichier:
                    case "Maquette National BUT1":
                        self.open_select_file_BUT1_maquette()
                    case "Maquette National BUT2":
                        self.open_select_file_BUT2_maquette()
                    case "Maquette National BUT3":
                        self.open_select_file_BUT3_maquette()
                    case "planning":
                        self.open_select_file_planning()
                    case "Ce que fait chaque professeurs":
                        self.open_select_file_QFQ()
                    case _:
                        print("erreur inattendu")

    def open_select_file(self):
        # initialise Tkinter
        root = tk.Tk()
        root.withdraw()
        if os.path.exists("fichiers necessaires/file_destination.txt"):
            open('fichiers necessaires/file_destination.txt', 'w').close()
        self.open_select_file_BUT1_maquette()
        self.open_select_file_BUT2_maquette()
        self.open_select_file_BUT3_maquette()
        self.open_select_file_planning()
        self.open_select_file_nom_prof()
        self.open_select_file_QFQ()

    def open_select_file_BUT1_maquette(self):
        """
        Ouvre le sélecteur de fichier pour sélectionner le fichier maquette BUT1
        :return:
        """
        # Affiche le message
        messagebox.showinfo("IMPORTANT", "Veuillez sélectionner le fichier maquette national du BUT 1")
        # ouvre la fenêtre pour choisir un fichier
        self.maquette_BUT1 = filedialog.askopenfilename()
        # écrit la destination dans le fichier destination
        self.scribe_destination_file("BUT1", self.maquette_BUT1)

    def open_select_file_BUT2_maquette(self):
        """
        Ouvre le sélecteur de fichier pour sélectionner le fichier maquette BUT2
        :return:
        """
        # Affiche le message
        messagebox.showinfo("IMPORTANT", "Veuillez sélectionner le fichier du BUT 2")
        # ouvre la fenêtre pour choisir un fichier
        self.maquette_BUT2 = filedialog.askopenfilename()
        # écrit la destination dans le fichier destination
        self.scribe_destination_file("BUT2", self.maquette_BUT2)

    def open_select_file_BUT3_maquette(self):
        """
        Ouvre le sélecteur de fichier pour sélectionner le fichier maquette BUT3
        :return:
        """
        # Affiche le message
        messagebox.showinfo("IMPORTANT", "Veuillez sélectionner le fichier maquette national du BUT 3")
        # ouvre la fenêtre pour choisir un fichier
        self.maquette_BUT3 = filedialog.askopenfilename()
        # écrit la destination dans le fichier destination
        self.scribe_destination_file("BUT3", self.maquette_BUT3)

    def open_select_file_nom_prof(self):
        """
        Ouvre le sélecteur de fichier pour sélectionner le fichier où se trouve le nom des professeurs
        :return:
        """
        # Affiche le message
        messagebox.showinfo("IMPORTANT", "Veuillez sélectionner le fichier où se trouve le nom des professeurs")
        # ouvre la fenêtre pour choisir un fichier
        self.nom_prof = filedialog.askopenfilename()
        # écrit la destination dans le fichier destination
        self.scribe_destination_file("nom_prof", self.nom_prof)

    def open_select_file_planning(self):
        """
        Ouvre le sélecteur de fichier pour sélectionner le fichier planning
        :return:
        """
        # Affiche le message
        messagebox.showinfo("IMPORTANT", "Veuillez sélectionner le fichier planning")
        # ouvre la fenêtre pour choisir un fichier
        self.planning = filedialog.askopenfilename()
        # écrit la destination dans le fichier destination
        self.scribe_destination_file("planning", self.planning)

    def open_select_file_QFQ(self):
        """
        Ouvre le sélecteur de fichier pour sélectionner le fichier de ce que fait chaque professeur par semestre
        et par ressources
        :return:
        """
        # Affiche le message
        messagebox.showinfo("IMPORTANT", "Veuillez sélectionner le fichier de ce que fait chaque professeurs par "
                                         "semestre et par ressources")
        # ouvre la fenêtre pour choisir un fichier
        self.QFQ = filedialog.askopenfilename()
        # écrit la destination dans le fichier destination
        self.scribe_destination_file("QFQ", self.QFQ)

    def scribe_destination_file(self, nom_fichier, destination):
        """
        Écrit dans un fichier .TXT le nom et la destination de chaque fichier
        :param nom_fichier:
        :param destination:
        :return:
        """
        fichier_destination = "fichiers necessaires/file_destination.txt"
        with open(fichier_destination, "a") as file:
            file.write(f'{nom_fichier}={destination}\n')

    def recup_destination_file(self):
        """
        Récupère la destination de chaque fichier dans le fichier.
        :return:
        """
        with open("fichiers necessaires/file_destination.txt", "r") as fichier:
            # Lire chaque ligne du fichier
            for ligne in fichier:
                # Divise la ligne en utilisant le signe "=" comme séparateur
                parties = ligne.strip().split("=")

                # Vérifie si la ligne a été correctement divisée en deux parties
                if len(parties) == 2:
                    # Récupère chaque chemin de chaque fichier
                    match parties[0]:
                        case "BUT1":
                            self.maquette_BUT1_file = parties[1]
                            self.verify_before_open(parties[1], "Maquette National BUT1")
                        case "BUT2":
                            self.maquette_BUT2_file = parties[1]
                            self.verify_before_open(parties[1], "Maquette National BUT2")
                        case "BUT3":
                            self.maquette_BUT3_file = parties[1]
                            self.verify_before_open(parties[1], "Maquette National BUT3")
                        case "planning":
                            self.planning_file = parties[1]
                            self.verify_before_open(parties[1], "planning")
                        case "nom_prof":
                            self.nom_prof_file = parties[1]
                            self.verify_before_open(parties[1], "Nom des professeurs")
                        case "QFQ":
                            self.QFQ_file = parties[1]
                            self.verify_before_open(parties[1], "Ce que fait chaque professeurs")
                        case _:
                            print("erreur inattendu")
                else:
                    print(f"Erreur de format sur la ligne : {ligne}")
