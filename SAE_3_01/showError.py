import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
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

        # Mise en blanc du fond de la fenêtre principale
        self.root.configure(bg='white')

        # Récupération de toutes les lignes de la table
        self.cursor.execute('SELECT * FROM Erreurs')
        rows = self.cursor.fetchall()

        # Récupération des noms des colonnes
        self.column_names = [description[0] for description in self.cursor.description]

        # Nombre de colonnes par ligne
        num_columns = 6

        self.trees = []
        self.labels = []
        self.label_states = [False] * len(rows)

        for index, row in enumerate(rows):
            # Création du label pour numéroter le tableau
            label = tk.Label(self.root, text=f"{index}", bg='black', fg='white', font='Helvetica 12 bold', padx=10, pady=5)
            label.grid(row=(index // num_columns) * 2, column=index % num_columns, padx=7, pady=5, sticky='n')

            # Création du tableau
            tree = ttk.Treeview(self.root, columns=('Value',))
            tree.heading('#0', text='Erreur')
            tree.heading('#1', text='Valeur')

            tree.column('#0', width=100, anchor='w')
            tree.column('#1', width=100, anchor='w')

            # Positionnement du tableau pour qu'il y ait 6 colonnes par ligne maximum
            tree.grid(row=(index // num_columns) * 2 + 1, column=index % num_columns, padx=7, pady=30)

            # Ajout d'une bordure blanche dans le tableau
            tree.tag_configure('odd', foreground='white')

            # Ajout des valeurs de la ligne au tableau
            for column_name, value in zip(self.column_names, row):
                tree.insert('', 'end', text=column_name, values=(value,))

                # Ajout d'une image au-dessus du tableau
                img = Image.open('images/logo_IUT.png')
                img = img.resize((100, 100), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                canvas = tk.Canvas(self.root, width=100, height=100, bg='white', highlightthickness=0)
                canvas.create_image(50, 50, image=img)
                canvas.place(relx=1.0, rely=0.0, anchor='ne')

                # Gardez une référence à l'image pour l'empêcher d'être supprimée par le ramasse-miettes
                canvas.img = img

            # Ajout du tableau à la liste pour y accéder ultérieurement
            self.trees.append(tree)

            # Création du bouton
            button = tk.Button(self.root, text="Détail", border=0 ,fg='black', font='Helvetica 12 bold', command=lambda index=index: self.on_button_click(index))
            # Ajout du bouton à la dernière ligne de chaque tableau positionné en bas
            button.grid(row=(index // num_columns) * 2 + 1, column=index % num_columns, padx=7, pady=40, sticky='s')

    def on_button_click(self, index):
        # Afficher la dernière ligne de chaque tableau
        tree = self.trees[index]
        last_row = tree.item(tree.get_children()[-1])['values']
        print(f"Dernière ligne du tableau {index}: {last_row}")

        # Afficher la dernière ligne dans une fenêtre de message
        if last_row:
            last_row_str = " ".join(str(x) for x in last_row)

            # Si le label est déjà affiché, le supprimer
            if self.label_states[index]:
                self.labels[index].destroy()

            label = tk.Label(self.root, text=f"Commentaire {index} : {last_row_str}", wraplength=200, border=2, relief='solid', bg='white', fg='black', font='Helvetica 14 bold')
            label.grid(row=(index // 6) * 2 + 2, column=index % 6, padx=7, pady=3, sticky='s')

            # Mettre à jour l'état du label
            self.label_states[index] = True

            # Ajouter le label à la liste pour y accéder ultérieurement
            self.labels.append(label)

        else:
            label = tk.Label(self.root, text=f"Commentaire {index} est vide", wraplength=200)
            label.grid(row=(index // 6) * 2 + 2, column=index % 6, padx=7, pady=3, sticky='s')

            # Mettre à jour l'état du label
            self.label_states[index] = False

            # Ajouter le label à la liste pour y accéder ultérieurement
            self.labels.append(label)

    def run(self):
        self.root.mainloop()

i = showError()
i.run()
