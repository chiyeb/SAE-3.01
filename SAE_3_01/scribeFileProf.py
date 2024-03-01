from recupData import *
from insertData import *
from scribeData import *


class scribeFileProf:
    """
    Classe qui s'occupe de lancer les différents scripts pour le fichier Professeurs_Horaires.xlsx
    """

    def __init__(self):
        """
        Constructeur de la classe
        """
        pass

    def run(self):
        """
        Méthode qui lance les différents scripts pour le fichier Professeurs_Horaires.xlsx
        :return:
        """
        print("Début du programme, veuillez patienter...")
        # on instancie les classes pour pouvoir les utiliser
        recupDataInstance = recupData()
        insertDataInstance = insertData()
        scribeDataInstance = scribeData()
        print("Classes instanciées")
        print("Récupération des valeurs dans les fichiers générés")
        valeurs_recuperes = recupDataInstance.recuperer_valeurs_dans_fichier_genere()
        print("Valeurs récupérées")
        # Insérer les valeurs récupérées dans la base de données
        print("Insertion des valeurs récupérées dans la base de données")
        insertDataInstance.insert_data_from_fichier_generer(valeurs_recuperes)
        print("Valeurs insérées")
        # Afficher les valeurs récupérées pour chaque fichier
        # for valeurs_fichier in valeurs_recuperes:
        #     for fichier, onglet, valeur_case, valeurs_onglet in valeurs_fichier:
        #         print(f"Nom du fichier : {os.path.splitext(fichier)[0]}")
        #         print(f"Onglet : {onglet}")
        #         print("Valeur de la ligne 2, colonne 2 :", valeur_case)
        #         for ligne in valeurs_onglet:
        #             print("Valeurs de la ligne:", ligne)
        #         print()

        # Écrire les valeurs récupérées dans le fichier de destination
        print("Écriture des valeurs récupérées dans le fichier de destination")
        scribeDataInstance.write_data_to_excel("fichiers genere/Professeurs_Horaires.xlsx")
        print("Valeurs écrites")


if __name__ == "__main__":
    scribe_prof = scribeFileProf()
    scribe_prof.run()
