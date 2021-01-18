from drivers.driverLED import *
from drivers.driverLCD import *
from drivers.driverBouton import *
import time

# Class qui permet de gérer les capteurs

class GestionCapteurs(object):
    # allume une LED Si elle est branché
    # Résultat :
    # - La LED est allumé 3 s si elle est branché
    def alumerLed(self):
        try :
            initLED()
            setValeurLED(1)
            time.sleep(3)
            setValeurLED(0)
        except Exception:
            pass

    # allume une LED Si elle est branché
    # Résultat :
    # - La LED est allumé 3 s si elle est branché
    def afficherMessage(self, message):
        try :
            setTextLigneParLigne(message)
        except Exception:
            pass
    # vérifie si un bouton est appuyé
    # Résultat :
    # - Un booléen à True si le bouton est branché et appuyé , sinon False
    def boutonEstActif(self):
        try :
            initBouton()
            return boutonActif()
        except Exception:
            pass
            return False

