import os

from BUT1 import BUT1
from BUT2 import BUT2
from BUT3 import BUT3
from recupdata import RecupData
from scribedata import ScribeData
from selectfile import SelectFile
from verifdata import VerifData

print("Début du programme\nVeuillez patienter...")
print("Instantiation des classes...")
recupDataInstance = RecupData()
recupDataInstance.recup_nom_prof()
print("Classes instanciées")
print("Lancement du programme pour le BUT1")
BUT1_instance = BUT1()
BUT1_instance.run()
print("Lancement du programme pour le BUT2")
BUT2_instance = BUT2()
BUT2_instance.run()
print("Lancement du programme pour le BUT3")
BUT3_instance = BUT3()
BUT3_instance.run()

verifdata_instance = VerifData()
verifdata_instance.renom_fichier_avec_nb_erreur()

#stats = Stats()
#stats.execAllStats()
