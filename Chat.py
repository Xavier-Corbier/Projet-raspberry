import curses,os,threading,curses.textpad
import Utilisateurs as appUtilisateurs
import Messages as appMessage

class Chat(object):

    def __init__(self, fenetre):

        self.stdscr = fenetre
        self.nomUtilisateur = ""
        self.actif = True

        # récupération des dimensions
        self.maxY, self.maxX = fenetre.getmaxyx()

        # connexion aux données des appli de Messages et Utilisateurs
        self.appMessages = appMessage.Messages()
        self.appUtilisateurs = appUtilisateurs.Utilisateurs()

    ##
    #   PARTIE INITIALISATION
    ##
    
    def initialisation(self):

        # Pas de répétition des caractères au clavier
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)


        # Récupération du caractère pour supprimer
        self.charSuppression = curses.erasechar()

        # Mise en place de l'affichage
        self.initialisationAffichage()

    def initialisationAffichage(self):

        # finY, finX, y, x

        try :
            self.titreFenetre = curses.newwin(1, self.maxX, 0, 0)
            self.utilisateurFenetre = curses.newwin(self.maxY - 1,int(self.maxX * 0.25),1,0)
            self.chatFenetre = curses.newwin(self.maxY - int(self.maxY * 0.1) - 1,self.maxX - int(self.maxX * 0.25),1,int(self.maxX * 0.25))
            self.texteFenetre = curses.newwin(int(self.maxY * 0.1),self.maxX - int(self.maxX * 0.25),self.maxY - int(self.maxY * 0.1),int(self.maxX * 0.25))

            self.utilisateurZone = curses.newwin(self.maxY - 4,int(self.maxX * 0.25)-3,3,1)
            self.chatZone = curses.newwin(self.maxY - int(self.maxY * 0.1) - 3,self.maxX - int(self.maxX * 0.25) - 2,2,int(self.maxX * 0.25) + 1)
            self.texteZone = curses.newwin(int(self.maxY * 0.1) - 2,self.maxX - int(self.maxX * 0.25) - 2,self.maxY - int(self.maxY * 0.1) + 1,int(self.maxX * 0.25) + 1)

            self.initTitre()
            self.initChat()
            self.initChatZone()
            self.initTexte()
            self.initTexteZone()
            self.initUtilisateur()

            self.effacer()

        except Exception :
            self.stoper()
            print("Erreur : les dimensions du terminal sont trop faibles")

    def initTitre(self):
        name = "Chat"
        self.titreFenetre.addstr(0, int(self.maxX/2 - len(name)/2), name)
        self.titreFenetre.refresh()

    def initChat(self):
        self.chatFenetre.box()
        self.chatFenetre.refresh()

    def initChatZone(self):
        self.chatZone.refresh()
        self.chatIndice = 0
        self.messageNombre = 0
        self.messageNombreHistorique = 0

    def initTexte(self):
        self.texteFenetre.box()
        self.texteFenetre.refresh()

    def initTexteZone(self):
        self.text = ""
        self.texteZone.refresh()

    def initUtilisateur(self):
        self.utilisateurFenetre.addstr(1, 1, "Utilisateur(s) :")
        self.utilisateurFenetre.box()
        self.utilisateurFenetre.refresh()
        self.rechargementUtilisateur()
        
    ##
    #   PARTIE RECHARGEMENT
    ##

    def rechargementChat(self):
        self.chatZone.erase()
        self.chatIndice = 0
        self.chatZone.refresh()
        self.messageNombreHistorique += self.messageNombre
        self.messageNombre = 1

    def rechargementUtilisateur(self):
        self.utilisateurZone.clear()
        self.utilisateurIndice = 0

        listeUtilisateurs = self.appUtilisateurs.listeDesUtilisateurs()

        for user in listeUtilisateurs :
            try:
                self.utilisateurZone.addstr(self.utilisateurIndice+3, 1, user)

            except Exception :
                pass

            self.utilisateurIndice+=1

        self.utilisateurZone.refresh()

    def rechargementTexteZone(self):
        self.texteZone.addstr(0, 0, self.text)
        self.texteZone.refresh()

    ##
    #   PARTIE GESTION MESSAGES
    ##

    def message(self, char):

        if self.actif :
            if char == ord('$'):
                self.stdscr.clear()
            # raccourciclavier pour envoyer un message
            elif char == ord('!'):
                self.envoyerMessage()
            elif char == curses.KEY_UP:
                var = True
                afficherMessage(self, utilisateur, chat)
                var = False
            elif char == ord('b'):
                for i in range(9780, 9801):
                    self.text += chr(i)
                    self.rechargementTexteZone()
                    
            elif char == curses.KEY_RIGHT:
                k = k + 1
            #raccourciclavier pour quitter
            elif char == ord(':'):
                self.stoper()
            elif chr(char) == "\n":

                self.messageNombre += 1
                self.afficherMessage(self.nomUtilisateur,self.text)
                self.envoyerMessage()
                return

            elif chr(char) == self.charSuppression or chr(char) == "ć" or chr(char) == "\x7f":
                self.effacer()
                return

            else:
                self.text += chr(char)
                self.rechargementTexteZone()
                return
        else :
            return

    def effacer(self):
        self.text = self.text[:-1]
        self.texteZone.clear()
        self.rechargementTexteZone()

    def recupererMessages(self):

        while self.actif:
            listeMessage = self.appMessages.listeDesMessages()

            if self.messageNombre + self.messageNombreHistorique < len(listeMessage)-1 :
                message = listeMessage[self.messageNombre + self.messageNombreHistorique]
                self.afficherMessage(message[0],message[1])
                self.messageNombre+=1

    def envoyerMessage(self):
        self.appMessages.envoyerMessage(self.nomUtilisateur,self.text)
        self.text = ""
        self.texteZone.clear()
        self.rechargementTexteZone()

    def afficherMessage(self,utilisateur,chat):

        try:
            self.chatZone.addstr(self.chatIndice, 0, str(utilisateur) + ' : ')

        except Exception:
            self.rechargementChat()
            self.chatZone.addstr(self.chatIndice, 0, str(utilisateur) + ' : ')

        self.chatZone.addstr(chat)
        self.chatZone.refresh()

        self.chatIndice = self.chatZone.getyx()[0]
        self.chatIndice += 1

    ##
    #   PARTIE GESTION UTILISATEURS
    ##

    def recupererUtilisateurs(self):

        while self.actif:
            listeUtilisateurs=self.appUtilisateurs.listeDesUtilisateurs()

            if self.utilisateurIndice != len(listeUtilisateurs) :
                self.rechargementUtilisateur()

    def ajouterUtilisateur(self):
        self.appUtilisateurs.ajouterUtilisateur(self.nomUtilisateur)

    def supprimerUtilisateur(self):
        self.appUtilisateurs.supprimerUtilisateur(self.nomUtilisateur)

    ##
    #   PARTIE ACTIVITE PROGRAMME
    ##

    def lancer(self):

        while self.actif:
            caractere = self.texteFenetre.getch()
            self.message(caractere)

    def stoper(self,signum=None, frame=None):

        self.actif=False
        self.stdscr.keypad(False)

        self.supprimerUtilisateur()

        curses.echo()
        curses.nocbreak()

        curses.endwin()

# Cette méthode est utilisé pour les test de Chat.py
if __name__ == "__main__":
    print("test programme")

