from drivers.driverLED import *
from drivers.driverLCD import *
from drivers.driverBouton import *
import time
class GestionCapteurs(object):
    def alumerLed(self):
        try :
            initLED()
            setValeurLED(1)
            time.sleep(3)
            setValeurLED(0)
        except Exception:
            pass

    def afficherMessage(self, message):
        try :
            setTextLigneParLigne(message)
        except Exception:
            pass

    def boutonEstActif(self):
        try :
            initBouton()
            return boutonActif()
        except Exception:
            pass
            return False

