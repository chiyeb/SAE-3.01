import tkinter as tk
from tkinter import ttk, Scrollbar
import sqlite3


class ShowError:
    instance = None

    def __new__(cls):
        """
        Fonction pour créer une seule instance de la classe
        """
        if cls.instance is None:
            cls.instance = super(ShowError, cls).__new__(cls)
            cls.instance._setup()
        return cls.instance

    def _setup(self):
        """
        Fonction qui "setup" l'objet, il initialise la BD et la fenetre TKinter, les onglets, les canvas, les barres
        de défilement, les frames, les boutons et les tableaux :return:
        """
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

        # Création d'un Canvas dans chaque onglet
        self.canvas_errors = tk.Canvas(self.tab_errors)
        self.canvas_warnings = tk.Canvas(self.tab_warnings)

        # Ajout des barres de défilement verticales
        self.scroll_y_errors = Scrollbar(self.tab_errors, orient='vertical', command=self.canvas_errors.yview)
        self.scroll_y_warnings = Scrollbar(self.tab_warnings, orient='vertical', command=self.canvas_warnings.yview)

        # Ajout du Canvas à chaque onglet
        self.canvas_errors.config(yscrollcommand=self.scroll_y_errors.set)
        self.canvas_warnings.config(yscrollcommand=self.scroll_y_warnings.set)

        self.scroll_y_errors.pack(side='right', fill='y')
        self.scroll_y_warnings.pack(side='right', fill='y')

        self.canvas_errors.pack(side='left', fill='both', expand=True)
        self.canvas_warnings.pack(side='left', fill='both', expand=True)

        # Création d'un Frame dans chaque Canvas
        self.frame_errors = tk.Frame(self.canvas_errors)
        self.frame_warnings = tk.Frame(self.canvas_warnings)

        # Ajout du Frame au Canvas
        self.canvas_errors.create_window((0, 0), window=self.frame_errors, anchor='nw')
        self.canvas_warnings.create_window((0, 0), window=self.frame_warnings, anchor='nw')

        # Ajout d'un bouton Suppression globale en haut à droite
        button = tk.Button(self.frame_errors, text="Suppression globale", border=0, fg='black',
                           font='Helvetica 12 bold', command=lambda: self.confirm_delete())
        button.grid(row=0, column=6, padx=40, pady=15, sticky='ne')

        # Ajout d'un bouton Suppression globale en haut à droite
        button2 = tk.Button(self.frame_warnings, text="Suppression globale", border=0, fg='black',
                            font='Helvetica 12 bold', command=lambda: self.confirm_delete())
        button2.grid(row=0, column=6, padx=40, pady=15, sticky='ne')

        # Ajout d'un bouton Rafrachir en haut à gauche
        button3 = tk.Button(self.frame_errors, text="Rafraichir", border=0, fg='black', font='Helvetica 12 bold',
                            command=lambda: self.refresh())
        button3.grid(row=1, column=6, padx=65, pady=10, sticky='ne')

        # Ajout d'un bouton Rafrachir en haut à gauche
        button3 = tk.Button(self.frame_warnings, text="Rafraichir", border=0, fg='black', font='Helvetica 12 bold',
                            command=lambda: self.refresh())
        button3.grid(row=1, column=6, padx=65, pady=10, sticky='ne')

        # Configuration du Canvas pour qu'il s'étende automatiquement
        self.canvas_errors.bind('<Configure>', lambda event, canvas=self.canvas_errors: self.on_frame_configure(canvas))
        self.canvas_warnings.bind('<Configure>',
                                  lambda event, canvas=self.canvas_warnings: self.on_frame_configure(canvas))

        # Récupération des données de la base de données sauf la dernière colonne
        self.cursor.execute(
            'SELECT Id_Erreur, Libelle, Type_Erreur, Semestre, Ressource, Heure_ecrites, Heure_poses, Commentaires '
            'FROM Erreurs')

        rows = self.cursor.fetchall()

        # Récupération des noms des colonnes
        self.column_names = [description[0] for description in self.cursor.description]

        # Création des tableaux et des boutons pour chaque ligne
        self.trees = []
        # Création des numérotation au dessus de chaque tableau
        self.labels = []
        self.label_states = [False] * len(rows)

        self.sort_data(rows)
        self.display_errors(rows)
        self.display_warnings(rows)

    def display_errors(self, rows):
        """
        Affiche les erreurs dans l'onglet "Erreurs" et les boutons pour chaque ligne pour afficher les commentaires et supprimer les erreurs.
        :param rows:
        :return:
        """
        # Nombre de colonnes par ligne
        num_columns = 4

        for index, row in enumerate(rows):
            if row[2] == 'Erreur':

                # Création du label pour numéroter le tableau
                label = tk.Label(self.frame_errors, text=f"{index}", bg='black', fg='white', font='Helvetica 12 bold',
                                 padx=10, pady=5)
                label.grid(row=(index // num_columns) * 2, column=index % num_columns, padx=7, pady=5, sticky='n')

                # Création du tableau
                tree = ttk.Treeview(self.frame_errors, columns=('Value',))
                tree.heading('#0', text='Erreur')
                tree.heading('#1', text='Valeur')

                tree.column('#0', width=140, anchor='w')
                tree.column('#1', width=140, anchor='w')

                # Positionnement du tableau pour qu'il y ait 6 colonnes par ligne maximum
                tree.grid(row=(index // num_columns) * 2 + 1, column=index % num_columns, padx=7, pady=30)

                # Ajout d'une bordure blanche dans le tableau
                tree.tag_configure('odd', foreground='black')

                # Ajout des valeurs de la ligne au tableau
                for column_name, value in zip(self.column_names, row):
                    tree.insert('', 'end', text=column_name, values=(value,))

                # Ajout du tableau à la liste pour y accéder ultérieurement
                self.trees.append(tree)

                # Création du bouton
                button = tk.Button(self.frame_errors, text="Détail", border=0, fg='black', font='Helvetica 12 bold',
                                   command=lambda index=index: self.on_button_click(index), width=6)
                # Ajout du bouton à la dernière ligne de chaque tableau positionné en bas
                button.grid(row=(index // num_columns) * 2 + 1, column=index % num_columns, padx=7, pady=35,
                            sticky='sw')

                # Ajout du bouton supprimer à la dernière ligne de chaque tableau positionné en bas à droite
                button2 = tk.Button(self.frame_errors, text="Supprimer", border=0, fg='black', font='Helvetica 12 bold',
                                    command=lambda index=index: self.delete_error(index))
                # Ajout du bouton à la dernière ligne de chaque tableau positionné en bas à droite
                button2.grid(row=(index // num_columns) * 2 + 1, column=index % num_columns, padx=7, pady=35,
                             sticky='se')

    def display_warnings(self, rows):
        """
        Affiche les warnings dans l'onglet "Warnings" et les boutons pour chaque ligne pour afficher les commentaires et supprimer les warnings.
        :param rows:
        :return:
        """
        # Nombre de colonnes par ligne
        num_columns = 4

        for index, row in enumerate(rows):
            if row[2] != 'Erreur':
                # Création du label pour numéroter le tableau
                label = tk.Label(self.frame_warnings, text=f"{index}", bg='black', fg='white', font='Helvetica 12 bold',
                                 padx=10, pady=5)
                label.grid(row=(index // num_columns) * 2, column=index % num_columns, padx=7, pady=5, sticky='n')

                tree = ttk.Treeview(self.frame_warnings, columns=('Value',))
                tree.heading('#0', text='Erreur')
                tree.heading('#1', text='Valeur')

                tree.column('#0', width=140, anchor='w')
                tree.column('#1', width=140, anchor='w')

                tree.grid(row=(index // num_columns) * 2 + 1, column=index % num_columns, padx=7, pady=30)
                tree.tag_configure('odd', foreground='black')

                for column_name, value in zip(self.column_names, row):
                    tree.insert('', 'end', text=column_name, values=(value,))

                self.trees.append(tree)

                # Création du bouton
                button = tk.Button(self.frame_warnings, text="Détail", border=0, fg='black', font='Helvetica 12 bold',
                                   command=lambda index=index: self.on_button_click2(index))
                # Ajout du bouton à la dernière ligne de chaque tableau positionné en bas à gauche
                button.grid(row=(index // num_columns) * 2 + 1, column=index % num_columns, padx=7, pady=35,
                            sticky='sw')

                # Ajout du bouton cacher à la dernière ligne de chaque tableau positionné en bas à droite
                button2 = tk.Button(self.frame_warnings, text="Supprimer", border=0, fg='black',
                                    font='Helvetica 12 bold',
                                    command=lambda index=index: self.delete_error(index))
                # Ajout du bouton à la dernière ligne de chaque tableau positionné en bas à droite
                button2.grid(row=(index // num_columns) * 2 + 1, column=index % num_columns, padx=7, pady=35,
                             sticky='se')

    def refresh(self):
        """
        Rafraichir la fenêtre principale
        :return:
        """
        # Ré ouverture de la fenêtre principale
        self.root.destroy()
        self.instance = None
        self._setup()

    def confirm_delete(self):
        """
        Fonction pour confirmer la suppression globale de toutes les erreurs ayant la colonne is_delete = 1
        :return:
        """
        # Création d'une fenêtre de message pour confirmer la suppression
        self.confirm_window = tk.Toplevel()
        self.confirm_window.title("Suppression globale")
        self.confirm_window.geometry("400x150")

        # Création d'un label pour le message de confirmation
        label = tk.Label(self.confirm_window, text="Voulez-vous vraiment supprimer toutes les erreurs ?",
                         font='Helvetica 14 bold')
        label.pack(pady=10)

        # Création d'un bouton pour confirmer la suppression
        button = tk.Button(self.confirm_window, text="Confirmer", font='Helvetica 12 bold',
                           command=lambda: self.delete_all_errors())
        button.pack(pady=20, padx=20, side='left')

        # Création d'un bouton pour annuler la suppression
        button2 = tk.Button(self.confirm_window, text="Annuler", font='Helvetica 12 bold',
                            command=lambda: self.confirm_window.destroy())
        button2.pack(pady=20, padx=20, side='right')

    def cancel_error(self, index):
        """
        Fonction pour annuler la suppression d'une erreur en mettant à jour la colonne is_delete dans la base de données.
        :param index:
        :return:
        """
        # Récupération de l'identifiant de l'erreur à supprimer dans la base de données
        id_error = self.trees[index].item(self.trees[index].get_children()[0])['values'][0]
        print(f"Annulation de l'erreur = {id_error}")

        # Récupération de la valeur de la colonne is_delete
        is_delete = self.cursor.execute('SELECT is_delete FROM Erreurs WHERE Id_Erreur = ?', (id_error,)).fetchone()[0]

        # Mise à jour de la base de données pour marquer l'erreur comme supprimée avec la colonne is_delete = 1
        new_is_delete = 0 if is_delete == 1 else 1
        self.cursor.execute(f"UPDATE Erreurs SET is_delete = {new_is_delete} WHERE Id_Erreur = ?", (id_error,))
        self.conn.commit()

        # Remplacer le bouton annuler par un autre bouton pour supprimer
        button2 = tk.Button(self.frame_errors, text="Supprimer", border=0, fg='black', font='Helvetica 12 bold',
                            command=lambda index=index: self.delete_error(index))
        button2.grid(row=(index // 4) * 2 + 1, column=index % 4, padx=7, pady=35, sticky='se')

        button3 = tk.Button(self.frame_warnings, text="Supprimer", border=0, fg='black', font='Helvetica 12 bold',
                            command=lambda index=index: self.delete_error(index))
        button3.grid(row=(index // 4) * 2 + 1, column=index % 4, padx=7, pady=35, sticky='se')

    def delete_all_errors(self):
        """
        Suppression globale de toutes les erreurs ayant la colonne is_delete = 1
        :return:
        """
        # Suppresion de toutes les lignes de la base de données avec la colonne is_delete = 1
        self.cursor.execute("DELETE FROM Erreurs WHERE is_delete = 1")
        self.conn.commit()
        self.confirm_window.destroy()

    def delete_error(self, index):
        """
        Fonction pour supprimer une erreur en mettant à jour la colonne is_delete égale à 1 dans la base de données.
        :param index: Index de l'erreur à supprimer
        :return:
        """
        # Récupération de l'identifiant de l'erreur à supprimer dans la base de données
        id_error = self.trees[index].item(self.trees[index].get_children()[0])['values'][0]
        print(f"Suppression de l'erreur = {id_error}")

        # Récupération de la valeur de la colonne is_delete
        is_delete = self.cursor.execute('SELECT is_delete FROM Erreurs WHERE Id_Erreur = ?', (id_error,)).fetchone()[0]

        # Mise à jour de la base de données pour marquer l'erreur comme supprimée avec la colonne is_delete = 1
        new_is_delete = 0 if is_delete == 1 else 1
        self.cursor.execute(f"UPDATE Erreurs SET is_delete = {new_is_delete} WHERE Id_Erreur = ?", (id_error,))
        self.conn.commit()

        # Remplacer le bouton supprimer par un autre bouton pour annuler la suppression
        button = tk.Button(self.frame_errors, text="Annuler", border=0, fg='black', font='Helvetica 12 bold',
                           command=lambda index=index: self.cancel_error(index), width=8)
        button.grid(row=(index // 4) * 2 + 1, column=index % 4, padx=8, pady=35, sticky='se')

        button = tk.Button(self.frame_warnings, text="Annuler", border=0, fg='black', font='Helvetica 12 bold',
                           command=lambda index=index: self.cancel_error(index), width=8)
        button.grid(row=(index // 4) * 2 + 1, column=index % 4, padx=8, pady=35, sticky='se')

    def sort_data(self, rows):
        """
        Tri des données en fonction de la troisième colonne afin d'afficher les erreurs dans l'onglet Erreurs et les warnings dans l'onglet Warnings.
        :param rows: Liste des données
        :return:
        """
        # Tri des données en fonction de la troisième colonne
        rows.sort(key=lambda x: x[2])

    def on_button_click(self, index):
        """
        Fonction pour afficher la dernière ligne de chaque tableau dans une fenêtre de message.
        :param index:
        :return:
        """
        num_columns = 4
        # Afficher la dernière ligne de chaque tableau
        tree = self.trees[index]
        last_row = tree.item(tree.get_children()[-1])['values']
        print(f"Dernière ligne du tableau {index}: {last_row}")

        # Afficher la dernière ligne dans une fenêtre de message
        if last_row:
            last_row_str = " ".join(str(x) for x in last_row)

            label = tk.Label(self.frame_errors, text=f"Commentaire {index} : {last_row_str}", wraplength=150, border=2,
                             relief='solid', bg='white', fg='black', font='Helvetica 14 bold', padx=5, pady=5)

            label.grid(row=(index // num_columns) * 2 + 2, column=index % num_columns, padx=5, pady=2, sticky='s')

            # Mettre à jour l'état du label
            self.label_states[index] = True

            # Ajouter le label à la liste pour y accéder ultérieurement
            self.labels.append(label)


        else:
            label = tk.Label(self.frame_errors, text=f"Commentaire {index} est vide", wraplength=150, border=2,
                             relief='solid', bg='white', fg='black', font='Helvetica 14 bold', padx=5, pady=5)

            label.grid(row=(index // num_columns) * 2 + 2, column=index % num_columns, padx=5, pady=2, sticky='s')

            # Mettre à jour l'état du label
            self.label_states[index] = False

            # Ajouter le label à la liste pour y accéder ultérieurement
            self.labels.append(label)

    def on_button_click2(self, index):
        """
        Fonction pour afficher la dernière ligne de chaque tableau dans une fenêtre de message.
        :param index: Index du tableau
        :return:
        """
        num_columns = 4
        # Afficher la dernière ligne de chaque tableau
        tree = self.trees[index]
        last_row = tree.item(tree.get_children()[-1])['values']
        print(f"Dernière ligne du tableau {index}: {last_row}")

        # Afficher la dernière ligne dans une fenêtre de message
        if last_row:
            last_row_str = " ".join(str(x) for x in last_row)

            label = tk.Label(self.frame_warnings, text=f"Commentaire {index} : {last_row_str}", wraplength=150,
                             border=2,
                             relief='solid', bg='white', fg='black', font='Helvetica 14 bold', padx=5, pady=5)

            label.grid(row=(index // num_columns) * 2 + 2, column=index % num_columns, padx=5, pady=2, sticky='s')

            # Mettre à jour l'état du label
            self.label_states[index] = True

            # Ajouter le label à la liste pour y accéder ultérieurement
            self.labels.append(label)



        else:
            label = tk.Label(self.frame_warnings, text=f"Commentaire {index} est vide", wraplength=200, border=2,
                             relief='solid', bg='white', fg='black', font='Helvetica 14 bold')
            label.grid(row=(index // num_columns) * 2 + 2, column=index % num_columns, padx=7, pady=3, sticky='s')

            # Mettre à jour l'état du label
            self.label_states[index] = False

            # Ajouter le label à la liste pour y accéder ultérieurement
            self.labels.append(label)

    def on_frame_configure(self, canvas):
        """
        Fonction pour configurer la taille du Canvas en fonction de la taille du Frame
        :param canvas: Canvas
        :return:
        """
        # Configurer la taille du Canvas en fonction de la taille du Frame
        canvas.configure(scrollregion=canvas.bbox('all'))

    def run(self):
        """
        Fonction pour lancer la fenêtre principale
        :return:
        """
        self.root.mainloop()


if __name__ == "__main__":
    app = ShowError()
    app.run()
