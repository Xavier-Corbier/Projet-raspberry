# coding: utf-8

import grovepi

# Connecte le Buzzer au port digital D5
BUZZER_PORT = 5

# Initialise le relais
# Précondition :
# - avoir un Buzzer branché à la raspberry
# Résultat :
# - Buzzer initialisé
def initBuzzer():
    grovepi.pinMode(BUZZER_PORT,"OUTPUT")

# Ecrit sur le Buzzer 0 ou 1
# Précondition :
# - valeur : entier à 0 pour arrêt et 1 marche
# Résultat :
# - Buzzer affecté
def setValeurBuzzer(valeur):
    grovepi.digitalWrite(BUZZER_PORT,valeur)
