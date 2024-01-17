import pandas as pd
# from SAE_3_01.old.database_handler import insert_maquette
from scribeData import *
from recupData import *
from verifData import *
from insertData import *
from selectFile import *


class BUT2:
    """
    Classe qui appel les fonctions nécessaires pour le BUT 2
    """
    instance = None
    verifDataInstance = None
    scribeDataInstance = None
    insertDataInstance = None
    recupDataInstance = None
    BUT2_file = None
    files = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(BUT2, cls).__new__(cls)
            cls.instance.setup()
        return cls.instance

    def setup(self):
        self.files = selectFile()
        # On importe la bible BUT2
        self.BUT2_file = pd.ExcelFile(self.files.maquette_BUT2_file)

        # instance de recupData
        self.recupDataInstance = recupData()

        # instance insertData
        self.insertDataInstance = insertData()

        # instance verifData
        self.verifDataInstance = verifData()

        # instance scribeData
        self.scribeDataInstance = scribeData()

    def run(self):
        # On affiche le parcours A FA pour ensuite prendre les données
        BUT2_A_FA_file = pd.read_excel(self.BUT2_file, 'BUT 2 Parcours A FA')
        # On récupère les lignes et colonnes utiles
        select_colonne_BUT2_S3_A_FA = BUT2_A_FA_file.iloc[11:29, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT2_S3_A_FA.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insertDataInstance.insert_maquette("S3AFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S3AFA", "S3")
        self.recupDataInstance.recupHProf("S3AFA", "S3")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S3AFA", "S3")
        self.scribeDataInstance.scribeRessource("S3AFA")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette national à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S3AFA")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S3AFA")

        select_colonne_BUT2_S4_A_FA = BUT2_A_FA_file.iloc[34:51, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT2_S4_A_FA.iterrows():
            if row.isnull().iloc[0]:
                continue
            # on insère chaque ligne dans la base de donnée
            print("tesr")
            self.insertDataInstance.insert_maquette("S4AFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S4AFA", "S4.A")
        self.recupDataInstance.recupHProf("S4AFA", "S4.A")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S4AFA", "S4.A")
        self.scribeDataInstance.scribeRessource("S4AFA")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S4AFA")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S4AFA")

        # On affiche le parcours A FI pour ensuite prendre les données
        BUT2_A_FI = pd.read_excel(self.BUT2_file, 'BUT 2 Parcours A FI')
        # On récupère les lignes et colonnes utiles
        select_colonne_BUT2_S3_A_FI = BUT2_A_FI.iloc[11:29, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT2_S3_A_FI.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insertDataInstance.insert_maquette("S3AFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S3AFI", "S3")
        self.recupDataInstance.recupHProf("S3AFI", "S3")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S3AFI", "S3")
        self.scribeDataInstance.scribeRessource("S3AFI")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S3AFI")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S3AFI")

        # On récupère les lignes et colonnes utiles
        select_colonne_BUT2_S4_A_FI = BUT2_A_FI.iloc[34:51, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT2_S4_A_FI.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insertDataInstance.insert_maquette("S4AFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S4AFI", "S4.A")
        self.recupDataInstance.recupHProf("S4AFI", "S4.A")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S4AFI", "S4.A")
        self.scribeDataInstance.scribeRessource("S4AFI")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S4AFI")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S4AFI")

        # On affiche le parcours B FA pour ensuite prendre les données
        BUT2_B_FA = pd.read_excel(self.BUT2_file, 'BUT 2 Parcours B FA')
        # On récupère les lignes et colonnes utiles
        select_colonne_BUT2_S3_B_FA = BUT2_B_FA.iloc[11:29, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT2_S3_B_FA.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insertDataInstance.insert_maquette("S3BFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S3BFA", "S3")
        self.recupDataInstance.recupHProf("S3BFA", "S3")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S3BFA", "S3")
        self.scribeDataInstance.scribeRessource("S3BFA")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S3BFA")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S3BFA")

        # On récupère les lignes et colonnes utiles
        select_colonne_BUT2_S4_B_FA = BUT2_B_FA.iloc[34:51, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT2_S4_B_FA.iterrows():

            if row.isnull().iloc[0]:
                continue
            self.insertDataInstance.insert_maquette("S4BFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S4BFA", "S4.B")
        self.recupDataInstance.recupHProf("S4BFA", "S4.B")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S4BFA", "S4.B")
        self.scribeDataInstance.scribeRessource("S4BFA")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S4BFA")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S4BFA")

        # On affiche le parcours B FI pour ensuite prendre les données
        BUT2_B_FI = pd.read_excel(self.BUT2_file, 'BUT 2 Parcours B FI')
        # On récupère les lignes et colonnes utiles
        select_colonne_BUT2_S3_B_FI = BUT2_B_FI.iloc[10:28, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT2_S3_B_FI.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insertDataInstance.insert_maquette("S3BFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S3BFI", "S3")
        self.recupDataInstance.recupHProf("S3BFI", "S3")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S3BFI", "S3")
        self.scribeDataInstance.scribeRessource("S3BFI")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S3BFI")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S3BFI")

        # On récupère les lignes et colonnes utiles
        select_colonne_BUT2_S4_B_FI = BUT2_B_FI.iloc[33:50, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT2_S4_B_FI.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insertDataInstance.insert_maquette("S4BFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S4BFI", "S4.B")
        self.recupDataInstance.recupHProf("S4BFI", "S4.B")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S4BFI", "S4.B")
        self.scribeDataInstance.scribeRessource("S4BFI")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S4BFI")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S4BFI")

# i = BUT2()
# i.run()
