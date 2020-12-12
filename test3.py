import curses,os,threading,curses.textpad

class Chat(object):
    startPos = 0
    # proportion of the left panel body, to the chat panel
    body_proportion = 0.20
    # proportion of textarea vertically to the chat panel
    text_area_proportion = 0.20

    def __init__(self, screen):
        self.stdscr = screen
        self.nickname = ""
        self.messageNumber = 0
        self.messageNumberHistory = 0
        self.actif = True

    def setup(self):

        # set getch to blocking
        self.stdscr.nodelay(0)
        # don't echo key strokes on the screen
        curses.noecho()
        # read keystrokes instantly, without waiting for enter to be pressed
        curses.cbreak()
        # enable keypad mode
        self.stdscr.keypad(1)
        # draw the main frame
        self.setup_draw()
        curses.curs_set(0)
        # find what's the erase character
        self.del_char = curses.erasechar()
        self.backspace()

    def setup_draw(self):

        # get screen dimensions
        self.maxY, self.maxX = self.stdscr.getmaxyx()
        # n_lines, n_cols, begin_y, begin_x
        self.head_win = curses.newwin(1, self.maxX, 0, 0)
        # left panel, contacts
        self.user_win = curses.newwin(
            self.maxY - 1,
            int(self.maxX * self.body_proportion),
            1,
            0)
        # chat frame
        self.chat_win = curses.newwin(
            self.maxY - 1 - int(self.maxY * self.text_area_proportion),
            self.maxX - int(self.maxX * self.body_proportion),
            1,
            int(self.maxX * self.body_proportion))

        self.chatareaHeight = self.maxY - 1 - int(self.maxY * self.text_area_proportion) - 2
        # chat window (displays text)
        self.chatarea = curses.newwin(
            self.chatareaHeight,
            self.maxX - int(self.maxX * self.body_proportion) - 2,
            2,
            int(self.maxX * self.body_proportion) + 1)
        # bottom frame window
        self.text_win = curses.newwin(
            int(self.maxY * self.text_area_proportion),
            self.maxX - int(self.maxX * self.body_proportion),
            self.maxY - int(self.maxY * self.text_area_proportion),
            int(self.maxX * self.body_proportion))
        # bottom textarea
        self.textarea = curses.newwin(
            int(self.maxY * self.text_area_proportion) - 2,
            self.maxX - int(self.maxX * self.body_proportion) - 2,
            self.maxY - int(self.maxY * self.text_area_proportion) + 1,
            int(self.maxX * self.body_proportion) + 1)

        self.init_head()
        self.init_chat()
        self.init_chatarea()
        self.init_textbox()
        self.init_textarea()
        self.init_user()
        self.user_win.keypad(1)


    def init_head(self):
        name = "Chat"
        middle_pos = int(self.maxX/2 - len(name)/2)
        self.head_win.addstr(0, middle_pos, name)
        self.head_win.refresh()

    def init_body(self):
        self.user_win.addstr(1, 1, "Utilisateur(s) :")
        self.user_win.box()
        self.user_win.refresh()


    def init_chat(self):

        self.chat_max_y, self.chat_max_x = self.chat_win.getmaxyx()
        self.chat_win.box()
        self.chat_win.refresh()

    def init_chatarea(self):

        self.chatarea.refresh()
        # represents the y position where to start writing chat
        self.chat_at = 0

    def init_textbox(self):

        self.text_win.box()
        self.text_win.refresh()

    def init_textarea(self):

        # the current displayed text
        self.char_pos = [0, 0]
        self.text = ""
        self.textarea.refresh()

    def refresh_textarea(self, char=None):

        self.textarea.addstr(0, 0, self.text)
        self.textarea.refresh()

    def update_chat(self):

        self.chatarea.clear()
        self.chat_at = 0
        self.chatarea.refresh()

    def init_user(self):

        self.user_win.clear()
        self.body_at = 0
        self.user_win.refresh()
        self.init_body()
        fichier = open("users.txt", "r")
        users =fichier.read()
        fichier.close()

        listUsers = users.split("\n")

        for user in listUsers :

            self.user_win.addstr(self.body_at+3, 1, user)
            self.body_at+=1
        self.user_win.refresh()
        
    def backspace(self):
        self.text = self.text[:-1]
        self.textarea.clear()
        self.refresh_textarea()

    def send_text(self):

        fichier = open("messages.txt", "a+")
        fichier.write(self.nickname+" : "+self.text+"\n")
        fichier.close()

        self.char_pos = [1, 1]
        self.text = ""
        self.textarea.clear()
        self.refresh_textarea()

    def push_chat(self,user,chat):

        try:
            self.chatarea.addstr(self.chat_at, 0, str(user) + ': ')

        except Exception:
            self.refreshChat()
            self.chatarea.addstr(self.chat_at, 0, str(user) + ': ')

        # write the actual chat content
        self.chatarea.addstr(chat)
        self.chatarea.refresh()
        # update cursor
        self.chat_at, _ = self.chatarea.getyx()
        self.chat_at += 1

    def getMessages(self):

        while self.actif:
            fichier = open("messages.txt", "r")
            chat =fichier.read()
            fichier.close()

            listMessage = chat.split("\n")

            if self.messageNumber + self.messageNumberHistory < len(listMessage)-1 :
                message = listMessage[self.messageNumber + self.messageNumberHistory].split(":")
                self.push_chat(message[0],message[1])
                self.messageNumber+=1
                
    def getUsers(self):

        while self.actif:
            fichier = open("users.txt", "r")
            users =fichier.read()
            fichier.close()

            listUsers = users.split("\n")

            if self.body_at != len(listUsers) :
                self.init_user()

    def add_user(self):

        fichier = open("users.txt", "a+")
        fichier.write(self.nickname+"\n")
        fichier.close()

    def remove_user(self):

        fichier = open("users.txt", "r")
        users =fichier.read()
        fichier.close()

        listUsers = users.split("\n")

        fichier = open("users.txt", "w")
        nombreSupprime = 0
        for user in listUsers:
            if nombreSupprime == 0:
                if user.split("\n")[0]!=self.nickname and user !="":
                    fichier.write(user+"\n")
                nombreSupprime +=1
            else :
                if user !="":
                    fichier.write(user+"\n")
        fichier.close()

    def refreshChat(self):

        self.chatarea.erase()
        self.chat_at = 0
        self.chatarea.refresh()
        self.messageNumberHistory += self.messageNumber
        self.messageNumber = 1

    def keypress(self, char):

        if chr(char) == "\n":

            self.messageNumber += 1
            self.push_chat(self.nickname,self.text)
            self.send_text()
            return

        elif chr(char) == self.del_char or chr(char) == "ć" or chr(char) == "\x7f":
            self.backspace()
            return

        else:
            self.text += chr(char)
            self.refresh_textarea(char)
            return

    def run(self):

        while True:
            c = self.user_win.getch()
            self.keypress(c)

    def stop(self):

        self.actif=False
        self.remove_user()

        curses.echo()
        curses.curs_set(1)
        curses.nocbreak()

        self.stdscr.keypad(0)
        curses.endwin()

# This method is callable for testing porpuses only
if __name__ == "__main__":

    chat = curses.wrapper(Chat)
    chat.nickname = os.environ["USER"]

    chat.add_user()
    chat.setup()

    threading.Thread(target=chat.getMessages).start()
    threading.Thread(target=chat.getUsers).start()

    while True:
        try:
            chat.run()
        except KeyboardInterrupt:
            chat.stop()
            exit(0)
