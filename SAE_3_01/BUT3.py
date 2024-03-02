from recupdata import *
from verifdata import *
from scribedata import *
from selectfile import *


class BUT3:
    """
    Classe qui appel les fonctions nécessaires pour le BUT 3
    """
    instance = None
    insert_data_instance = None
    recup_data_instance = None
    scribe_data_instance = None
    verif_data_instance = None
    BUT3_file = None
    files = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(BUT3, cls).__new__(cls)
            cls.instance.setup()
        return cls.instance

    def setup(self):
        self.files = SelectFile()
        # On importe la maquette du BUT3
        self.BUT3_file = pd.ExcelFile(self.files.maquette_BUT3_file)

        # instance de recupData
        self.recup_data_instance = RecupData()

        # instance insertData
        self.insert_data_instance = InsertData()

        # instance verifData
        self.verif_data_instance = VerifData()

        # instance scribeData
        self.scribe_data_instance = ScribeData()

    def run(self):
        # On affiche le parcours A FA pour ensuite prendre les données
        BUT3_A_FA_file = pd.read_excel(self.BUT3_file, 'BUT 3 Parcours A FA')
        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S5_A_FA = BUT3_A_FA_file.iloc[9:27, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S5_A_FA.iterrows():
            if row.isnull().iloc[0]:
                continue
            # on insère chaque ligne dans la base de donnée
            self.insert_data_instance.insert_maquette("S5AFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                      row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recup_data_instance.trouver_val("S5AFA", "S5.A")
        self.recup_data_instance.recup_h_prof("S5AFA", "S5.A")
        # Récupérer les cours par date dans le fichier planning
        self.recup_data_instance.recup_X_et_Y("S5AFA", "S5.A")
        self.scribe_data_instance.scribeRessource("S5AFA")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verif_data_instance.concordance("S5AFA")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verif_data_instance.concordancePlanning("S5AFA")

        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S6_A_FA = BUT3_A_FA_file.iloc[32:43, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S6_A_FA.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insert_data_instance.insert_maquette("S6AFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                      row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recup_data_instance.trouver_val("S6AFA", "S6.A")
        self.recup_data_instance.recup_h_prof("S6AFA", "S6.A")
        # Récupérer les cours par date dans le fichier planning
        self.recup_data_instance.recup_X_et_Y("S6AFA", "S6.A")
        self.scribe_data_instance.scribeRessource("S6AFA")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verif_data_instance.concordance("S6AFA")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verif_data_instance.concordancePlanning("S6AFA")

        # On affiche le parcours A FI pour ensuite prendre les données
        BUT3_A_FI = pd.read_excel(self.BUT3_file, 'BUT 3 Parcours A FI')
        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S5_A_FI = BUT3_A_FI.iloc[9:27, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S5_A_FI.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insert_data_instance.insert_maquette("S5AFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                      row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recup_data_instance.trouver_val("S5AFI", "S5.A")
        self.recup_data_instance.recup_h_prof("S5AFI", "S5.A")
        # Récupérer les cours par date dans le fichier planning
        self.recup_data_instance.recup_X_et_Y("S5AFI", "S5.A")
        self.scribe_data_instance.scribeRessource("S5AFI")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verif_data_instance.concordance("S5AFI")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verif_data_instance.concordancePlanning("S5AFI")

        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S6_A_FI = BUT3_A_FI.iloc[32:42, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S6_A_FI.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insert_data_instance.insert_maquette("S6AFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                      row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recup_data_instance.trouver_val("S6AFI", "S6.A")
        self.recup_data_instance.recup_h_prof("S6AFI", "S6.A")
        # Récupérer les cours par date dans le fichier planning
        self.recup_data_instance.recup_X_et_Y("S6AFI", "S6.A")
        self.scribe_data_instance.scribeRessource("S6AFI")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verif_data_instance.concordance("S6AFI")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verif_data_instance.concordancePlanning("S6AFI")

        # On affiche le parcours B FA pour ensuite prendre les données
        BUT3_B_FA = pd.read_excel(self.BUT3_file, 'BUT 3 Parcours B FA')
        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S5_B_FA = BUT3_B_FA.iloc[9:25, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S5_B_FA.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insert_data_instance.insert_maquette("S5BFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                      row.iloc[4])

        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recup_data_instance.trouver_val("S5BFA", "S5.B")
        self.recup_data_instance.recup_h_prof("S5BFA", "S5.B")
        # Récupérer les cours par date dans le fichier planning
        self.recup_data_instance.recup_X_et_Y("S5BFA", "S5.B")
        self.scribe_data_instance.scribeRessource("S5BFA")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verif_data_instance.concordance("S5BFA")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verif_data_instance.concordancePlanning("S5BFA")

        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S6_B_FA = BUT3_B_FA.iloc[30:41, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S6_B_FA.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insert_data_instance.insert_maquette("S6BFA", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                      row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recup_data_instance.trouver_val("S6BFA", "S6.B")
        self.recup_data_instance.recup_h_prof("S6BFA", "S6.B")
        # Récupérer les cours par date dans le fichier planning
        self.recup_data_instance.recup_X_et_Y("S6BFA", "S6.B")
        self.scribe_data_instance.scribeRessource("S6BFA")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verif_data_instance.concordance("S6BFA")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verif_data_instance.concordancePlanning("S6BFA")

        # On affiche le parcours B FI pour ensuite prendre les données
        BUT3_B_FI = pd.read_excel(self.BUT3_file, 'BUT 3 Parcours B FI')
        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S5_B_FI = BUT3_B_FI.iloc[9:25, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S5_B_FI.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insert_data_instance.insert_maquette("S5BFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                      row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recup_data_instance.trouver_val("S5BFI", "S5.A")
        self.recup_data_instance.recup_h_prof("S5AFI", "S5.B")
        # Récupérer les cours par date dans le fichier planning
        self.recup_data_instance.recup_X_et_Y("S5BFI", "S5.B")
        self.scribe_data_instance.scribeRessource("S5BFI")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verif_data_instance.concordance("S5BFI")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verif_data_instance.concordancePlanning("S5BFI")

        # On récupère les lignes et colonnes utiles
        select_colonne_BUT3_S6_B_FI = BUT3_B_FI.iloc[30:40, [0, 2, 17, 18, 19]]
        for index, row in select_colonne_BUT3_S6_B_FI.iterrows():
            if row.isnull().iloc[0]:
                continue
            self.insert_data_instance.insert_maquette("S6BFI", row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3],
                                                      row.iloc[4])
        # fonction pour récupérer les valeurs du premier semestre dans le fichier planning
        self.recup_data_instance.trouver_val("S6BFI", "S6.B")
        self.recup_data_instance.recup_h_prof("S6BFI", "S6.B")
        # Récupérer les cours par date dans le fichier planning
        self.recup_data_instance.recup_X_et_Y("S6BFI", "S6.B")
        self.scribe_data_instance.scribeRessource("S6BFI")
        # fonction pour vérifier les concordances entre le fichier planning et le fichier maquette nationnal à partir de
        # la base de données pour le premier semestre
        self.verif_data_instance.concordance("S6BFI")
        # Vérifie la concordance entre les heures écrite et les heures placés dans le fichier planning
        self.verif_data_instance.concordancePlanning("S6BFI")
        print(self.verif_data_instance.getNbErreur())

# i = BUT3()
# i.run()
