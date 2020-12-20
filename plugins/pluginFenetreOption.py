import curses,os,threading,curses.textpad,signal

class FenetreOption(object):

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

    def initialisation(self,question):
        # Récupération des données
        self.question = question
        # Création des fenètres de l'écran
        try :
            self.titreFenetre = curses.newwin(int(self.maxY/2), self.maxX, 0, 0)
            self.texteFenetre = curses.newwin(int(self.maxY * 0.1),self.maxX ,self.maxY - int(self.maxY * 0.1),0)
            self.texteZone = curses.newwin(int(self.maxY * 0.1)  -3  ,self.maxX  -3 ,self.maxY - int(self.maxY * 0.1) + 2, + 2)
        except Exception:
            print("Erreur : Les dimensions de l'écran sont trop petites !")
            self.stoper()
        # Initialisation des différentes fenètres
        self.initTitre()
        self.initTexte()

    def initTitre(self):
        # Ajout du titre au centre de l'écran
        try :
            self.titreFenetre.addstr(int(self.maxY/2)-2, int(self.maxX/2 - len(self.question)/2), self.question)
        except Exception :
            print("Erreur : Les dimensions de l'écran sont trop petites !")
            self.stoper()
        self.titreFenetre.refresh()

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

    def rechargementTexteZone(self):
        # Si la zone de texte est assez grande
        try :
            self.texteZone.addstr(0, 0, self.text)
            self.texteZone.refresh()
        # Sinon on suprime le caractère qu'on vient d'ajouter
        except Exception:
            self.text = self.text[:-1]

    def message(self, char):
        # Si le chat est actif
        if self.actif :
            # Si on clique sur entré
            if chr(char) == "\n":
                self.stoper()
                return
            # Si on est en train de supprimer
            elif chr(char) == self.charSuppression or chr(char) == "ć" or chr(char) == "\x7f":
                self.effacer()
                return
            # Sinon on ajoute le caractère à l'écran
            else:
                self.text += chr(char)
                self.rechargementTexteZone()
                return
        # Si on est pas actif on s'arrête
        else :
            return

    def effacer(self):
        # On supprime le dernier caractère
        self.text = self.text[:-1]
        self.texteZone.clear()
        self.rechargementTexteZone()

    def lancer(self):
        # Ajout du signal pour stopper avec un ctrl + C
        signal.signal(signal.SIGINT, self.stoper)
        # Tant que l'option est actif
        while self.actif:
            # On récupère les caractères saisie au clavier et on les traitent
            caractere = self.texteZone.getch()
            self.message(caractere)
        # Retourne la réponse à la question
        return self.text

    def stoper(self,signum=None, frame=None):
        # Fermeture de l'option
        self.actif=False
        # Fermeture de la fenètre
        curses.curs_set(1)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

