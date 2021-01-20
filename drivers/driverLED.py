# coding: utf-8

from drivers.grovepi import *
import time
# Connecte la LED au port digital D2
LED_PORT = 2

# Initialise la LED
# Précondition :
# - avoir une LED branché à la raspberry
# Résultat :
# - LED initialisé
def initLED():
    pinMode(LED_PORT,"OUTPUT")

# Ecrit sur la LED 0 ou 1
# Précondition :
# - valeur : entier à 0 pour arrêt et 1 marche
# Résultat :
# - LED affecté
def setValeurLED(valeur):
    time.sleep(0.1)
    digitalWrite(LED_PORT,valeur)
