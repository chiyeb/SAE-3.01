import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pandas as pd


class selectFile:
    """
    Classe qui permet de faire choisir à l'utilisateur l'endroit où se trouve chaque fichier nécessaire au programme
    """
    fichier_destination = None
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
        self.fichier_destination = "fichiers necessaires/file_destination.txt"
        # vérifie si le fichier existe
        if os.path.exists(self.fichier_destination):
            self.recup_destination_file()
        else:
            with open(self.fichier_destination, "w") as file:
                file.write("")
                self.open_select_file()

    def verify_before_open(self, file, nom_fichier):
        if os.path.exists(file):
            print("ok")
        else:
            open('fichiers necessaires/file_destination.txt', 'w').close()
            self.open_select_file()

    def open_select_file(self):
        if os.path.exists(self.fichier_destination):
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

    def scribe_destination_file(self, nom_fichier, nouvelle_destination):
        """
        Écrit dans un fichier .TXT le nom et la destination de chaque fichier
        :param nom_fichier:
        :param nouvelle_destination:
        :return:
        """
        with open(self.fichier_destination, "r") as file:
            lignes = file.readlines()
        print(lignes)
        is_writed = False
        # Modifier la ligne correspondante
        with open(self.fichier_destination, "w") as file:
            for ligne in lignes:
                if ligne.startswith(nom_fichier + "="):
                    # Remplacer par la nouvelle destination
                    file.write(f"{nom_fichier}={nouvelle_destination}\n")
                    is_writed = True
                else:
                    # Conserver les autres lignes telles quelles
                    file.write(ligne)
        if not is_writed:
            with open(self.fichier_destination, "a") as file:
                file.write(f"{nom_fichier}={nouvelle_destination}\n")

    def recup_destination_file(self):
        """
        Récupère la destination de chaque fichier dans le fichier.
        :return:
        """
        with open(self.fichier_destination, "r") as fichier:
            nb_ligne = 0
            for ligne in fichier:
                nb_ligne += 1
        if nb_ligne < 5:
            os.remove(self.fichier_destination)
            messagebox.showerror("ERREUR","Veuillez relancer le programme et re-choisir les fichiers.")
            exit()

        with open(self.fichier_destination, "r") as fichier:
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
