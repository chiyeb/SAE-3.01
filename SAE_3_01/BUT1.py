from scribedata import *
from verifdata import *
from recupdata import *
from insertdata import *
import pandas as pd
from selectfile import *


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
    files = None

    def __new__(cls, mode='defaut'):
        if cls.instance is None:
            cls.instance = super(BUT1, cls).__new__(cls)
            cls.instance.setup(mode)
        return cls.instance

    def setup(self, mode):
        """
        "Setup" l'objet : créer les instances, initialise les fichiers...
        :return:
        """
        if mode == 'defaut':
            self.files = SelectFile()
        else:
            self.files = SelectFile('utils')
        # lire le fichier maquette
        self.BUT1file = pd.ExcelFile(self.files.maquette_BUT1_file)
        # récupérer l'onglet BUT 1
        self.BUT1_1file = pd.read_excel(self.BUT1file, 'BUT 1')
        # instance de recupData
        self.recupDataInstance = RecupData()
        # instance insertData
        self.insertDataInstance = InsertData()
        # instance verifData
        self.verifDataInstance = VerifData()
        # instance scribeData
        self.scribeDataInstance = ScribeData()

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
        self.recupDataInstance.trouver_val("S1", "S1")
        self.recupDataInstance.recup_h_prof("S1", "S1")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recup_X_et_Y("S1", "S1")
        # écrire les informations du S1
        self.scribeDataInstance.scribeRessource("S1")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S1")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette national à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S1")
        # Sélection des heures du deuxième semestre
        select_colonne_BUT1_S2 = self.BUT1_1file.iloc[36:58, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT1_S2.iterrows():
            if row.isnull().iloc[0]:
                continue
            # on insère chaque ligne dans la base de donnée
            self.insertDataInstance.insert_maquette("S2", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du deuxième semestre dans le fichier planning
        self.recupDataInstance.trouver_val("S2", "S2")
        self.recupDataInstance.recup_h_prof("S2", "S2")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recup_X_et_Y("S2", "S2")
        # écrire les informations du S2
        self.scribeDataInstance.scribeRessource("S2")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le deuxième semestre
        self.verifDataInstance.concordance("S2")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S2")


if __name__ == "__main__":
    but = BUT1()
    but.run()

