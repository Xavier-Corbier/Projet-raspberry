# coding: utf-8

import grovepi

# Connecte le Grove Switch au port digital D3
BOUTON_PORT = 3

# Initialise le bouton
# Précondition :
# - avoir un bouton branché à la raspberry
# Résultat :
# - bouton initialisé
def initBouton():
	grovepi.pinMode(BOUTON_PORT,"INPUT")

# Vérifie si le bouton est appuyé
# Précondition :
# - avoir un bouton branché à la raspberry
# Résultat :
# - Boolean : True si le bouton est actif sinon False
def boutonActif():
	return grovepi.digitalRead(BOUTON_PORT)
