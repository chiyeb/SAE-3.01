class PlanningClass:
    def __init__(self, semestre, ressource, h_cm, h_td, h_tp, resp):
        self.semestre = semestre
        self.ressource = ressource
        self.h_cm = h_cm
        self.h_td = h_td
        self.h_tp = h_tp
        self.resp = resp

    def getSemestre(self):
        return self.semestre

    def getRessource(self):
        return self.ressource

    def getH_CM(self):
        return self.h_cm

    def getH_TD(self):
        return self.h_td

    def getH_TP(self):
        return self.h_tp

    def getResp(self):
        return self.resp
    def setRessource(self, ressource):
        self.ressource = ressource

    def setCm(self, cm):
        self.h_cm = cm

    def setTd(self, td):
        self.h_td = td

    def setTp(self, tp):
        self.h_tp = tp
