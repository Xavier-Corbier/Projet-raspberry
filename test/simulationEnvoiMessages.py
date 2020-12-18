import time,os
while True :
    lienDossier = os.path.dirname(os.path.realpath('__file__'))

    fichier = open(os.path.join(lienDossier, "données/messages.txt"), "a+")

    fichier.write("spam:message spammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm\n")
    fichier.close()
    time.sleep(0.1)