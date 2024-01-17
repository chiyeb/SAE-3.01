import pandas as pd
from insertData import *
from recupData import *
from verifData import *
from scribeData import *
from selectFile import *


class BUT3:
    """
    Classe qui appel les fonctions nécessaires pour le BUT 3
    """
    instance = None
    insertDataInstance = None
    recupDataInstance = None
    scribeDataInstance = None
    verifDataInstance = None
    BUT3_file = None
    files = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(BUT3, cls).__new__(cls)
            cls.instance.setup()
        return cls.instance

    def setup(self):
        self.files = selectFile()
        # On importe la maquette du BUT3
        self.BUT3_file = pd.ExcelFile(self.files.maquette_BUT3_file)

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
        BUT3_A_FA_file = pd.read_excel(self.BUT3_file, 'BUT 3 Parcours A FA')
        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S5_A_FA = BUT3_A_FA_file.iloc[9:27, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S5_A_FA.iterrows():
            if row.isnull().iloc[0]:
                continue
            # on insère chaque ligne dans la base de donnée
            self.insertDataInstance.insert_maquette("S5AFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S5AFA", "S5.A")
        self.recupDataInstance.recupHProf("S5AFA", "S5.A")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S5AFA", "S5.A")
        self.scribeDataInstance.scribeRessource("S5AFA")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S5AFA")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S5AFA")

        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S6_A_FA = BUT3_A_FA_file.iloc[32:43, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S6_A_FA.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insertDataInstance.insert_maquette("S6AFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S6AFA", "S6.A")
        self.recupDataInstance.recupHProf("S6AFA", "S6.A")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S6AFA", "S6.A")
        self.scribeDataInstance.scribeRessource("S6AFA")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S6AFA")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S6AFA")


        # On affiche le parcours A FI pour ensuite prendre les données 
        BUT3_A_FI = pd.read_excel(self.BUT3_file, 'BUT 3 Parcours A FI')
        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S5_A_FI = BUT3_A_FI.iloc[9:27, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S5_A_FI.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insertDataInstance.insert_maquette("S5AFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S5AFI", "S5.A")
        self.recupDataInstance.recupHProf("S5AFI", "S5.A")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S5AFI", "S5.A")
        self.scribeDataInstance.scribeRessource("S5AFI")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S5AFI")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S5AFI")


        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S6_A_FI = BUT3_A_FI.iloc[32:42, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S6_A_FI.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insertDataInstance.insert_maquette("S6AFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S6AFI", "S6.A")
        self.recupDataInstance.recupHProf("S6AFI", "S6.A")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S6AFI", "S6.A")
        self.scribeDataInstance.scribeRessource("S6AFI")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S6AFI")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S6AFI")


        # On affiche le parcours B FA pour ensuite prendre les données 
        BUT3_B_FA = pd.read_excel(self.BUT3_file, 'BUT 3 Parcours B FA')
        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S5_B_FA = BUT3_B_FA.iloc[9:25, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S5_B_FA.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insertDataInstance.insert_maquette("S5BFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])

        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S5BFA", "S5.B")
        self.recupDataInstance.recupHProf("S5BFA", "S5.B")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S5BFA", "S5.B")
        self.scribeDataInstance.scribeRessource("S5BFA")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S5BFA")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S5BFA")


        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S6_B_FA = BUT3_B_FA.iloc[30:41, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S6_B_FA.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insertDataInstance.insert_maquette("S6BFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S6BFA", "S6.B")
        self.recupDataInstance.recupHProf("S6BFA", "S6.B")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S6BFA", "S6.B")
        self.scribeDataInstance.scribeRessource("S6BFA")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S6BFA")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S6BFA")

        # On affiche le parcours B FI pour ensuite prendre les données
        BUT3_B_FI = pd.read_excel(self.BUT3_file, 'BUT 3 Parcours B FI')
        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S5_B_FI = BUT3_B_FI.iloc[9:25, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S5_B_FI.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insertDataInstance.insert_maquette("S5BFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S5BFI", "S5.A")
        self.recupDataInstance.recupHProf("S5AFI", "S5.B")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S5BFI", "S5.B")
        self.scribeDataInstance.scribeRessource("S5BFI")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S5BFI")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S5BFI")


        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S6_B_FI = BUT3_B_FI.iloc[30:40, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S6_B_FI.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insertDataInstance.insert_maquette("S6BFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                    row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recupDataInstance.trouverVal("S6BFI", "S6.B")
        self.recupDataInstance.recupHProf("S6BFI", "S6.B")
        # Récupérer les cours par date dans le fichier planning
        self.recupDataInstance.recupXetY("S6BFI", "S6.B")
        self.scribeDataInstance.scribeRessource("S6BFI")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verifDataInstance.concordance("S6BFI")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verifDataInstance.concordancePlanning("S6BFI")
        print(self.verifDataInstance.getNbErreur())

# i = BUT3()
# i.run()
