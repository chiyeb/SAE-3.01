import tkinter as tk
from tkinter import filedialog, messagebox


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

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(selectFile, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def _setup(self):
        """
        "Setup" l'objet : initialise la connexion à la BD
        :return:
        """
        # initialise Tkinter
        root = tk.Tk()
        root.withdraw()

    def open_select_file(self):
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
        messagebox.showinfo("IMPORTANT", "Veuillez sélectionner le fichier maquette national du BUT 2")
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
            file.write(f'{nom_fichier} = {destination}\n')
