import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


class Stats:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(Stats, cls).__new__(cls)
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

    def execAllStats(self):
        """
        Exécute chaque fonction pour les statistiques
        :return:
        """
        self.genereGraph()
        self.generePie()

    def genereGraph(self):
        """
        Fonction qui génère un graphique
        :return:
        """
        # Récupération des heures par ressources et par semestre
        requete = """
        SELECT Semestre, Num_res, SUM(H_CM + H_TD + H_TP) as HTotal
        FROM Planning
        GROUP BY Semestre, Ressource
        ORDER BY Semestre, HTotal DESC;
        """
        data = pd.read_sql_query(requete, self.conn)

        # Génère le graphique
        plt.figure(figsize=(15, 10))
        for semestre in data['Semestre'].unique():
            subset = data[data['Semestre'] == semestre]
            plt.bar(subset['Num_res'], subset['HTotal'], label=semestre)

        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Ressource')
        plt.ylabel('Heure total')
        plt.title('Heure total par ressources et par semestre')
        plt.legend(title='Semestre')
        plt.tight_layout()
        # Si aucun dossier "statistiques" alors on en crée un
        if not os.path.exists('statistiques'):
            os.makedirs('statistiques')

        # Enregistrement du graphique
        plt.savefig('statistiques/ressources_par_semestre.jpg', format='jpg')
        plt.close()

    def generePie(self):
        """
        Fonction qui génère un camembert
        :return:
        """
        # Récupération des heures pour chaque enseignant
        requete = """
        SELECT Resp, SUM(H_CM + H_TD + H_TP) as HTotal
        FROM Planning
        GROUP BY Resp;
        """
        data = pd.read_sql_query(requete, self.conn)

        # Génère le graphique en camembert
        plt.figure(figsize=(10, 10))
        plt.pie(data['HTotal'], labels=data['Resp'], autopct='%1.1f%%', startangle=140)
        plt.title('Répartition des Heures par Responsable')
        plt.axis('equal')

        # Si aucun dossier "statistiques" alors, on en crée un
        if not os.path.exists('statistiques'):
            os.makedirs('statistiques')

        # Enregistrement du graphique
        plt.savefig('statistiques/heures_par_responsable.jpg', format='jpg')
        plt.close()

    def __del__(self):
        """
            Fonction qui ferme la connexion à la BD
            :param self:
            :return:
            """
        self.conn.close()

