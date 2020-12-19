import time,os
for _ in range(0,15) :
    lienDossier = os.path.dirname(os.path.realpath('__file__'))
    fichier = open(os.path.join(lienDossier[:-5], "données/utilisateurs.txt"), "a+")

    fichier.write("spammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm\n")
    fichier.close()
    time.sleep(0.1)