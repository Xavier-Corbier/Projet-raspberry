# coding: utf-8

import grovepi

# Connecte la LED au port digital D2
LED_PORT = 2

# Initialise le relais
# Précondition :
# - avoir une LED branché à la raspberry
# Résultat :
# - LED initialisé
def initLED():
    grovepi.pinMode(LED_PORT,"OUTPUT")

# Ecrit sur la LED 0 ou 1
# Précondition :
# - valeur : entier à 0 pour arrêt et 1 marche
# Résultat :
# - LED affecté
def setValeurLED(valeur):
    grovepi.digitalWrite(LED_PORT,valeur)
