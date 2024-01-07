from scribeData import *
from verifData import *
from recupData import *
from insertData import *
import pandas as pd


class BUT1:
    """
    Classe qui appel les fonctions nécessaires pour le BUT 1
    """
    instance = None
    insertDataInstance = None
    recupDataInstance = None
    scribeDataInstance = None
    verifDataInstance = None
    BUT1file = None
    BUT1_1file = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(BUT1, cls).__new__(cls)
            cls.instance.setup()
        return cls.instance

    def setup(self):
        """
        "Setup" l'objet : créer les instances, initialise les fichiers...
        :return:
        """
        # lire le fichier maquette
        self.BUT1file = pd.ExcelFile('Documents/BUT1_INFO_AIX.xlsx')
        # récupérer l'onglet BUT 1
        self.BUT1_1file = pd.read_excel(self.BUT1file, 'BUT 1')
        # instance de recupData
        self.recupDataInstance = recupData()
        # instance insertData
        self.insertDataInstance = insertData()
        # instance verifData
        self.verifDataInstance = verifData()
        # instance scribeData
        self.scribeDataInstance = scribeData()

    def run(self):
        # Sélection des heures du premier semestre
        select_colonne_BUT1_S1 = self.BUT1_1file.iloc[10:31, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT1_S1.iterrows():
            if row.isnull().iloc[0]:
                continue
            # on insère chaque ligne dans la base de donnée
            self.insertDataInstance.insert_maquette("S1", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S1", "S1")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette national à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S1")
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S1", "S1")
        # écrire les informations du S1
        self.scribeDataInstance.scribeRessource("S1")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S1", "S1")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S1")

        # Sélection des heures du deuxième semestre
        select_colonne_BUT1_S2 = self.BUT1_1file.iloc[36:58, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT1_S2.iterrows():
            if row.isnull().iloc[0]:
                continue
            # on insère chaque ligne dans la base de donnée
            self.insertDataInstance.insert_maquette("S2", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du deuxième semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S2", "S2")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le deuxième semestre
        self.verifDataInstance.concordance("S2")
        # fonction pour récupérer les valeurs du deuxième semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S2", "S2")
        # écrire les informations du S2
        self.scribeDataInstance.scribeRessource("S2")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S2", "S2")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S2")
