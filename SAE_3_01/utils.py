import shutil
import webbrowser

from SAE_3_01.BUT1 import BUT1
from SAE_3_01.BUT2 import BUT2
from SAE_3_01.BUT3 import BUT3
from scribefileprof import *
from mail import *
from showdata import *


class Utils:
    """
    Classe où se trouvent des fonctions utiles pour le programme
    """
    instance = None
    root = None
    selectFileInstance = None
    showDataInstance = None
    but1Instance = None
    but2Instance = None
    but3Instance = None

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
        self.selectFileInstance = SelectFile('utils')
        self.but1Instance = BUT1('utils')
        self.but2Instance = BUT2('utils')
        self.but3Instance = BUT3('utils')

    def create_main_window(self):
        self.root = tk.Tk()
        self.root.title("Gestion du programme")
        self.root.geometry("600x600")

        # Créer un style
        style = ttk.Style()
        style.configure("TButton", font=('Helvetica', 12), borderwidth='4')
        style.configure("TLabel", font=('Helvetica', 14), padding=10)

        # Utiliser un Frame pour organiser les widgets
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        ttk.Label(main_frame, text="Choisissez une action :").pack()

        buttons = [
            ("Supprimer les données de la base de données", self.clear_bd),
            ("Lancer le programme seulement pour le BUT1", self.but1_run),
            ("Lancer le programme seulement pour le BUT2", self.but2_run),
            ("Lancer le programme seulement pour le BUT3", self.but3_run),
            ("Supprimer les fichiers générés", self.clearAllFiles),
            ("Choisir les fichiers utiles pour le programme", self.selectFileInstance.open_select_file),
            ("Générer le fichier d'heures par professeurs", self.generer_fichier_heure_prof),
            ("Envoyer les fichiers par mail", run),
            ("Ouvrir le manuel d'utilisation", self.open_link)
        ]

        for (text, command) in buttons:
            ttk.Button(main_frame, text=text, command=command).pack(pady=5, fill="x")

        self.root.mainloop()

    def open_link(self):
        """
        Fonction pour ouvrir le lien du manuel d'utilisation
        """
        webbrowser.open_new("https://chihebbr.notion.site/Manuel-d-utilisation-f730396ababa421796965488ed0aa194?pvs=4")

    def clear_bd(self):
        """
        Fonction pour supprimer toutes les données la BD
        :return:
        """
        confirmation = self.confirm_deletion("Les données de la base de données")
        # si l'utilisateur à confirmer la suppression des données de la BD
        if confirmation:
            # requête pour obtenir la liste des tables
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [table[0] for table in self.cursor.fetchall()]
            # Parcoure chaque table et supprimer toutes les données
            for table in tables:
                self.cursor.execute(f"DELETE FROM {table}")
            self.conn.commit()
            self.display_result(True)
        # si l'utilisateur n'as pas confirmé la suppression des données de de la BD
        else:
            self.display_result(False)

    def confirm_deletion(self, arg):
        """
        Fonction pour confirmer la suppresion ou l'annuler
        :param arg: Argument à supprimer
        :return:
        """
        root = tk.Tk()
        root.withdraw()

        # créer une boîte de dialogue de confirmation
        response = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer {arg}?")

        root.destroy()  # ferme la fenêtre tkinter

        return response

    def clearAllFiles(self):
        """
        Fonction pour supprimer tout les fichiers généré par le programme
        :return:
        """
        confirmation = self.confirm_deletion("les fichiers générés")
        # si l'utilisateur a confirmé la suppression des fichiers
        if confirmation:
            # On définit les chemins des dossiers et fichiers à supprimer
            dossier_rap_err = 'rapport d\'erreurs'
            dossier_fich_genere = 'fichiers genere'
            dossier_fichere_mail = 'fichiers genere mail'
            dossier_stats = 'statistiques'
            # Supprimer le contenu du dossier "rapport d'erreurs"
            if os.path.exists(dossier_rap_err):
                shutil.rmtree(dossier_rap_err)
                os.makedirs(dossier_rap_err)  # Recréer le dossier vide

            # Supprimer le contenu du dossier "fichiers genere"
            if os.path.exists(dossier_fich_genere):
                shutil.rmtree(dossier_fich_genere)
                os.makedirs(dossier_fich_genere)  # Recréer le dossier vide

            # Supprimer le dossier "statistiques"
            if os.path.exists(dossier_stats):
                shutil.rmtree(dossier_stats)
                os.makedirs(dossier_stats)
            self.display_result(True)
            # si le dossier "fichiers genere mail" existe, le supprimer
            if os.path.exists(dossier_fichere_mail):
                shutil.rmtree(dossier_fichere_mail)
                os.makedirs(dossier_fichere_mail)
        # si l'utilisateur n'as pas confirmé la suppression des fichiers
        else:
            self.display_result(False)

    def display_result(self, is_deleted):
        """
        Fonction qui affiche la confirmation de suppression ou d'annulation
        :param is_deleted: Si les fichiers/données ont été supprimés
        :return:
        """
        root = tk.Tk()
        root.withdraw()

        if is_deleted:
            messagebox.showinfo("Suppression", "Tous les fichiers/données ont été supprimés.")
        else:
            messagebox.showinfo("Suppression", "Les fichiers/données n'ont pas été supprimés.")

        root.destroy()

    def recreate_file(self):
        """
        Fonction qui recrée les dossiers importants
        :return:
        """
        # Définition des chemins des dossiers et fichiers à supprimer
        dossier_rap_err = 'rapport d\'erreurs'
        dossier_fich_genere = 'fichiers genere'
        dossier_stats = 'statistiques'
        # Si le dossier n'existe pas, le créer
        if not os.path.exists(dossier_rap_err):
            os.makedirs(dossier_rap_err)  # recrée le dossier

        # Si le dossier n'existe pas, le créer
        if not os.path.exists(dossier_fich_genere):
            os.makedirs(dossier_fich_genere)  # recrée le dossier vide

        # Si le dossier n'existe pas, le créer
        if not os.path.exists(dossier_stats):
            os.makedirs(dossier_stats)  # recrée le dossier

    def generer_fichier_heure_prof(self):
        """
        Fonction pour générer le fichier d'heure par professeur
        :return:
        """
        scribe_file_prof_instance = ScribeFileProf()
        scribe_file_prof_instance.run()

    def but1_run(self):
        """
        Fonction pour lancer le programme pour le BUT1
        :return:
        """
        but1_instance = BUT1()
        but1_instance.run()

    def but2_run(self):
        """
        Fonction pour lancer le programme pour le BUT2
        """
        self.but2Instance = BUT2()
        self.but2Instance.run()

    def but3_run(self):
        """
        Fonction pour lancer le programme pour le BUT3
        """
        self.but3Instance = BUT3()
        self.but3Instance.run()


i = Utils()
i.create_main_window()
