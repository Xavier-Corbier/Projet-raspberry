from plugins.pluginGestionCapteurs import *
import time
test = GestionCapteurs()
# simulation affichage texte
test.afficherMessage("salut !!!!")
while True :
    time.sleep(1)
    # simulation activité bouton
    if test.boutonEstActif():
        print("je suis allumé !!!")
