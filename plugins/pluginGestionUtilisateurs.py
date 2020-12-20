import os
#from ilock import ILock

class GestionUtilisateurs(object):

    def supprimerUtilisateur(self,nomUtilisateur):
        # TO DO : Pas sur du fonctionnement à verifier !
        #with ILock('utilisateursSuppression'):
            # Récupération des utilisateurs actuels
            listeUtilisateurs = self.listeDesUtilisateurs()
            # Réécriture de tous les noms d'utilisateurs sauf celui que l'on veut supprimer
            lienDossier = os.path.dirname(os.path.realpath('__file__'))
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
        # TO DO : Pas sur du fonctionnement à verifier !
        #with ILock('utilisateursAjout'):
            # Ecriture du nom d'utilisateur dans le fichier
            lienDossier = os.path.dirname(os.path.realpath('__file__'))
            fichier = open(os.path.join(lienDossier, "données/utilisateurs.txt"), "a+")
            fichier.write(nomUtilisateur+"\n")
            fichier.close()

    def listeDesUtilisateurs(self):
        # TO DO : Pas sur du fonctionnement à verifier !
        #with ILock('utilisateursLecture'):
            # Lecture du fichier
            lienDossier = os.path.dirname(os.path.realpath('__file__'))
            fichier = open(os.path.join(lienDossier, "données/utilisateurs.txt"), "r")
            utilisateurs =fichier.read()
            fichier.close()
            # Décomposition du fichier en ligne
            return utilisateurs.split("\n")