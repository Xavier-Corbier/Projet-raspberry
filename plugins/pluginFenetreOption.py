import curses,os,threading,curses.textpad,signal

# Class qui permet de gérer et afficher des options au chat

class FenetreOption(object):

    # Crée l'option
    # Précondition :
    # - fenetre : fenetre curses - curses.initscr()
    # Résultat :
    # - La fenètre option est crée
    def __init__(self, fenetre):
        self.stdscr = fenetre
        self.actif = True
        # Initialisation des variables
        self.question = ""
        self.text = ""
        # Récupération des dimensions
        self.maxY, self.maxX = fenetre.getmaxyx()
        # Pas de répétition des caractères au clavier
        curses.noecho()
        curses.cbreak()
        # Pas de delai à l'affichage
        self.stdscr.nodelay(0)
        # Ne pas afficher de curseurs à l'écran
        curses.curs_set(0)
        curses.doupdate()
        # Récupération du caractère pour supprimer
        self.charSuppression = curses.erasechar()
        # Nettoyer l'écran
        self.stdscr.clear()

    ##
    #   PARTIE INITIALISATION
    ##

    # Initialise l'option
    # Précondition :
    # - question : table de chaines de caractères de questions que l'on veut posé
    # - boolReponse : booléen pour savoir si l'on veut une réponse à notre question
    # Résultat :
    # - L'affichage de l'option est initialisé
    def initialisation(self,question,boolReponse=True):
        # Récupération des données
        self.question = question
        self.boolReponse = boolReponse
        # Création des fenètres de l'écran
        try :
            if boolReponse :
                self.titreFenetre = curses.newwin(self.maxY-int(self.maxY * 0.3)-2, self.maxX, 0, 0)
                self.texteFenetre = curses.newwin(int(self.maxY * 0.3),self.maxX ,self.maxY - int(self.maxY * 0.3),0)
                self.texteZone = curses.newwin(int(self.maxY * 0.3)  -3  ,self.maxX  -3 ,self.maxY - int(self.maxY * 0.3) + 2, + 2)
            else :
                self.titreFenetre = curses.newwin(self.maxY, self.maxX, 0, 0)

        except Exception:
            print("Erreur : Les dimensions de l'écran sont trop petites !")
            self.stoper()
        # Initialisation des différentes fenètres
        self.initTitre()
        if boolReponse :
            self.initTexte()

    # Initialise le titre de l'option
    # Résultat :
    # - La partie titre de l'option est initialisé si les dimensions le permettent
    def initTitre(self):
        # Ajout du titre au centre de l'écran
        y, x = self.titreFenetre.getmaxyx()
        longeur = int(len(self.question)/2) - len(self.question)
        i = 0
        # Mise en en place de chaque ligne des questions au centre de l'écran
        try :
            while longeur< len(self.question) and i < len(self.question) :
                self.titreFenetre.addstr(int(self.maxY/2)-2-longeur, int(self.maxX/2 - len(self.question[len(self.question)-i-1])/2), self.question[len(self.question)-i-1])
                longeur +=1
                i+=1
        except Exception :
            print("Erreur : Les dimensions de l'écran sont trop petites !")
            self.stoper()
        self.titreFenetre.refresh()

    # Initialise la partie texte de l'option
    # Résultat :
    # - La partie texte de l'option est initialisé
    def initTexte(self):
        try :
            self.texteFenetre.addstr(1,1, "Réponse :")
        except Exception :
            print("Erreur : Les dimensions de l'écran sont trop petites !")
            self.stoper()
        # Bordures de la fenètre
        self.texteFenetre.box()
        self.texteFenetre.refresh()
        self.text = ""
        self.texteZone.refresh()

    ##
    #   PARTIE RECHARGEMENT
    ##

    # Recharge la partie texte de l'option
    # Résultat :
    # - La partie texte de l'option est rechargé avec les dernieres lettres tappé
    def rechargementTexteZone(self):
        # Si la zone de texte est assez grande
        try :
            self.texteZone.addstr(0, 0, self.text)
            self.texteZone.refresh()
        # Sinon on suprime le caractère qu'on vient d'ajouter
        except Exception:
            self.text = self.text[:-1]

    ##
    #   PARTIE GESTION MESSAGES CLAVIER
    ##

    # Traite le message écrit à partir des commandes reçu du clavier
    # Résultat :
    # - Les commandes sont traités
    def message(self, char):
        # Si le chat est actif
        if self.actif :
            # Si on clique sur entré
            if chr(char) == "\n":
                self.stoper()
                return
            # Si on a une réponse
            elif self.boolReponse:
                # Si on est en train de supprimer
                if chr(char) == self.charSuppression or chr(char) == "ć" or chr(char) == "\x7f":
                    self.effacer()
                    return
                # Sinon on ajoute le caractère à l'écran
                else:
                    self.text += chr(char)
                    self.rechargementTexteZone()
                    return
            else :
                return
        # Si on est pas actif on s'arrête
        else :
            return

    # Efface le dernier caractère écrit sur la partie texte de l'option
    # Résultat :
    # - Le dernier caractère est effacé
    def effacer(self):
        # On supprime le dernier caractère
        self.text = self.text[:-1]
        self.texteZone.clear()
        self.rechargementTexteZone()

    ##
    #   PARTIE ACTIVITE PROGRAMME
    ##

    # Lance l'option
    # Résultat :
    # - L'option est lancé et le signal Ctrl + C est activé pour stopper l'option
    def lancer(self):
        # Ajout du signal pour stopper avec un ctrl + C
        signal.signal(signal.SIGINT, self.stoper)
        # Si on veut une réponse
        if self.boolReponse:
            self.texteZone.nodelay(0)
        # Tant que l'option est actif
        while self.actif:
            # On récupère les caractères saisie au clavier et on les traitent
            if self.boolReponse:
                caractere = self.texteZone.getch()
                self.message(caractere)
        # Retourne la réponse à la question
        return self.text

    # Stoppe l'option
    # Précondition :
    # - signum,frame : Paramètre facultatif qui sont utile pour lier à un signal
    # Résultat :
    # - L'option est stoppé
    def stoper(self,signum=None, frame=None):
        # Fermeture de l'option
        self.actif=False
        # Fermeture de la fenètre
        curses.curs_set(1)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

