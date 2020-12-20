import os
#from ilock import ILock

class GestionMessages(object):

    def listeDesMessages(self):
            resultat = []
        # TO DO : Pas sur du fonctionnement à verifier !
        #with ILock('messagesLecture'):
            # Lecture du fichier
            lienDossier = os.path.dirname(os.path.realpath('__file__'))
            fichier = open(os.path.join(lienDossier, "données/messages.txt"), "r")
            # Décomposition en ligne de messages
            chat =fichier.read().split("\n")
            fichier.close()
            # Décomposition des messages en [0] nom utilisateur [1] contenu message
            for message in chat :
                resultat.append(message.split(":"))
            return resultat

    def envoyerMessage(self,utilisateur,message):
        # TO DO : Pas sur du fonctionnement à verifier !
        #with ILock('messagesEcriture'):
            # Ecriture dans le fichier
            lienDossier = os.path.dirname(os.path.realpath('__file__'))
            fichier = open(os.path.join(lienDossier, "données/messages.txt"), "a+")
            fichier.write(utilisateur+":"+message+"\n")
            fichier.close()