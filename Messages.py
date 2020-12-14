class Messages(object):

    def listeDesMessages(self):
        fichier = open("messages.txt", "r")
        chat =fichier.read().split("\n")
        fichier.close()

        resultat = []
        for message in chat :
            resultat.append(message.split(":"))

        return resultat

    def envoyerMessage(self,utilisateur,message):
        fichier = open("messages.txt", "a+")
        fichier.write(utilisateur+":"+message+"\n")
        fichier.close()