import time,os

# Simulation d'envoie de messages tout les 0.1 secondes
while True :
    lienDossier = os.path.dirname(os.path.realpath('__file__'))
    fichier = open(os.path.join(lienDossier[:-5], "données/messages.txt"), "a+")
    fichier.write("spam:message spammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm\n")
    fichier.close()
    time.sleep(0.1)