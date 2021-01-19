# coding: utf-8

from drivers.grovepi import *

# Connecte le Buzzer au port digital D5
BUZZER_PORT = 5

# Initialise le Buzzer
# Précondition :
# - avoir un Buzzer branché à la raspberry
# Résultat :
# - Buzzer initialisé
def initBuzzer():
    pinMode(BUZZER_PORT,"OUTPUT")

# Ecrit sur le Buzzer 0 ou 1
# Précondition :
# - valeur : entier à 0 pour arrêt et 1 marche
# Résultat :
# - Buzzer affecté
def setValeurBuzzer(valeur):
    digitalWrite(BUZZER_PORT,valeur)
