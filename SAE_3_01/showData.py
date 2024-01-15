import tkinter as tk
from tkinter import ttk
import sqlite3


class showData:
    """
    Classe qui permet d'afficher les données de la base de données dans une fenêtre graphique
    """
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(showData, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def _setup(self):
        """
        Fonction qui "setup" l'objet, il initialise la BD et la fenetre TKinter
        :return:
        """
        # connexion à la base de données
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()

        # Initialise l'interface graphique tKinter
        self.root = tk.Tk()
        self.root.title("Visualiseur de Base de Données")

        # Barre de recherche
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.root, textvariable=self.search_var)
        self.search_entry.pack(padx=10, pady=5)
        search_button = tk.Button(self.root, text="Rechercher", command=self.search_data)
        search_button.pack(pady=5)

        # Combobox pour choisir la table
        self.table_var = tk.StringVar()
        self.tables_combobox = ttk.Combobox(self.root, textvariable=self.table_var)
        self.tables_combobox.pack(padx=10, pady=10)
        self.tables_combobox.bind("<<ComboboxSelected>>", self.update_table_view)

        # Treeview pour afficher les données
        self.treeview = ttk.Treeview(self.root)
        self.treeview.pack(padx=10, pady=10, fill='both', expand=True)

        self.initialize_combobox()

    def initialize_combobox(self):
        """
        Remplit le combobox avec les noms des tables de la base de données.
        Sélectionne la première table par défaut et met à jour le Treeview (tableau où sont affiché les données).
        :return:
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        self.tables_combobox['values'] = [table[0] for table in tables]
        if tables:
            self.tables_combobox.current(0)
            self.update_table_view(None)

    #
    def update_table_view(self, event):
        """
        Met à jour le Treeview (tableau où sont affiché les données) pour afficher les données de la table sélectionnée
        dans le combobox (liste des tables de la BD).
        :param event:
        :return:
        """
        table_name = self.table_var.get()
        self.update_table_data(table_name)

    def update_table_data(self, table_name):
        """
        Fonction récupère et affiche les données de la table sélectionné dans le Treeview (tableau où sont affiché les données).
        :param table_name: 
        :return: 
        """
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in self.cursor.fetchall()]

        self.treeview.delete(*self.treeview.get_children())
        self.treeview['columns'] = columns
        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, anchor=tk.CENTER)

        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        for row in rows:
            self.treeview.insert('', tk.END, values=row)

    def search_data(self):
        """
        Fonction pour rechercher des données depuis la fenetre tKinter dans la BD.
        :return: 
        """
        # récupère la recherche
        search_query = self.search_var.get()
        # récupère le nom de la table
        table_name = self.table_var.get()

        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in self.cursor.fetchall()]

        query = f"SELECT * FROM {table_name} WHERE " + " OR ".join(
            [f"{col} LIKE '%{search_query}%'" for col in columns])
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.treeview.delete(*self.treeview.get_children())
        for row in rows:
            self.treeview.insert('', tk.END, values=row)

    def run(self):
        """
        Fonction qui démarre la fenetre
        :return: 
        """
        self.root.mainloop()

#i = showData()
#i.run()