# coding: utf-8
import smbus
import time


bus = smbus.SMBus(1)  # pour I2C-1 (0 pour I2C-0)

# Les deux adresses de l'ecran LCD
# celle pour les couleurs du fond d'ecran 
# et celle pour afficher des caracteres
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

##
#   GESTION DE L'ECRAN
##

# Initialise l'écran
# Précondition :
# - avoir un écran Grove-LCD Backlight branché à la raspberry
# Résultat :
# - ecran initialisé
def initEcran():
	texteCmd(0x01)
	texteCmd(0x0F)
	texteCmd(0x38)

# Envoie  a l'ecran une commande concerant l'affichage des caracteres
# Précondition :
# - cmd : chaine de caractère désignant une commande
# Résultat :
# - commande appliqué
def texteCmd(cmd):
	time.sleep(0.1)
	bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

##
#   GESTION DE LA COULEUR
##

# Code de la fonction permettant de choisir la couleur
# du fond d'ecran, ne pas oublier d'initialiser l'ecran
# Précondition :
# - rouge,vert,bleu : trois entiers compris entre 0 et 255
# Résultat :
# - couleur de l'écran changé
def setRGB(rouge,vert,bleu):
	# rouge, vert et bleu sont les composantes de la couleur
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x00,0x00)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x01,0x00)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x02,bleu)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x03,vert)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x04,rouge)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xAA)
#print("Couleur écran changée")

# Met à jour la coleur de l'écran en fonction d'un nom en chaine de caractère
# Précondition :
# - couleur : une chaine de caractère parmis : "bleu", "rouge", "vert", "noir", "blanc"
# Résultat :
# - couleur de l'écran changé
def setCouleur(couleur):

	if(couleur=="bleu"):
		setRGB(0,0,255)
	elif(couleur=="rouge"):
		setRGB(255,0,0)
	elif(couleur=="vert"):
		setRGB(0,255,0)
	elif(color=="noir"):
		setRGB(0,0,0)
	elif(color=="blanc"):
		setRGB(255,255,255)

##
#   GESTION DE L'AFFICHAGE
##

# Fonction permettant d'ecrire le texte recu en parametre (scrolling)
# Si le texte contient un \n ou plus de 16 caracteres un passage à la ligne se fait
# Précondition :
# - texte : chaine de caractère
# Résultat : 
# - texte affiché sur l'écran
def setTextScrolling(texte):
	initEcran()

	nbCaracteres = 0 # Nb de caractères sur la ligne
	numLigne = 1 # Id de la ligne de l'écran
	tempTableau = [] # Sauvegarde temporaire du texte

	# Parcours chaques caractères du texte
	for c in texte:
		nbCaracteres+=1
		if c == '\n':
			texteCmd(0xc0) # sauter la ligne
			nbCaracteres=0 # Reset nb caractères 
			if numLigne==2: # Si on est à la fin de la deuxième ligne. On Reset l'écran
				time.sleep(2)
				initEcran()
				for v in tempTableau:
					bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(v))
				texteCmd(0xc0) # sauter la ligne
				tempTableau=[]
				numLigne=1

			numLigne+=1 # Passage à la ligne suivante

		elif nbCaracteres==16 :
			bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))
			texteCmd(0xc0) # sauter la ligne
			nbCaracteres=0 # Reset nb caractères
			if numLigne==2: # Si on est à la fin de la deuxième ligne. On Reset l'écran
				tempTableau.append(c)
				time.sleep(2)
				initEcran()
				for v in tempTableau:
					bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(v))
				texteCmd(0xc0) # sauter la ligne
				tempTableau=[]
				numLigne=1
			numLigne+=1 # Passage à la ligne suivante

		else:
			bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))
			if numLigne == 2 : # sauvegarde de la dernière ligne du tableau
				tempTableau.append(c)



# Fonction permettant d'ecrire le texte recu en parametre (LigneParLigne)
# Si le texte contient un \n ou plus de 16 caracteres un passage à la ligne se fait
# Précondition :
# - texte : chaine de caractère
# Résultat :
# - texte affiché sur l'écran
def setTextLigneParLigne(texte):
	initEcran()

	nbCaracteres = 0 # Nb de caracteres sur la ligne
	numLigne = 1 # Id de la ligne sur l'écran

	# Parcours chaques caractères du texte
	for c in texte:
		nbCaracteres+=1
		if c == '\n':
			texteCmd(0xc0)
			nbCaracteres=0 # Reset nb caractères
			if numLigne==2: # Si on est à la fin de la deuxième ligne. On Reset l'écran
				time.sleep(2)
				initEcran()
				numLigne=0
			numLigne+=1 # Passage à la ligne suivante

		elif nbCaracteres==16 :
			bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))
			texteCmd(0xc0)
			nbCaracteres=0 # Reset nb caractères
			if numLigne==2: # Si on est à la fin de la deuxième ligne. On Reset l'écran
				time.sleep(2)
				initEcran()
				numLigne=0
			numLigne+=1 # Passage à la ligne suivante


		else:
			bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

