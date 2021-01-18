# coding: utf-8

from drivers.grovepi import *

# Connecte le Grove Switch au port digital D3
BOUTON_PORT = 3

# Initialise le bouton
# Précondition :
# - avoir un bouton branché à la raspberry
# Résultat :
# - bouton initialisé
def initBouton():
	pinMode(BOUTON_PORT,"INPUT")

# Vérifie si le bouton est appuyé
# Précondition :
# - avoir un bouton branché à la raspberry
# Résultat :
# - Boolean : True si le bouton est actif sinon False
def boutonActif():
	return digitalRead(BOUTON_PORT)
