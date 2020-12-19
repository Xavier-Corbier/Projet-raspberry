import os
#from ilock import ILock

class GestionUtilisateurs(object):

    def supprimerUtilisateur(self,nomUtilisateur):


            lienDossier = os.path.dirname(os.path.realpath('__file__'))

            listeUtilisateurs = self.listeDesUtilisateurs()

        #with ILock('utilisateursSuppression'):
            fichier = open(os.path.join(lienDossier, "données/utilisateurs.txt"), "w")
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

            lienDossier = os.path.dirname(os.path.realpath('__file__'))
        #with ILock('utilisateursAjout'):
            fichier = open(os.path.join(lienDossier, "données/utilisateurs.txt"), "a+")
            fichier.write(nomUtilisateur+"\n")
            fichier.close()

    def listeDesUtilisateurs(self):
            lienDossier = os.path.dirname(os.path.realpath('__file__'))

        #with ILock('utilisateursLecture'):
            fichier = open(os.path.join(lienDossier, "données/utilisateurs.txt"), "r")
            utilisateurs =fichier.read()
            fichier.close()

            return utilisateurs.split("\n")