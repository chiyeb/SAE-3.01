import pandas as pd

from ADEClass import *

import BUT1
import BUT2
import BUT3

# importer le fichier excel
planning = pd.ExcelFile('./Planning 2023-2024.xlsx')

# S2

# lire l'onglet du S2
S2 = pd.read_excel(planning, 'S2')

# récupérer la maquette des heures de chaque ressource
heures_S2_1 = S2.iloc[26:32, [3, 6, 8, 10]]
heures_S2_2 = S2.iloc[26:34, [36, 39, 41, 43]]

# remplacer les cases vides par des '0'
heures_S2_1 = heures_S2_1.fillna(0)
heures_S2_2 = heures_S2_2.fillna(0)

#print(heures_S2_1)
#print(heures_S2_2)

# fonction qui crée une liste d'objets de classe ADEClass (chaque objet est une ressource avec ses heures respectives)
def liste_heures(liste_heures, heures):
    for index, row in heures.iterrows():
        if row.isnull().iloc[0]:
            continue
        # On crée un objet ADE et on rentre les valeurs pour chaque ligne
        ADE = ADEClass(None, row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3])
        liste_heures.append(ADE)

# créer une liste avec la fonction "liste_heures" pour le S2
liste_heures_S2 = []
liste_heures(liste_heures_S2, heures_S2_1)
liste_heures(liste_heures_S2, heures_S2_2)

# fonction qui vérifie que la maquette du planning corresponde bien à celle originale
def concordance(planning, maquette, semestre):
    print("Concordance pour le", semestre, ":")
    cpt = 0
    for i in range(len(planning)):
        if not(planning[i].getLibelle() in maquette[i].getLibelle()):
            print("La ressource numéro", i+1, "n'existe pas ou n'a pas été placé au bon endroit.")
        else:
            if planning[i].getCm() != maquette[i].getCm():
                print("Les heures de C.M. de la ressource numéro", i+1, "ne correspondent pas entre le fichier de la maquette et celui du planning.")
            if planning[i].getTd() != maquette[i].getTd():
                print("Les heures de T.D. de la ressource numéro", i+1, "ne correspondent pas entre le fichier de la maquette et celui du planning.")
            if planning[i].getTp() != maquette[i].getTp():
                print("Les heures de T.P. de la ressource numéro", i+1, "ne correspondent pas entre le fichier de la maquette et celui du planning.")
            if planning[i].getCm() == maquette[i].getCm() and planning[i].getTd() == maquette[i].getTd() and planning[i].getTp() == maquette[i].getTp():
                print("Tout concorde pour la ressource numéro", i+1)
                cpt += 1
    return cpt == len(planning)


#print(concordance(liste_heures_S1, BUT1.liste_adeS1, "S1"))
print(concordance(liste_heures_S2, BUT1.liste_adeS2, "S2"))