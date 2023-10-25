import pandas as pd

from ADEClass import *

import BUT1
import BUT2
import BUT3

# importer le fichier excel
planning = pd.ExcelFile('./Planning 2023-2024.xlsx')

# fonction qui crée une liste d'objets de classe ADEClass (chaque objet est une ressource avec ses heures respectives)
def liste_heures(liste_heures, heures):
    for index, row in heures.iterrows():
        if row.isnull().iloc[0]:
            continue
        # On crée un objet ADE et on rentre les valeurs pour chaque ligne
        ADE = ADEClass(None, row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3])
        liste_heures.append(ADE)

# fonction qui vérifie que la maquette du planning corresponde bien à celle originale
def concordance(planning, maquette, semestre):
    print("Concordance pour le", semestre, ":")
    cpt = 0
    for i in range(len(planning)):
        if not(planning[i].getLibelle() in maquette[i].getLibelle()):
            print("La ressource numéro", planning[i].getLibelle(), "n'existe pas ou n'a pas été placé au bon endroit.")
        else:
            if planning[i].getCm() != maquette[i].getCm():
                print("Les heures de C.M. de la ressource", planning[i].getLibelle(), "ne correspondent pas entre le fichier de la maquette et celui du planning.")
            if planning[i].getTd() != maquette[i].getTd():
                print("Les heures de T.D. de la ressource", planning[i].getLibelle(), "ne correspondent pas entre le fichier de la maquette et celui du planning.")
            if planning[i].getTp() != maquette[i].getTp():
                print("Les heures de T.P. de la ressource", planning[i].getLibelle(), "ne correspondent pas entre le fichier de la maquette et celui du planning.")
            if planning[i].getCm() == maquette[i].getCm() and planning[i].getTd() == maquette[i].getTd() and planning[i].getTp() == maquette[i].getTp():
                print("Tout concorde pour la ressource", planning[i].getLibelle())
                cpt += 1
    return cpt == len(planning)

# S1

# lire l'onglet du S1
S1 = pd.read_excel(planning, 'S1')

# récupérer la maquette des heures de chaque ressource
heures_S1_1 = S1.iloc[25:30, [3, 6, 8, 10]]
heures_S1_2 = S1.iloc[25:33, [35, 38, 40, 42]]

# remplacer les cases vides par des '0'
heures_S1_1 = heures_S1_1.fillna(0)
heures_S1_2 = heures_S1_2.fillna(0)

# créer une liste avec la fonction "liste_heures" pour le S1
liste_heures_S1 = []
liste_heures(liste_heures_S1, heures_S1_1)
liste_heures(liste_heures_S1, heures_S1_2)

# fusionner les lignes de R1.06-1 avec R1.06-2 en additionnant les heures des 2 lignes
liste_heures_S1[5].setLibelle("R1.06")
liste_heures_S1[5].setCm(liste_heures_S1[5].getCm() + liste_heures_S1[6].getCm())
liste_heures_S1[5].setTd(liste_heures_S1[5].getTd() + liste_heures_S1[6].getTd())
liste_heures_S1[5].setTp(liste_heures_S1[5].getTp() + liste_heures_S1[6].getTp())
del liste_heures_S1[6]

print(concordance(liste_heures_S1, BUT1.liste_adeS1, "S1"), "\n")

# S2

# lire l'onglet du S2
S2 = pd.read_excel(planning, 'S2')

# récupérer la maquette des heures de chaque ressource
heures_S2_1 = S2.iloc[26:32, [3, 6, 8, 10]]
heures_S2_2 = S2.iloc[26:34, [36, 39, 41, 43]]

# remplacer les cases vides par des '0'
heures_S2_1 = heures_S2_1.fillna(0)
heures_S2_2 = heures_S2_2.fillna(0)

# créer une liste avec la fonction "liste_heures" pour le S2
liste_heures_S2 = []
liste_heures(liste_heures_S2, heures_S2_1)
liste_heures(liste_heures_S2, heures_S2_2)

print(concordance(liste_heures_S2, BUT1.liste_adeS2, "S2"), "\n")

# S3

# lire l'onglet du S3
S3 = pd.read_excel(planning, 'S3')

# Parcours A

# récupérer la maquette des heures de chaque ressource
heures_S3_A_1 = S3.iloc[29:36, [3, 6, 8, 10]]
heures_S3_A_2 = S3.iloc[29:36, [38, 40, 42, 44]]
heures_S3_A_3 = S3.iloc[37:38, [3, 6, 8, 10]]

# remplacer les cases vides par des '0'
heures_S3_A_1 = heures_S3_A_1.fillna(0)
heures_S3_A_2 = heures_S3_A_2.fillna(0)
heures_S3_A_3 = heures_S3_A_3.fillna(0)

# créer une liste avec la fonction "liste_heures" pour le S3 Parcours A
liste_heures_S3_A = []
liste_heures(liste_heures_S3_A, heures_S3_A_1)
liste_heures(liste_heures_S3_A, heures_S3_A_2)
liste_heures(liste_heures_S3_A, heures_S3_A_3)

print(concordance(liste_heures_S3_A, BUT2.liste_heures_S3_A, "S3 Parcours A"), "\n")

# Parcours B

# récupérer la maquette des heures de chaque ressource
heures_S3_B_1 = S3.iloc[29:36, [3, 6, 8, 10]]
heures_S3_B_2 = S3.iloc[29:36, [38, 40, 42, 44]]
heures_S3_B_3 = S3.iloc[36:37, [38, 40, 42, 44]]

# remplacer les cases vides par des '0'
heures_S3_B_1 = heures_S3_B_1.fillna(0)
heures_S3_B_2 = heures_S3_B_2.fillna(0)
heures_S3_B_3 = heures_S3_B_3.fillna(0)

# créer une liste avec la fonction "liste_heures" pour le S3 Parcours B
liste_heures_S3_B = []
liste_heures(liste_heures_S3_B, heures_S3_B_1)
liste_heures(liste_heures_S3_B, heures_S3_B_2)
liste_heures(liste_heures_S3_B, heures_S3_B_3)

print(concordance(liste_heures_S3_B, BUT2.liste_heures_S3_B, "S3 Parcours B"), "\n")

# S4 Parcours A

# lire l'onglet du S4 Parcours A
S4_A = pd.read_excel(planning, 'S4.A')

# récupérer la maquette des heures de chaque ressource
heures_S4_A_1 = S4_A.iloc[18:21, [3, 6, 8, 10]]
heures_S4_A_2 = S4_A.iloc[18:22, [40, 43, 45, 47]]
heures_S4_A_3 = S4_A.iloc[22:23, [3, 6, 8, 10]]
heures_S4_A_4 = S4_A.iloc[23:24, [40, 43, 45, 47]]
heures_S4_A_5 = S4_A.iloc[23:25, [3, 6, 8, 10]]
heures_S4_A_6 = S4_A.iloc[24:25, [40, 43, 45, 47]]
heures_S4_A_7 = S4_A.iloc[25:26, [3, 6, 8, 10]]

# remplacer les cases vides par des '0'
heures_S4_A_1 = heures_S4_A_1.fillna(0)
heures_S4_A_2 = heures_S4_A_2.fillna(0)
heures_S4_A_3 = heures_S4_A_3.fillna(0)
heures_S4_A_4 = heures_S4_A_4.fillna(0)
heures_S4_A_5 = heures_S4_A_5.fillna(0)
heures_S4_A_6 = heures_S4_A_6.fillna(0)
heures_S4_A_7 = heures_S4_A_7.fillna(0)

# créer une liste avec la fonction "liste_heures" pour le S4 Parcours A
liste_heures_S4_A = []
liste_heures(liste_heures_S4_A, heures_S4_A_1)
liste_heures(liste_heures_S4_A, heures_S4_A_2)
liste_heures(liste_heures_S4_A, heures_S4_A_3)
liste_heures(liste_heures_S4_A, heures_S4_A_4)
liste_heures(liste_heures_S4_A, heures_S4_A_5)
liste_heures(liste_heures_S4_A, heures_S4_A_6)
liste_heures(liste_heures_S4_A, heures_S4_A_7)

print(concordance(liste_heures_S4_A, BUT2.liste_heures_S4_A, "S4 Parcours A"), "\n")

# Parcours B

# lire l'onglet du S4 Parcours B
S4_B = pd.read_excel(planning, 'S4.B')

# récupérer la maquette des heures de chaque ressource
heures_S4_B_1 = S4_B.iloc[18:21, [3, 6, 8, 10]]
heures_S4_B_2 = S4_B.iloc[18:22, [40, 43, 45, 47]]
heures_S4_B_3 = S4_B.iloc[22:23, [3, 6, 8, 10]]
heures_S4_B_4 = S4_B.iloc[23:25, [40, 43, 45, 47]]
heures_S4_B_5 = S4_B.iloc[23:26, [3, 6, 8, 10]]

# remplacer les cases vides par des '0'
heures_S4_B_1 = heures_S4_B_1.fillna(0)
heures_S4_B_2 = heures_S4_B_2.fillna(0)
heures_S4_B_3 = heures_S4_B_3.fillna(0)
heures_S4_B_4 = heures_S4_B_4.fillna(0)
heures_S4_B_5 = heures_S4_B_5.fillna(0)

# créer une liste avec la fonction "liste_heures" pour le S4 Parcours B
liste_heures_S4_B = []
liste_heures(liste_heures_S4_B, heures_S4_B_1)
liste_heures(liste_heures_S4_B, heures_S4_B_2)
liste_heures(liste_heures_S4_B, heures_S4_B_3)
liste_heures(liste_heures_S4_B, heures_S4_B_4)
liste_heures(liste_heures_S4_B, heures_S4_B_5)

print(concordance(liste_heures_S4_B, BUT2.liste_heures_S4_B, "S4 Parcours B"), "\n")
