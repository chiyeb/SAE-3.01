import tkinter as tk
from tkinter import ttk
import sqlite3

class showError:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(showError, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def _setup(self):
        # Connexion à la base de données
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()

        # Création de la fenêtre principale
        self.root = tk.Tk()
        self.root.title("Rapport d'erreurs")
        self.root.geometry("1400x1300")
        self.root.bg = 'Black'

        # Récupération de toutes les lignes de la table
        self.cursor.execute('SELECT * FROM Erreurs')
        rows = self.cursor.fetchall()

        # Récupération des noms des colonnes
        self.column_names = [description[0] for description in self.cursor.description]

        # Nombre de colonnes par ligne
        num_columns = 6

        for index, row in enumerate(rows):
            # Création du tableau
            tree = ttk.Treeview(self.root, columns=('Value',))
            tree.heading('#0', text='Erreur')
            tree.heading('#1', text='Valeur')

            tree.column('#0', width=100, anchor='w')
            tree.column('#1', width=100, anchor='w')

            # Positionnement du tableau pour qu'il y ait 6 colonnes par ligne maximum
            tree.grid(row=index // num_columns, column=index % num_columns, padx=10, pady=10)

            # Ajout d'une bordure blanche dans le tableau
            tree.tag_configure('odd', foreground='white')

            # Ajout des valeurs de la ligne au tableau
            for column_name, value in zip(self.column_names, row):
                tree.insert('', 'end', text=column_name, values=(value,))

    def run(self):
        self.root.mainloop()

i = showError()
i.run()
