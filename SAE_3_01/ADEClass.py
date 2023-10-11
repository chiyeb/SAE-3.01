class ADEClass:
    def __init__(self, id, libelle, cm, td, tp):
        self.id = id
        self.libelle = libelle
        self.cm = cm
        self.td = td
        self.tp = tp

    def getId(self):
        return self.id

    def getLibelle(self):
        return self.libelle

    def getCm(self):
        return self.cm

    def getTd(self):
        return self.td

    def getTp(self):
        return self.tp
