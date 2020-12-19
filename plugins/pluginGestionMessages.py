import os
#from ilock import ILock

class GestionMessages(object):

    def listeDesMessages(self):
            resultat = []

        #with ILock('messagesLecture'):
            lienDossier = os.path.dirname(os.path.realpath('__file__'))

            fichier = open(os.path.join(lienDossier, "données/messages.txt"), "r")
            chat =fichier.read().split("\n")
            fichier.close()


            for message in chat :
                resultat.append(message.split(":"))

            return resultat

    def envoyerMessage(self,utilisateur,message):
        #with ILock('messagesEcriture'):
            lienDossier = os.path.dirname(os.path.realpath('__file__'))

            fichier = open(os.path.join(lienDossier, "données/messages.txt"), "a+")
            fichier.write(utilisateur+":"+message+"\n")
            fichier.close()