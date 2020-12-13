def listeDesMessages():
    fichier = open("messages.txt", "r")
    chat =fichier.read()
    fichier.close()

    return chat.split("\n")

def envoyerMessage(utilisateur,message):
    fichier = open("messages.txt", "a+")
    fichier.write(utilisateur+":"+message+"\n")
    fichier.close()