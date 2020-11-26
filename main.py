import curses,os,sys
from curses.textpad import Textbox, rectangle



def affichage(stdscr):

    stdscr.clear()
    stdscr.refresh()

    while True:

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

        stdscr.refresh()

def lectureMessage(stdscr):

    while True :

        messageZon_uly = (int(stdscr.getmaxyx()[0] * 0.9 + 1))
        messageZon_ulx = (int(stdscr.getbegyx()[1])+2)
        messageZon_lry = (int(stdscr.getmaxyx()[0] - 1))
        messageZon_lrx = (int(stdscr.getmaxyx()[1] * 0.8 - 2))

        messageZon = curses.newwin(1, messageZon_lrx-4, messageZon_uly+3, messageZon_ulx+2)

        box = Textbox(messageZon)
        box.edit()
        message = box.gather()
        fichier = open("messages.txt", "a")
        fichier.write("user : "+message+"\n")
        fichier.close()
        message =""



def main():

    # On lance les 3 processus
    for i in range(3):

        # On fork un processus
        pid = os.fork()

        # Si je suis un fils
        if pid == 0:

            # Si je suis le premier
            if i==0 :
                curses.wrapper(affichage)
            elif i==1 :
                curses.wrapper(lectureMessage)
            elif i==2 :
                sys.exit(i)


    # On tue tout les fils
    for i in range(3):
        pid,status = os.wait()



if __name__ == "__main__":
    main()