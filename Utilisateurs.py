class Utilisateurs(object):

    def supprimerUtilisateur(self,nomUtilisateur):

        listeUtilisateurs = self.listeDesUtilisateurs()

        fichier = open("users.txt", "w")
        nombreSupprime = 0
        for user in listeUtilisateurs:
            if nombreSupprime == 0:
                if user.split("\n")[0]!=nomUtilisateur and user !="":
                    fichier.write(user+"\n")
                else :
                    nombreSupprime +=1
            else :
                if user !="":
                    fichier.write(user+"\n")
        fichier.close()

    def ajouterUtilisateur(self,nomUtilisateur):
        fichier = open("users.txt", "a+")
        fichier.write(nomUtilisateur+"\n")
        fichier.close()

    def listeDesUtilisateurs(self):
        fichier = open("users.txt", "r")
        utilisateurs =fichier.read()
        fichier.close()

        return utilisateurs.split("\n")