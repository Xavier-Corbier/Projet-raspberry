# coding: utf-8

from drivers.grovepi import *

# Connecte le Grove Relay au port digital D4
RELAIS_PORT = 4

# Initialise le relais
# Précondition :
# - avoir un relais branché à la raspberry
# Résultat :
# - relais initialisé
def initRelais():
	pinMode(RELAIS_PORT,"OUTPUT")

# Ecrit sur le relais 0 ou 1
# Précondition :
# - valeur : entier à 0 pour arrêt et 1 marche
# Résultat :
# - relais affecté
def setValeurRelais(valeur):
	digitalWrite(RELAIS_PORT,valeur)