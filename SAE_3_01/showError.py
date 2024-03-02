from tkinter import ttk, Scrollbar
import tkinter as tk
import sqlite3
from PIL import Image, ImageTk

class ShowError:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(ShowError, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def _setup(self):
        # Connexion à la base de données
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()

        # Création de la fenêtre principale
        self.root = tk.Tk()
        self.root.title("Rapport d'erreurs")
        self.root.geometry("1500x1300")

        # Création d'un Notebook pour les onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Ajout des onglets "Erreurs" et "Warnings"
        self.tab_errors = tk.Frame(self.notebook)
        self.tab_warnings = tk.Frame(self.notebook)
        self.notebook.add(self.tab_errors, text='Erreurs')
        self.notebook.add(self.tab_warnings, text='Warnings')

        # Fond blanc pour les onglets
        self.tab_errors.config(bg='white')
        self.tab_warnings.config(bg='white')

        # Récupération des données de la base de données sauf la dernière colonne
        self.cursor.execute('SELECT Id_Erreur, Libelle, Type_Erreur, Semestre, Ressource, Heure_ecrites, Heure_poses, Commentaires FROM Erreurs')

        rows = self.cursor.fetchall()

        # Récupération des noms des colonnes
        self.column_names = [description[0] for description in self.cursor.description]

        self.trees = []
        self.labels = []
        self.label_states = [False] * len(rows)

        self.sort_data(rows)
        self.display_errors(rows)
        self.display_warnings(rows)

    def display_errors(self, rows):
        # Nombre de colonnes par ligne
        num_columns = 4

        for index, row in enumerate(rows):
            if row[2] == 'Erreur':
                # Création du label pour numéroter le tableau
                label = tk.Label(self.tab_errors, text=f"{index}", bg='black', fg='white', font='Helvetica 12 bold', padx=10, pady=5)
                label.grid(row=(index // num_columns) * 2, column=index % num_columns, padx=7, pady=5, sticky='n')

                # Création du tableau
                tree = ttk.Treeview(self.tab_errors, columns=('Value',))
                tree.heading('#0', text='Erreur')
                tree.heading('#1', text='Valeur')

                tree.column('#0', width=140, anchor='w')
                tree.column('#1', width=140, anchor='w')

                # Positionnement du tableau pour qu'il y ait 6 colonnes par ligne maximum
                tree.grid(row=(index // num_columns) * 2 + 1, column=index % num_columns, padx=7, pady=30)

                # Ajout d'une bordure blanche dans le tableau
                tree.tag_configure('odd', foreground='white')

                # Ajout des valeurs de la ligne au tableau
                for column_name, value in zip(self.column_names, row):
                    tree.insert('', 'end', text=column_name, values=(value,))

                # Ajout du tableau à la liste pour y accéder ultérieurement
                self.trees.append(tree)

                # Création du bouton
                button = tk.Button(self.tab_errors, text="Détail", border=0 ,fg='black', font='Helvetica 12 bold', command=lambda index=index: self.on_button_click(index))
                # Ajout du bouton à la dernière ligne de chaque tableau positionné en bas
                button.grid(row=(index // num_columns) * 2 + 1, column=index % num_columns, padx=7, pady=35, sticky='sw')

                # Ajout du bouton cacher à la dernière ligne de chaque tableau positionné en bas à droite
                button2 = tk.Button(self.tab_errors, text="Supprimer", border=0, fg='black', font='Helvetica 12 bold',
                                    command=lambda index=index: self.delete_error(index))
                # Ajout du bouton à la dernière ligne de chaque tableau positionné en bas à droite
                button2.grid(row=(index // num_columns) * 2 + 1, column=index % num_columns, padx=7, pady=35,
                             sticky='se')

                # Ajout d'une image au-dessus du tableau
                img = Image.open('images/logo_IUT.png')
                img = img.resize((100, 100), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                canvas = tk.Canvas(self.tab_errors, width=100, height=100, bg='white', highlightthickness=0)
                canvas.create_image(50, 50, image=img)
                canvas.place(relx=1.0, rely=0.0, anchor='ne')

                # Gardez une référence à l'image pour l'empêcher d'être supprimée par le ramasse-miettes
                canvas.img = img

    def display_warnings(self, rows):
        # Nombre de colonnes par ligne
        num_columns = 4

        for index, row in enumerate(rows):
            if row[2] != 'Erreur':
                # Création du label pour numéroter le tableau
                label = tk.Label(self.tab_warnings, text=f"{index}", bg='black', fg='white', font='Helvetica 12 bold',
                                 padx=10, pady=5)
                label.grid(row=(index // num_columns) * 2, column=index % num_columns, padx=7, pady=5, sticky='n')

                tree = ttk.Treeview(self.tab_warnings, columns=('Value',))
                tree.heading('#0', text='Erreur')
                tree.heading('#1', text='Valeur')

                tree.column('#0', width=140, anchor='w')
                tree.column('#1', width=140, anchor='w')

                tree.grid(row=(index // num_columns) * 2 + 1, column=index % num_columns, padx=7, pady=30)
                tree.tag_configure('odd', foreground='white')

                for column_name, value in zip(self.column_names, row):
                    tree.insert('', 'end', text=column_name, values=(value,))

                self.trees.append(tree)

                # Création du bouton
                button = tk.Button(self.tab_warnings, text="Détail", border=0, fg='black', font='Helvetica 12 bold',
                                   command=lambda index=index: self.on_button_click2(index))
                # Ajout du bouton à la dernière ligne de chaque tableau positionné en bas à gauche
                button.grid(row=(index // num_columns) * 2 + 1, column=index % num_columns, padx=7, pady=35,
                            sticky='sw')

                # Ajout du bouton cacher à la dernière ligne de chaque tableau positionné en bas à droite
                button2 = tk.Button(self.tab_warnings, text="Supprimer", border=0, fg='black', font='Helvetica 12 bold',
                                      command=lambda index=index: self.delete_error(index))
                # Ajout du bouton à la dernière ligne de chaque tableau positionné en bas à droite
                button2.grid(row=(index // num_columns) * 2 + 1, column=index % num_columns, padx=7, pady=35,
                            sticky='se')

                # Ajout d'une image au-dessus du tableau
                img = Image.open('images/logo_IUT.png')
                img = img.resize((100, 100), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                canvas = tk.Canvas(self.tab_warnings, width=100, height=100, bg='white', highlightthickness=0)
                canvas.create_image(50, 50, image=img)
                canvas.place(relx=1.0, rely=0.0, anchor='ne')

                # Gardez une référence à l'image pour l'empêcher d'être supprimée par le ramasse-miettes
                canvas.img = img

                # Barre de défilement pour l'onglet "Erreurs"
                scrollbar = Scrollbar(self.tab_errors, orient='vertical')
                scrollbar.grid(row=0, column=4, rowspan=70, sticky='nes')
                scrollbar.config(command=tree.yview)
                tree.config(yscrollcommand=scrollbar.set)

    def delete_error(self, index):
        # Récupération de l'identifiant de l'erreur à supprimer dans la base de données
        id_error = self.trees[index].item(self.trees[index].get_children()[0])['values'][0]
        print(f"Suppression de l'erreur = {id_error}")

        # Récupération de la valeur de la colonne is_delete
        is_delete = self.cursor.execute('SELECT is_delete FROM Erreurs WHERE Id_Erreur = ?', (id_error,)).fetchone()[0]

        # Mise à jour de la base de données pour marquer l'erreur comme supprimée avec la colonne is_delete = 1
        new_is_delete = 0 if is_delete == 1 else 1
        self.cursor.execute(f"UPDATE Erreurs SET is_delete = {new_is_delete} WHERE Id_Erreur = ?", (id_error,))
        self.conn.commit()

        # Supprimer le tableau correspondant de l'interface utilisateur
        self.trees[index].destroy()

    def sort_data(self, rows):
        # Tri des données en fonction de la troisième colonne
        rows.sort(key=lambda x: x[2])

    def on_button_click(self, index):
        # Afficher la dernière ligne de chaque tableau
        tree = self.trees[index]
        last_row = tree.item(tree.get_children()[-1])['values']
        print(f"Dernière ligne du tableau {index}: {last_row}")

        # Afficher la dernière ligne dans une fenêtre de message
        if last_row:
            last_row_str = " ".join(str(x) for x in last_row)

            label = tk.Label(self.tab_errors, text=f"Commentaire {index} : {last_row_str}", wraplength=150, border=2,
                             relief='solid', bg='white', fg='black', font='Helvetica 14 bold', padx=5, pady=5)

            label.grid(row=(index // 6) * 2 + 2, column=index % 6, padx=5, pady=2, sticky='s')

            # Mettre à jour l'état du label
            self.label_states[index] = True

            # Ajouter le label à la liste pour y accéder ultérieurement
            self.labels.append(label)

        else:
            label = tk.Label(self.tab_errors, text=f"Commentaire {index} est vide",wraplength=150, border=2,
                             relief='solid', bg='white', fg='black', font='Helvetica 14 bold', padx=5, pady=5)

            label.grid(row=(index // 6) * 2 + 2, column=index % 6, padx=5, pady=2, sticky='s')

            # Mettre à jour l'état du label
            self.label_states[index] = False

            # Ajouter le label à la liste pour y accéder ultérieurement
            self.labels.append(label)

    def on_button_click2(self, index):
        # Afficher la dernière ligne de chaque tableau
        tree = self.trees[index]
        last_row = tree.item(tree.get_children()[-1])['values']
        print(f"Dernière ligne du tableau {index}: {last_row}")

        # Afficher la dernière ligne dans une fenêtre de message
        if last_row:
            last_row_str = " ".join(str(x) for x in last_row)

            label = tk.Label(self.tab_warnings, text=f"Commentaire {index} : {last_row_str}", wraplength=150, border=2,
                             relief='solid', bg='white', fg='black', font='Helvetica 14 bold', padx=5, pady=5)

            label.grid(row=(index // 6) * 2 + 2, column=index % 6, padx=5, pady=2, sticky='s')

            # Mettre à jour l'état du label
            self.label_states[index] = True

            # Ajouter le label à la liste pour y accéder ultérieurement
            self.labels.append(label)

        else:
            label = tk.Label(self.tab_warnings, text=f"Commentaire {index} est vide", wraplength=200, border=2,
                             relief='solid', bg='white', fg='black', font='Helvetica 14 bold')
            label.grid(row=(index // 6) * 2 + 2, column=index % 6, padx=7, pady=3, sticky='s')

            # Mettre à jour l'état du label
            self.label_states[index] = False

            # Ajouter le label à la liste pour y accéder ultérieurement
            self.labels.append(label)

    def run(self):
        self.root.mainloop()

app = ShowError()
app.run()
