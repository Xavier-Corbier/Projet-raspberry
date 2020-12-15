import curses,os,threading,curses.textpad,signal

class Option(object):

    def __init__(self, fenetre):

        self.stdscr = fenetre
        self.question = ""
        self.text = ""
        self.actif = True
        # récupération des dimensions
        self.maxY, self.maxX = fenetre.getmaxyx()

        # Pas de répétition des caractères au clavier
        curses.noecho()
        curses.cbreak()

        # Récupération du caractère pour supprimer
        self.charSuppression = curses.erasechar()

    def initialisation(self,question):

        self.question = question

        self.titreFenetre = curses.newwin(int(self.maxY/2), self.maxX, 0, 0)
        self.texteFenetre = curses.newwin(int(self.maxY * 0.1),self.maxX ,self.maxY - int(self.maxY * 0.1),0)
        self.texteZone = curses.newwin(int(self.maxY * 0.1)  -3  ,self.maxX  -3 ,self.maxY - int(self.maxY * 0.1) + 2, + 2)

        self.initTitre()
        self.initTexte()
        self.initTexteZone()

        self.effacer()

    def initTitre(self):
        self.titreFenetre.addstr(int(self.maxY/2)-2, int(self.maxX/2 - len(self.question)/2), self.question)
        self.titreFenetre.refresh()

    def initTexte(self):
        self.texteFenetre.addstr(1,1, "Réponse :")
        self.texteFenetre.box()
        self.texteFenetre.refresh()

    def initTexteZone(self):
        self.text = ""
        self.texteZone.refresh()

    def rechargementTexteZone(self):
        self.texteZone.addstr(0, 0, self.text)
        self.texteZone.refresh()

    def message(self, char):

        if self.actif :
            if chr(char) == "\n":

                self.stoper()
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

    def lancer(self):

        signal.signal(signal.SIGINT, self.stoper)

        while self.actif:
            caractere = self.texteZone.getch()
            self.message(caractere)

        return self.text

    def stoper(self,signum=None, frame=None):

        self.actif=False

        curses.echo()
        curses.nocbreak()

        curses.endwin()

