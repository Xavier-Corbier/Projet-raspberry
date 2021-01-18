import curses, threading,curses.textpad,signal,time,os
from plugins import pluginGestionMessages as pgm, pluginGestionUtilisateurs as pgu, pluginFenetreOption as pfo
#from plugins import pluginGestionCapteurs as pgc

# Class qui permet le fonctionnement général du chat (envoi / récupération messages, gestion utilisateurs, affichage)

class Chat(object):

    # Crée le chat
    # Précondition :
    # - fenetre : fenetre curses - curses.initscr()
    # Résultat :
    # - Le chat est crée et il est connecté aux appli de gestion
    def __init__(self, fenetre):
        self.stdscr = fenetre
        self.nomUtilisateur = ""
        # Récupération des dimensions
        self.maxY, self.maxX = fenetre.getmaxyx()
        # Connexion aux données des appli de gestion de Messages et Utilisateurs
        self.gestionMessages = pgm.GestionMessages()
        self.gestionUtilisateurs = pgu.GestionUtilisateurs()
        # Gestion des capteurs
        #self.gestionCapteurs = pgc.GestionCapteurs()
        # Création du mutex
        self.mutex=threading.Lock()
        # Nettoyer l'écran
        self.stdscr.clear()

    ##
    #   PARTIE INITIALISATION
    ##

    # Initialise le chat
    # Résultat :
    # - Le chat est crée et il est connecté aux appli de gestion
    def initialisation(self):
        # Pas de répétition des caractères au clavier
        curses.noecho()
        curses.cbreak()
        # Pas de delai à l'affichage
        self.stdscr.nodelay(1)
        # Récupération du caractère pour supprimer
        self.charSuppression = curses.erasechar()
        # Ne pas afficher de curseurs à l'écran
        curses.curs_set(0)
        curses.doupdate()
        # Mise en place de l'affichage
        self.initialisationAffichage()
        # Conditions d'affichage
        self.afficherLed = False
        self.afficherEcran = False

    # Initialise l'affichage du chat
    # Résultat :
    # - L'affichage du chat et initialisé et chaque fenetre est crée
    def initialisationAffichage(self):
        # finY, finX, y, x
        try :
            # Création de chaque fenètre de traitement
            self.titreFenetre = curses.newwin(4, self.maxX, 0, 0)
            self.utilisateurFenetre = curses.newwin(self.maxY - 5,int(self.maxX * 0.25)-2,5,2)
            self.chatFenetre = curses.newwin(self.maxY - int(self.maxY * 0.1) - 5,self.maxX - int(self.maxX * 0.25),5,int(self.maxX * 0.25))
            self.texteFenetre = curses.newwin(int(self.maxY * 0.1),self.maxX - int(self.maxX * 0.25),self.maxY - int(self.maxY * 0.1),int(self.maxX * 0.25))

            ## Ce sont des fenètres superposées aux précédentes pour permettre un traitement plus simple
            self.utilisateurZone = curses.newwin(self.maxY - 8,int(self.maxX * 0.25)-6,7,5)
            self.chatZone = curses.newwin(self.maxY - int(self.maxY * 0.1) - 7,self.maxX - int(self.maxX * 0.25) - 3,6,int(self.maxX * 0.25) + 2)
            self.texteZone = curses.newwin(1,self.maxX - int(self.maxX * 0.25) - 2,self.maxY - int(self.maxY * 0.1) + 1,int(self.maxX * 0.25) + 1)
        except Exception :
            self.stoper()
            print("Erreur : les dimensions du terminal sont trop faibles")
        # Initialisation de chaques parties de l'écran
        self.initTitre()
        self.initChat()
        self.initTexte()
        self.initUtilisateur()

    # Initialise le titre du chat
    # Résultat :
    # - La partie titre du chat est initialisé si les dimensions le permettent
    def initTitre(self):
        # Ajout du titre au centre de l'écran
        name = "Chat"
        try :
            self.titreFenetre.addstr(2, int(self.maxX/2 - len(name)/2), name)
            self.titreFenetre.addstr(3, 3, "Options - envoyer :option ")
        except Exception :
            self.stoper()
            print("Erreur : les dimensions du terminal sont trop faibles")
        self.titreFenetre.refresh()

    # Initialise la partie chat du chat
    # Résultat :
    # - La partie chat du chat est initialisé
    def initChat(self):
        # Bordures de la fenètre
        self.chatFenetre.box()
        self.chatFenetre.refresh()
        self.chatZone.refresh()
        self.chatIndice = 0
        self.messageNombre = 0
        self.messageNombreHistorique = 0
        self.nombreMessageRemoter = 0

    # Initialise la partie texte du chat
    # Résultat :
    # - La partie texte du chat est initialisé
    def initTexte(self):
        # Bordures de la fenètre
        self.texteFenetre.box()
        self.texteFenetre.refresh()
        self.text = ""
        self.texteZone.refresh()

    # Initialise la partie utilisateur du chat
    # Résultat :
    # - La partie texte du chat est initialisé si les dimensions le permettent
    def initUtilisateur(self):
        # Ajout colonne utilisateurs
        try :
            self.utilisateurFenetre.addstr(1, 2, "Utilisateur(s) :")
        except Exception :
            self.stoper()
            print("Erreur : les dimensions du terminal sont trop faibles")
        # Bordures de la fenètre
        self.utilisateurFenetre.box()
        self.utilisateurFenetre.refresh()
        self.rechargementUtilisateur()

    ##
    #   PARTIE RECHARGEMENT
    ##

    # Recharge la partie chat du chat
    # Résultat :
    # - La partie chat du chat est rechargé avec les derniers messages reçu, ou avec les anciens messages souhaité
    def rechargementChat(self):
        # Rechargement de la chat Zone
        self.chatZone.erase()
        self.chatZone.refresh()
        y, x = self.chatZone.getmaxyx()
        # Rechargement de la liste des messages
        self.messageNombre = 0
        listeMessage = self.gestionMessages.listeDesMessages()
        # Tant que le nombre de message ne dépasse pas l'écran et qu'il est inférieur aux nombres de messages enregistré (moins le nombre de message remonté)
        while self.messageNombre  < y  and self.messageNombre  <len(listeMessage)-1 - self.nombreMessageRemoter:
            message = listeMessage[len(listeMessage)-2-self.messageNombre-self.nombreMessageRemoter]
            try :
                self.afficherMessage(message[0],message[1])
            except Exception :
                self.messageNombre+=1
                pass
        self.messageNombreHistorique = len(listeMessage)-self.messageNombre
        if len(listeMessage)!=0:
            if listeMessage[self.messageNombre-1][0] !="pi" and listeMessage[self.messageNombre-1][0] != "" and listeMessage[self.messageNombre-1][1]!="" :
                self.afficherLed=True

    # Recharge la partie utilisateur du chat
    # Résultat :
    # - La partie utilisateur du chat est rechargé avec les derniers utilisateurs
    def rechargementUtilisateur(self):
        # Rechargement de la zone utilisateur
        self.utilisateurZone.erase()
        self.utilisateurZone.refresh()
        y, x = self.utilisateurZone.getmaxyx()
        # Rechargement de la liste des utilisateurs
        self.utilisateurIndice = 0
        self.nombreUtilisateurs = 0
        listeUtilisateurs = self.gestionUtilisateurs.listeDesUtilisateurs()
        for user in listeUtilisateurs :
            try:
                if len(user)>x :
                    self.utilisateurZone.addstr(self.utilisateurIndice+3, 0, user[:x-1])
                else:
                    self.utilisateurZone.addstr(self.utilisateurIndice+3, 0, user)
            except Exception :
                pass
            self.utilisateurIndice+=1
            if user !="" :
                self.nombreUtilisateurs+=1
        self.utilisateurZone.refresh()

    # Recharge la partie texte du chat
    # Résultat :
    # - La partie texte du chat est rechargé avec les dernieres lettres tappé
    def rechargementTexteZone(self):
        # Rechargement de la zone texte
        self.texteZone.erase()
        self.texteZone.refresh()
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
        try :
            # Si le chat est actif
            if self.actif :
                # Si on envoie un message
                if chr(char) == "\n" :
                    # Si il correspond à un changement de nom d'utilisateur
                    if self.text == ":changerNom" :
                        self.stoper()
                        # Démarrage d'une FenetreOption
                        option = curses.wrapper(pfo.FenetreOption)
                        option.initialisation(["Changement de pseudo :","(Appuyez sur Entrée pour quitter)"])
                        # Récupération de la réponse
                        reponse = option.lancer()
                        if reponse != "" :
                            self.nomUtilisateur = reponse
                        # Redémarrage du chat
                        self.lancer()
                    # Si on veut accéder aux option
                    elif self.text == ":option" :
                        self.stoper()
                        # Démarrage d'une FenetreOption
                        option = curses.wrapper(pfo.FenetreOption)
                        option.initialisation(["Option du chat :","(Appuyez sur Entrée pour quitter)", "",":changerNom - Changer de nom d'utilisateur temporairement", ":p - Messages précédent", ":s Messages suivant", ":quitter - Quitter le chat"],False)
                        # Récupération de la réponse
                        _ = option.lancer()
                        # Redémarrage du chat
                        self.lancer()
                    # Si on veut accéder aux messages précédent
                    elif self.text == ":p" :
                        # Si on remonte pas plus de messages qu'il en existe
                        if self.nombreMessageRemoter < self.messageNombre + self.messageNombreHistorique - 1 :
                            self.nombreMessageRemoter +=1
                        with self.mutex:
                            self.rechargementChat()
                            self.text=""
                        with self.mutex:
                            self.rechargementTexteZone()
                    # Si on veut accéder aux messages suivant
                    elif self.text == ":s" :
                        # Si le nombre de messages remonté est positif
                        if self.nombreMessageRemoter > 0:
                            self.nombreMessageRemoter -=1
                        with self.mutex:
                            self.rechargementChat()
                            self.text=""
                        with self.mutex:
                            self.rechargementTexteZone()
                    # Si on veut quitter le chat
                    elif self.text == ":quitter" :
                        self.stoper()
                    # Sinon on envoie le message
                    else :
                        if self.nombreMessageRemoter != 0:
                            self.nombreMessageRemoter =0
                        self.envoyerMessage()
                    return
                # Si on est en train de supprimer
                elif chr(char) == self.charSuppression or chr(char) == "ć" or chr(char) == "\x7f":
                    self.effacer()
                    return
                # Sinon on ajoute le caractère à l'écran
                else:
                    y, x = self.chatZone.getmaxyx()
                    if len(self.text)+1 < x:
                        self.text += chr(char)
                    with self.mutex:
                        self.rechargementTexteZone()
                    return
            # Si on est pas actif on s'arrête
            else :
                return
        except Exception :
            return

    # Efface le dernier caractère écrit sur la partie texte du chat
    # Résultat :
    # - Le dernier caractère est effacé
    def effacer(self):
        # On supprime le dernier caractère
        self.text = self.text[:-1]
        self.texteZone.clear()
        with self.mutex :
            self.rechargementTexteZone()

    ##
    #   PARTIE GESTION MESSAGES UTILISATEURS
    ##

    # Récupère les messages du chat
    # Précondition :
    # - Doit être utilisé avec un Thread
    # Résultat :
    # - La liste des messages est contrôlé toutes les 0.1 s
    def recupererMessages(self):
        while self.actif:
            # Delai de 0.1 pour économiser les calculs
            time.sleep(0.1)
            # On récupère la liste des utilisateurs
            listeMessage = self.gestionMessages.listeDesMessages()
            # Si le nombre est différent de celui que l'on connait et si on remonte pas des messages
            if self.messageNombre + self.messageNombreHistorique != len(listeMessage) and self.nombreMessageRemoter==0:
                with self.mutex :
                    self.rechargementChat()

    # Envoie le message écrit sur le chat
    # Résultat :
    # - Le message a été envoyé
    def envoyerMessage(self):
        # Réinitialisation de la zonne de texte
        message = self.text
        self.text = ""
        with self.mutex :
            self.rechargementTexteZone()
        # Si le message n'est pas vide
        if message !="":
            self.gestionMessages.envoyerMessage(self.nomUtilisateur,message)

    # Affiche un messages sur la partie chat du chat
    # Précondition :
    # - utilisateur : utilisateur qui envoie le message
    # - chat : message a envoyé
    # Résultat :
    # - Le message est affiché
    def afficherMessage(self,utilisateur,chat):
        # Récupération des dimensions de la chat zone
        y, x = self.chatZone.getmaxyx()
        ligne = str(utilisateur) + ' : ' + str(chat)
        texte = ligne
        try:
            # Si le message est trop long
            if len(ligne)>x :
                texte = ligne[:x-1]

            if self.nomUtilisateur == utilisateur :
                self.chatZone.addstr(y-1-self.messageNombre, 0, texte, curses.A_BOLD)
            else :
                self.chatZone.addstr(y-1-self.messageNombre, 0, texte)

        except Exception:
            with self.mutex :
                self.rechargementChat()
        self.chatZone.refresh()
        self.messageNombre+=1

    ##
    #   PARTIE GESTION UTILISATEURS
    ##

    # Récupère les utilisateurs du chat
    # Précondition :
    # - Doit être utilisé avec un Thread
    # Résultat :
    # - La liste des utilisateurs est contrôlé toutes les 0.1 s
    def recupererUtilisateurs(self):
        while self.actif:
            # Delai de 0.1 pour économiser les calculs
            time.sleep(0.1)
            # On récupère la liste des utilisateurs
            listeUtilisateurs=self.gestionUtilisateurs.listeDesUtilisateurs()
            # Si le nombre est différent de celui que l'on connait
            if self.utilisateurIndice != len(listeUtilisateurs) :
                with self.mutex :
                    self.rechargementUtilisateur()

    # Ajout le nom de l'utilisateur au chat
    # Résultat :
    # - L'utilisateur est ajouté
    def ajouterUtilisateur(self):
        self.gestionUtilisateurs.ajouterUtilisateur(self.nomUtilisateur)

    # Supprime le nom de l'utilisateur du chat
    # Résultat :
    # - L'utilisateur est supprimé
    def supprimerUtilisateur(self):
        self.gestionUtilisateurs.supprimerUtilisateur(self.nomUtilisateur)

    # Ejecte tout les utilisateurs
    def ejectionUtilisateurs(self):
        self.gestionUtilisateurs.initialisationNombreUtilisateurs()

    ##
    #   PARTIE VERIFICATION
    ##

    # Vérifie si un capteur doit être activé
    # Précondition :
    # - Doit être utilisé avec un Thread
    # Résultat :
    # - Les capteurs sont contrôlé
    def verificationCapteurs(self):
        while self.actif :
            time.sleep(0.1)
            if self.afficherLed :
                #self.gestionCapteurs.alumerLed()
                print("j'allume la led")
                self.afficherLed = False
            if self.afficherEcran :
                #self.gestionCapteurs.afficherMessage(str(self.nombreUtilisateurs))
                print("J'affiche l'écran")
                self.afficherEcran = False
            #if self.gestionCapteurs.boutonEstActif() :
                #self.ejectionUtilisateurs()

    # Vérifie si l'utilisateur est enregistré
    # Précondition :
    # - Doit être utilisé avec un Thread
    # Résultat :
    # - L'activité est stoppé si l'utilisateur n'est plus enregistré
    def verificationSiEstEnregistre(self):
        while self.actif :
            time.sleep(0.1)
            if not self.gestionUtilisateurs.estUnUtilisateurEnregistre(self.nomUtilisateur):
                self.actif = False

    ##
    #   PARTIE ACTIVITE PROGRAMME
    ##

    # Lance le chat
    # Résultat :
    # - Le chat est lancé avec les threads de gestion, et le signal Ctrl + C est activé pour stopper le chat
    def lancer(self):
        # Activation du chat
        self.actif = True
        self.initialisation()
        self.ajouterUtilisateur()
        # Lancement des threads
        threading.Thread(target=self.recupererMessages).start()
        threading.Thread(target=self.recupererUtilisateurs).start()
        threading.Thread(target=self.verificationCapteurs).start()
        threading.Thread(target=self.verificationSiEstEnregistre).start()
        # Demande d'afficher le nombre d'utilisateur à l'écran
        self.afficherEcran=True
        # Ajout du signal pour stopper avec un ctrl + C
        signal.signal(signal.SIGINT, self.stoper)
        # Aucun délai au clavier
        self.texteFenetre.nodelay(1)
        # Tant que le chat est actif
        while self.actif:
            # On récupère les caractères saisie au clavier et on les traitent
            caractere = self.texteFenetre.getch()
            self.message(caractere)
        self.stoper()

    # Stoppe le chat
    # Précondition :
    # - signum,frame : Paramètre facultatif qui sont utile pour lier à un signal
    # Résultat :
    # - Le chat est stoppé
    def stoper(self,signum=None, frame=None):
        # sauvegarde du dernier nombre d'utulisateurs
        nombreUtilisateurs = self.nombreUtilisateurs
        # Fermeture du chat
        self.actif=False
        self.supprimerUtilisateur()
        # Attendre que les threads se terminent
        time.sleep(0.1)
        # Afficher le dernier nombre d'utilisateurs
        #self.gestionCapteurs.afficherMessage(str(nombreUtilisateurs-1))
        # Nettoyer l'écran
        self.stdscr.clear()
        # Fermeture de la fenètre
        curses.curs_set(1)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

# Cette méthode est utilisé pour les test de Chat.py
if __name__ == "__main__":
    print("test programme")

