import os
#from ilock import ILock

# Class qui permet la gestion des messages des utilisateurs

class GestionMessages(object):

    # Récupère la liste des messages
    # Résultat :
    # - La liste des messages est retourné
    def listeDesMessages(self):
            resultat = []
        # TO DO : Pas sur du fonctionnement à verifier !
        #with ILock('messagesLecture'):
            # Lecture du fichier
            lienDossier = os.path.dirname(os.getcwd())
            fichier = open(os.path.join(lienDossier, "Projet-raspberry/données/messages.txt"), "r")
            # Décomposition en ligne de messages
            chat =fichier.read().split("\n")
            fichier.close()
            # Décomposition des messages en [0] nom utilisateur [1] contenu message
            for message in chat :
                resultat.append(message.split(":"))
            return resultat

    # Envoie le message écrit
    # Précondition :
    # - utilisateur : utilisateur qui envoie le message
    # - message : message a écrire
    # Résultat :
    # - Le message a été écrit
    def envoyerMessage(self,utilisateur,message):
        # TO DO : Pas sur du fonctionnement à verifier !
        #with ILock('messagesEcriture'):
            # Ecriture dans le fichier
            lienDossier = os.path.dirname(os.getcwd())
            fichier = open(os.path.join(lienDossier, "Projet-raspberry/données/messages.txt"), "a+")
            fichier.write(utilisateur+":"+message+"\n")
            fichier.close()