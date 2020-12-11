import curses,os,sys,signal
from curses.textpad import Textbox, rectangle




def main(stdscr):

            stdscr.clear()
            stdscr.refresh()

            # Affichage du titre du chat
            titre = 'Chat'

            stdscr.addstr(2, int(stdscr.getmaxyx()[1]/2+len(titre)/2), titre)


            # Affichage de la chatZone
            chatZone_uly = (int(stdscr.getbegyx()[0])+4)
            chatZone_ulx = (int(stdscr.getbegyx()[1])+2)
            chatZone_lry = (int(stdscr.getmaxyx()[0] * 0.9))
            chatZone_lrx = (int(stdscr.getmaxyx()[1] * 0.8 - 2))

            rectangle(stdscr, chatZone_uly, chatZone_ulx, chatZone_lry, chatZone_lrx)


            # Affichage de la liste des utilisateurs
            utilisateurZone_uly = (int(stdscr.getbegyx()[0])+3)
            utilisateurZone_ulx = (int(stdscr.getmaxyx()[1] * 0.8))
            utilisateurZone_lry = (int(stdscr.getmaxyx()[0] - 1))
            utilisateurZone_lrx = (int(stdscr.getmaxyx()[1] - 2))


            rectangle(stdscr, utilisateurZone_uly+1, utilisateurZone_ulx, utilisateurZone_lry, utilisateurZone_lrx)
            stdscr.addstr(utilisateurZone_uly+2, utilisateurZone_ulx+2, 'Utilisateurs :')


            # Affichage de la zone pour écrire
            messageZone_uly = (int(stdscr.getmaxyx()[0] * 0.9 + 1))
            messageZone_ulx = (int(stdscr.getbegyx()[1])+2)
            messageZone_lry = (int(stdscr.getmaxyx()[0] - 1))
            messageZone_lrx = (int(stdscr.getmaxyx()[1] * 0.8 - 2))

            rectangle(stdscr, messageZone_uly, messageZone_ulx, messageZone_lry, messageZone_lrx)
            stdscr.addstr(messageZone_uly+1, 4, 'Ecrire un message :')


            #stdscr.clear()
            stdscr.refresh()

            # On lance les 3 processus
            for i in range(1):

                # On fork un processus
                pid = os.fork()

                # Si je suis un fils
                if pid == 0:

                    # Si je suis le premier
                    if i==0 :
                        curses.wrapper(lectureMessage)
                        sys.exit(i)
                    if i==1 :
                        curses.wrapper(affichageMessage)
                        sys.exit(i)
                # On tue tout les fils
            for i in range(1):
                pid,status = os.wait()


def lectureMessage(stdscr):

        messageZone_uly = (int(stdscr.getmaxyx()[0] * 0.9 + 1))
        messageZone_ulx = (int(stdscr.getbegyx()[1])+2)
        messageZone_lrx = (int(stdscr.getmaxyx()[1] * 0.8 - 2))

        while boolCondition :

            messageZone = curses.newwin(1, messageZone_lrx-4, messageZone_uly+3, messageZone_ulx+2)

            box = Textbox(messageZone)


            box.edit(verificationClavier)
            message = box.gather()
            fichier = open("messages.txt", "a+")
            fichier.write("user : "+message+"\n")
            fichier.close()
            stdscr.refresh()
            message =""

def affichageMessage(stdscr):
    global boolRepeat
    messageZone_lry = (int(stdscr.getmaxyx()[0] - 1))
    taille = os.path.getsize("messages.txt")

    while boolCondition:
            nouvelleTaille = os.path.getsize("messages.txt")
            if  nouvelleTaille != taille :
                taille = nouvelleTaille

                fichier = open("messages.txt", "r")
                chat =fichier.read()
                fichier.close()
                listMessage = chat.split("\n")
                i=0
                while i<len(listMessage) :
                    stdscr.addstr(messageZone_lry-5-i, 4, listMessage[len(listMessage)-i-1])
                    stdscr.refresh()

                    i+=1
def verificationClavier(x) :
    global boolRepeat
    # Si le programme n'est pas stoppé on renvoie la valeur qu'on a écrit
    if boolCondition :
        return x
    # Sinon on renvoie une valeur de fin (Simulation de Entrée au clavier)
    else :
        boolRepeat = False
        return 10


def interruptionProgramme(signum, frame):
    global boolCondition
    boolCondition = False


if __name__ == "__main__":

    # Variable global qui gère l'activité du programme
    boolCondition = True
    boolRepeat = True
    # Si un signal d'interruption est reçu , on stoppe le programme
    signal.signal(signal.SIGINT, interruptionProgramme)

    # Lancement de la fonction principale
    curses.wrapper(main)
