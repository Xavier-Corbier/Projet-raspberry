import os

class GestionMessages(object):

    def listeDesMessages(self):
        lienDossier = os.path.dirname(os.path.realpath('__file__'))

        fichier = open(os.path.join(lienDossier, "données/messages.txt"), "r")
        chat =fichier.read().split("\n")
        fichier.close()

        resultat = []
        for message in chat :
            resultat.append(message.split(":"))

        return resultat

    def envoyerMessage(self,utilisateur,message):
        lienDossier = os.path.dirname(os.path.realpath('__file__'))

        fichier = open(os.path.join(lienDossier, "données/messages.txt"), "a+")
        fichier.write(utilisateur+":"+message+"\n")
        fichier.close()