import curses,os,threading,curses.textpad,signal
import chat as appChat

# Création de la fenètre de Chat
chat = appChat.Chat(curses.initscr())

chat.lancer()
