import os
#from ilock import ILock

# Class qui permet la gestion des utilisateurs

class GestionUtilisateurs(object):

    # Supprime l'utilisateur
    # Précondition :
    # - nomUtilisateur : nom utilisateur a supprimer
    # Résultat :
    # - Le nom de l'utilisateur a été supprimé
    def supprimerUtilisateur(self,nomUtilisateur):
        # TO DO : Pas sur du fonctionnement à verifier !
        #with ILock('utilisateursSuppression'):
            # Récupération des utilisateurs actuels
            listeUtilisateurs = self.listeDesUtilisateurs()
            # Réécriture de tous les noms d'utilisateurs sauf celui que l'on veut supprimer
            lienDossier = os.path.dirname(os.getcwd())
            fichier = open(os.path.join(lienDossier, "Projet-raspberry/données/utilisateurs.txt"), "w")
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

    # Ajout l'utilisateur
    # Précondition :
    # - nomUtilisateur : nom utilisateur a ajouté
    # Résultat :
    # - Le nom de l'utilisateur a été écrit
    def ajouterUtilisateur(self,nomUtilisateur):
        # TO DO : Pas sur du fonctionnement à verifier !
        #with ILock('utilisateursAjout'):
            # Ecriture du nom d'utilisateur dans le fichier
            lienDossier = os.path.dirname(os.getcwd())
            fichier = open(os.path.join(lienDossier, "Projet-raspberry/données/utilisateurs.txt"), "a+")
            fichier.write(nomUtilisateur+"\n")
            fichier.close()

    # Récupère la liste des utilisateurs
    # Résultat :
    # - La liste des utilisateurs est retourné
    def listeDesUtilisateurs(self):
        # TO DO : Pas sur du fonctionnement à verifier !
        #with ILock('utilisateursLecture'):
            # Lecture du fichier
            lienDossier = os.path.dirname(os.getcwd())
            fichier = open(os.path.join(lienDossier, "Projet-raspberry/données/utilisateurs.txt"), "r")
            utilisateurs =fichier.read()
            fichier.close()
            # Décomposition du fichier en ligne
            return utilisateurs.split("\n")