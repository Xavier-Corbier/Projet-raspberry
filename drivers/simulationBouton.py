from drivers.driverBouton import *
import time


initBouton()
while True:
    time.sleep(0.1)
    if boutonActif():
        print("Je suis actif")
    
