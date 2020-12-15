import curses,os,threading,curses.textpad,signal
import Chat as appChat

chat = appChat.Chat(curses.initscr())
chat.nomUtilisateur = os.environ["USER"]

chat.ajouterUtilisateur()
chat.lancer()
