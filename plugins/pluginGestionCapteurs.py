from drivers.driverLED import *
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
if __name__ == "__main__":
    GestionCapteurs.alumerLed()
