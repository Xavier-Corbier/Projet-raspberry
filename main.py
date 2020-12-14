import curses,os,threading,curses.textpad,signal
import Chat as appChat

chat = curses.wrapper(appChat.Chat)
chat.nomUtilisateur = os.environ["USER"]

chat.ajouterUtilisateur()
chat.initialisation()

threading.Thread(target=chat.recupererMessages).start()
threading.Thread(target=chat.recupererUtilisateurs).start()

signal.signal(signal.SIGINT, chat.stoper)

chat.lancer()
