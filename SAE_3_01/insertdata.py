import os
import sqlite3


class InsertData:
    """
    Classe permettant d'insérer des données dans la base de données
    """
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(InsertData, cls).__new__(cls)
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
        :param Semestre: Le semestre de la ressource à insérer
        :param Code_ressource: Le code de la ressource à insérer
        :param Libelle: Le libellé de la ressource à insérer
        :param H_CM: Le nombre d'heures de CM de la ressource à insérer
        :param H_TD: Le nombre d'heures de TD de la ressource à insérer
        :param H_TP: Le nombre d'heures de TP de la ressource à insérer
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

    def insert_planning(self, semestre, ressource, H_CM, H_TD, H_TP, resp):
        """
        Fonction qui insère les données dans la base de données "Planning"
        :param semestre: Le semestre de la ressource à insérer
        :param ressource: Le libellé de la ressource à insérer
        :param H_CM: Le nombre d'heures de CM de la ressource à insérer
        :param H_TD: Le nombre d'heures de TD de la ressource à insérer
        :param H_TP: Le nombre d'heures de TP de la ressource à insérer
        :param resp: Le nom du responsable de la ressource à insérer
        :return:
        """
        # éxécution de la requête SQL pour vérifier si il existe déjà dans la BD la ressource pour un semestre précis
        self.cursor.execute("SELECT Semestre FROM Planning WHERE Semestre = ? AND Ressource = ?",
                            (semestre, ressource,))
        existing_row = self.cursor.fetchone()
        espace = ressource.index(" ")
        # récupération de seulement le numéro de la ressource sans le nom de la ressource
        num_ressource = ressource[:espace]
        # si la requête renvoie quelque chose on update au lieu d'insérer
        if existing_row:
            self.cursor.execute(
                "UPDATE Planning SET H_CM = ?, H_TD = ?, H_TP = ?, Resp = ?, Num_res = ? WHERE Semestre = ? AND "
                "Ressource = ?",
                (H_CM, H_TD, H_TP, resp, num_ressource, semestre, ressource))
            self.conn.commit()
        # sinon on insère au lieu d'update
        else:
            self.cursor.execute(
                "INSERT INTO Planning (Semestre, Ressource, H_CM, H_TD, H_TP, Resp, Num_res) VALUES (?, ?, ?, ?, ?, "
                "?, ?)",
                (semestre, ressource, H_CM, H_TD, H_TP, resp, num_ressource))
            # commit les changements pour les sauvegarder dans la base de données
            self.conn.commit()

    def insert_nombre_heure_prof(self):
        '''
        Écrire dans un fichier, le nombre d'heures totales de chaque professeur
        :return:
        '''
        # réinitialiser le nombre d'heures à 0
        self.cursor.execute("UPDATE HoraireTotalProf SET H_CM = 0, H_TD = 0, H_TP_D = 0, H_TP_ND = 0, H_TEST = 0")
        self.conn.commit()
        # récupération des données utiles
        self.cursor.execute(
            "SELECT HoraireProf.Ressource, Intervenant, CM, TD, TP_Non_Dedoubles, NbCours, Type_Cours, Test, "
            "TP_Dedoubles FROM HoraireProf "
            "JOIN Horaires "
            "ON HoraireProf.Ressource = Horaires.Ressource")
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
            already_exist = self.cursor.fetchall()
            # si il existe on update
            if already_exist:
                self.cursor.execute(
                    "UPDATE HoraireTotalProf "
                    "SET H_CM = H_CM + ?, H_TD = H_TD + ?, H_TP_D = H_TP_D + ?, H_TP_ND = H_TP_ND + ?, "
                    "H_TEST = H_TEST + ? WHERE Prof = ?",
                    (hCMPActuel, hTDPActuel, hTPDPActuel, hTPNDPActuel, hTestPActuel, pr[1]))
                self.conn.commit()
            # sinon, on insère
            else:
                self.cursor.execute(
                    "INSERT INTO HoraireTotalProf (H_CM, H_TD, H_TP_D, H_TP_ND, H_TEST, Prof) VALUES (?, ?, ?,"
                    " ?, ?, ?)", (hCMPActuel, hTDPActuel, hTPDPActuel, hTPNDPActuel, hTestPActuel,
                                  pr[1]))
                self.conn.commit()
