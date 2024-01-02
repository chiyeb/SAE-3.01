from BUT1 import *
from BUT2 import *
from BUT3 import *
from Stats import Stats
from scribeData import *
BUT1_instance = BUT1()
BUT1_instance.run()

BUT2_instance = BUT2()
BUT2_instance.run()

BUT3_instance = BUT3()
BUT3_instance.run()

scribedata_instance = scribeData()
scribedata_instance.scribeHoraireTotalProf()

stats = Stats()
stats.execAllStats()
