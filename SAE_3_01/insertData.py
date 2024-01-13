import sqlite3
import math
import pandas as pd


class insertData:
    """
    Classe permettant d'insérer des données dans la base de données
    """
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(insertData, cls).__new__(cls)
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

    def insert_maquette(self, Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP):
        """
        Fonction qui insère les données dans la base de données "Maquette"
        :param Semestre:
        :param Code_ressource:
        :param Libelle:
        :param H_CM:
        :param H_TD:
        :param H_TP:
        :return:
        """
        # création d'un id unique pour chaque semestre par ressource
        id_res_formation = Semestre + Code_ressource
        espace = Libelle.index(" ")
        # récupération de seulement le numéro de la ressource sans le nom de la ressource
        num_ressource = Libelle[:espace]
        # éxécution de la requête SQL pour vérifier s'il existe déjà dans la BD la ressource pour un semestre précis
        self.cursor.execute("SELECT * FROM Maquette WHERE id_res_formation = ?", (id_res_formation,))
        existing_row = self.cursor.fetchone()
        # si la requête renvoie quelque chose on update au lieu d'insérer
        if existing_row:
            print(Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP)
            self.cursor.execute(
                "UPDATE Maquette SET Code_ressource = ?, Semestre = ?, Libelle = ?, H_CM = ?, H_TD = ?, H_TP = ?, "
                "Num_Res = ? WHERE id_res_formation = ?",
                (Code_ressource, Semestre, Libelle, H_CM, H_TD, H_TP, num_ressource, id_res_formation)
            )
            self.conn.commit()
        # sinon on insère au lieu d'update
        else:
            self.cursor.execute(
                "INSERT INTO Maquette (id_res_formation, Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP, "
                "Num_Res) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (id_res_formation, Semestre, Code_ressource, Libelle, H_CM, H_TD, H_TP, num_ressource))
            # commit les changements pour les sauvegarder dans la base de données
            self.conn.commit()

    def insert_planning(self, Semestre, Ressource, H_CM, H_TD, H_TP, Resp):
        """
        Fonction qui insère les données dans la base de données "Planning"
        :param Semestre:
        :param Ressource:
        :param H_CM:
        :param H_TD:
        :param H_TP:
        :param Resp:
        :return:
        """
        # éxécution de la requête SQL pour vérifier si il existe déjà dans la BD la ressource pour un semestre précis
        self.cursor.execute("SELECT Semestre FROM Planning WHERE Semestre = ? AND Ressource = ?",
                            (Semestre, Ressource,))
        existing_row = self.cursor.fetchone()
        espace = Ressource.index(" ")
        # récupération de seulement le numéro de la ressource sans le nom de la ressource
        num_ressource = Ressource[:espace]
        # si la requête renvoie quelque chose on update au lieu d'insérer
        if existing_row:
            self.cursor.execute(
                "UPDATE Planning SET H_CM = ?, H_TD = ?, H_TP = ?, Resp = ?, Num_res = ? WHERE Semestre = ? AND "
                "Ressource = ?",
                (H_CM, H_TD, H_TP, Resp, num_ressource, Semestre, Ressource))
            self.conn.commit()
        # sinon on insère au lieu d'update
        else:
            self.cursor.execute(
                "INSERT INTO Planning (Semestre, Ressource, H_CM, H_TD, H_TP, Resp, Num_res) VALUES (?, ?, ?, ?, ?, "
                "?, ?)",
                (Semestre, Ressource, H_CM, H_TD, H_TP, Resp, num_ressource))
            # commit les changements pour les sauvegarder dans la base de données
            self.conn.commit()

    def insertNombreHeureProf(self):
        '''
        Écrire dans un fichier, le nombre d'heures totales de chaque professeur
        :return:
        '''
        # réinitialiser le nombre d'heures à 0
        self.cursor.execute("UPDATE HoraireTotalProf SET H_CM = 0, H_TD = 0, H_TP_D = 0, H_TP_ND = 0, H_TEST = 0")
        self.conn.commit()
        dictProf = {}
        hCMPActuel = hTDPActuel = hTPDPActuel = hTPNDPActuel = hTestPActuel = 0
        # récupération des données utiles
        self.cursor.execute(
            "SELECT HoraireProf.Ressource, Intervenant, CM, TD, TP_Non_Dedoubles, NbCours, Type_Cours, Test, "
            "TP_Dedoubles FROM HoraireProf "
            "JOIN Horaires "
            "ON SUBSTR(HoraireProf.Ressource, 1, INSTR(HoraireProf.Ressource, ' ') - 1) = Horaires.Ressource")
        profs = self.cursor.fetchall()
        for pr in profs:
            # ajout des heures total pour chaque type de cours (sur chaque ressources)
            hCMPActuel = hTDPActuel = hTPDPActuel = hTPNDPActuel = hTestPActuel = 0
            if pr[2] is not None and pr[6] == 'Amphi':
                hCMPActuel = pr[2] * pr[5]
            if pr[3] is not None and pr[6] == 'TD':
                hTDPActuel = pr[3] * pr[5]
            if pr[4] is not None and pr[6] == 'TP':
                hTPDPActuel = pr[4] * pr[5]
            if pr[8] is not None and pr[6] == 'TP':
                hTPNDPActuel = pr[8] * pr[5]
            if pr[7] is not None and pr[6] == 'Test':
                hTestPActuel = pr[7] * pr[5]
            # éxécution d'une requete pour savoir si le prof existe déjà dans la BD
            self.cursor.execute("SELECT Prof FROM HoraireTotalProf WHERE Prof = ?", (pr[1],))
            alreadyExist = self.cursor.fetchall()
            # si il existe on insère
            if alreadyExist:
                self.cursor.execute(
                    "UPDATE HoraireTotalProf "
                    "SET H_CM = H_CM + ?, H_TD = H_TD + ?, H_TP_D = H_TP_D + ?, H_TP_ND = H_TP_ND + ?, "
                    "H_TEST = H_TEST + ? WHERE Prof = ?",
                    (hCMPActuel, hTDPActuel, hTPDPActuel, hTPNDPActuel, hTestPActuel, pr[1]))
                self.conn.commit()
            # sinon, on update
            else:
                self.cursor.execute(
                    "INSERT INTO HoraireTotalProf (H_CM, H_TD, H_TP_D, H_TP_ND, H_TEST, Prof) VALUES (?, ?, ?,"
                    " ?, ?, ?)", (hCMPActuel, hTDPActuel, hTPDPActuel, hTPNDPActuel, hTestPActuel,
                                  pr[1]))
                self.conn.commit()

i = insertData()
i.insertNombreHeureProf()