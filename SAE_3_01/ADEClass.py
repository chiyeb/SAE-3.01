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

    def setLibelle(self, libelle):
        self.libelle = libelle

    def setCm(self, cm):
        self.cm = cm

    def setTd(self, td):
        self.td = td

    def setTp(self, tp):
        self.tp = tp