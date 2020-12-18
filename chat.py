import curses, threading,curses.textpad,signal,time,os
from plugins import pluginGestionMessages as pgm, pluginGestionUtilisateurs as pgu, pluginFenetreOption as pfo


class Chat(object):

    def __init__(self, fenetre):

        self.stdscr = fenetre
        self.nomUtilisateur = ""

        # récupération des dimensions
        self.maxY, self.maxX = fenetre.getmaxyx()

        # connexion aux données des appli de gestion de Messages et Utilisateurs
        self.gestionMessages = pgm.GestionMessages()
        self.gestionUtilisateurs = pgu.GestionUtilisateurs()

        self.mutex=threading.Lock()

    ##
    #   PARTIE INITIALISATION
    ##
    
    def initialisation(self):

        # Pas de répétition des caractères au clavier
        curses.noecho()
        curses.cbreak()

        # Pas de delai à l'affichage
        self.stdscr.nodelay(0)
        # Récupération du caractère pour supprimer
        self.charSuppression = curses.erasechar()
        curses.curs_set(0)

        curses.doupdate()
        # Mise en place de l'affichage
        self.initialisationAffichage()

    def initialisationAffichage(self):

        # finY, finX, y, x

        try :
            # Création de chaque fenètre de traitement
            self.titreFenetre = curses.newwin(1, self.maxX, 0, 0)
            self.utilisateurFenetre = curses.newwin(self.maxY - 1,int(self.maxX * 0.25),1,0)
            self.chatFenetre = curses.newwin(self.maxY - int(self.maxY * 0.1) - 1,self.maxX - int(self.maxX * 0.25),1,int(self.maxX * 0.25))
            self.texteFenetre = curses.newwin(int(self.maxY * 0.1),self.maxX - int(self.maxX * 0.25),self.maxY - int(self.maxY * 0.1),int(self.maxX * 0.25))

            ## Ce sont des fenètres superposées aux précédentes pour permettre un traitement plus simple
            self.utilisateurZone = curses.newwin(self.maxY - 4,int(self.maxX * 0.25)-3,3,1)
            self.chatZone = curses.newwin(self.maxY - int(self.maxY * 0.1) - 3,self.maxX - int(self.maxX * 0.25) - 2,2,int(self.maxX * 0.25) + 1)
            self.texteZone = curses.newwin(1,self.maxX - int(self.maxX * 0.25) - 2,self.maxY - int(self.maxY * 0.1) + 1,int(self.maxX * 0.25) + 1)

            # Initialisation de chaques parties de l'écran
            self.initTitre()
            self.initChat()
            self.initTexte()
            self.initUtilisateur()


            self.text="initialisation"
            self.envoyerMessage()
        except Exception :
            # Si les dimensions de l'écran sont trop faibles
            self.stoper()
            print("Erreur : les dimensions du terminal sont trop faibles")

    def initTitre(self):
        # Ajout du titre au centre de l'écran
        name = "Chat"
        self.titreFenetre.addstr(0, int(self.maxX/2 - len(name)/2), name)
        self.titreFenetre.refresh()

    def initChat(self):
        # Bordures de la fenètre
        self.chatFenetre.box()
        self.chatFenetre.refresh()
        self.chatZone.refresh()
        self.chatIndice = 0
        self.messageNombre = 0
        self.messageNombreHistorique = 0
        self.nombreMessageRemoter = 0

    def initTexte(self):
        # Bordures de la fenètre
        self.texteFenetre.box()
        self.texteFenetre.refresh()
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
        self.chatZone.refresh()
        y, x = self.chatZone.getmaxyx()

        self.messageNombre = 0

        listeMessage = self.gestionMessages.listeDesMessages()
        while self.messageNombre < y :
            message = listeMessage[len(listeMessage)-2-self.messageNombre]
            self.afficherMessage(message[0],message[1])
        self.messageNombreHistorique = len(listeMessage)-self.messageNombre

    def rechargementUtilisateur(self):
        self.utilisateurZone.clear()
        self.utilisateurIndice = 0

        listeUtilisateurs = self.gestionUtilisateurs.listeDesUtilisateurs()

        for user in listeUtilisateurs :
            try:
                self.utilisateurZone.addstr(self.utilisateurIndice+3, 1, user)
            except Exception :
                pass

            self.utilisateurIndice+=1

        self.utilisateurZone.refresh()

    def rechargementTexteZone(self):
        try :

            self.texteZone.addstr(0, 0, self.text)
            self.texteZone.refresh()
        except Exception:
            self.text = self.text[:-1]


    ##
    #   PARTIE GESTION MESSAGES
    ##

    def message(self, char):

        if self.actif :

            if chr(char) == "\n" :

                if self.text == ":changerNom" :
                    self.stoper()

                    option = curses.wrapper(pfo.FenetreOption)
                    option.initialisation("Changement de pseudo :")
                    reponse = option.lancer()

                    if reponse != "" :
                        self.nomUtilisateur = reponse

                    self.lancer()

                elif self.text == ":effacerEcran" :
                    self.rechargementChat()
                    self.text = ""
                    self.texteZone.clear()
                    self.rechargementTexteZone()

                elif self.text == ":p" :
                    self.nombreMessageRemoter +=1
                    self.chatZone.erase()
                    self.chatZone.refresh()
                    self.chatIndice = 0
                    self.messageNombre = 0
                    self.messageNombreHistorique = 0
                    self.text = ""
                    self.texteZone.erase()
                    self.texteZone.refresh()

                elif self.text == ":s" :
                    if self.nombreMessageRemoter > 0:
                        self.nombreMessageRemoter -=1
                    self.chatZone.erase()
                    self.chatZone.refresh()
                    self.chatIndice = 0
                    self.messageNombre = 0
                    self.messageNombreHistorique = 0
                    self.text = ""
                    self.texteZone.erase()
                    self.texteZone.refresh()
                else :

                    if self.nombreMessageRemoter != 0:
                        self.nombreMessageRemoter =0
                        self.chatZone.erase()
                        self.chatZone.refresh()
                        self.chatIndice = 0
                        self.messageNombre = 0
                        self.messageNombreHistorique = 0

                    else :
                        self.envoyerMessage()

                return

            elif chr(char) == self.charSuppression or chr(char) == "ć" or chr(char) == "\x7f":
                self.effacer()
                return

            else:
                self.text += chr(char)
                with self.mutex:
                    self.rechargementTexteZone()
                return
        else :
            return

    def effacer(self):
        self.text = self.text[:-1]
        self.texteZone.clear()
        with self.mutex :
            self.rechargementTexteZone()

    def recupererMessages(self):

        while self.actif:
            time.sleep(0.1)
            listeMessage = self.gestionMessages.listeDesMessages()

            if self.messageNombre + self.messageNombreHistorique < len(listeMessage) :
                with self.mutex :
                    self.rechargementChat()

    def envoyerMessage(self):
        message = self.text
        self.text = ""
        self.texteZone.clear()
        with self.mutex :
            self.rechargementTexteZone()
        if message !="":
            self.gestionMessages.envoyerMessage(self.nomUtilisateur,message)


    def afficherMessage(self,utilisateur,chat):

        y, x = self.chatZone.getmaxyx()
        try:
            self.chatZone.addstr(y-1-self.messageNombre, 0, str(utilisateur) + ' : ' + str(chat))

        except Exception:
            with self.mutex :
                self.rechargementChat()
            self.chatZone.addstr(y-1-self.messageNombre, 0, str(utilisateur) + ' : '+ str(chat))

        self.chatZone.refresh()
        self.messageNombre+=1


    ##
    #   PARTIE GESTION UTILISATEURS
    ##

    def recupererUtilisateurs(self):

        while self.actif:
            time.sleep(0.1)
            listeUtilisateurs=self.gestionUtilisateurs.listeDesUtilisateurs()

            if self.utilisateurIndice != len(listeUtilisateurs) :
                with self.mutex :
                    self.rechargementUtilisateur()

    def ajouterUtilisateur(self):
        self.gestionUtilisateurs.ajouterUtilisateur(self.nomUtilisateur)

    def supprimerUtilisateur(self):
        self.gestionUtilisateurs.supprimerUtilisateur(self.nomUtilisateur)

    ##
    #   PARTIE ACTIVITE PROGRAMME
    ##

    def lancer(self):

        self.actif = True

        self.initialisation()
        self.nomUtilisateur = os.environ["USER"]

        self.ajouterUtilisateur()
        threading.Thread(target=self.recupererMessages).start()
        threading.Thread(target=self.recupererUtilisateurs).start()

        signal.signal(signal.SIGINT, self.stoper)

        while self.actif:
            caractere = self.texteFenetre.getch()
            self.message(caractere)

    def stoper(self,signum=None, frame=None):

        self.actif=False
        self.supprimerUtilisateur()
        # Attendre que les threads se terminent
        time.sleep(0.1)
        # Fermeture de la fenètre
        curses.echo()
        curses.nocbreak()
        curses.endwin()

# Cette méthode est utilisé pour les test de Chat.py
if __name__ == "__main__":
    print("test programme")

