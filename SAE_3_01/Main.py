from BUT1 import BUT1
from BUT2 import BUT2
from BUT3 import BUT3
from recupData import recupData
from scribeData import scribeData
from selectFile import selectFile
from verifData import verifData

print("i")
selectFileInstance = selectFile()
selectFileInstance.recup_destination_file()

recupDataInstance = recupData()
recupDataInstance.recupNomProf()

BUT1_instance = BUT1()
BUT1_instance.run()

BUT2_instance = BUT2()
BUT2_instance.run()

BUT3_instance = BUT3()
BUT3_instance.run()

verifdata_instance = verifData()
verifdata_instance.renomFichierAvecNbErreur()

scribedata_instance = scribeData()
scribedata_instance.scribeHoraireTotalProf()

#stats = Stats()
#stats.execAllStats()
