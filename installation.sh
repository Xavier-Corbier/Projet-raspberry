commande=$(sudo -nv 2>&1)
## exécute la commande et vérifie qu'elle s'est éxécuté avec succés
if [ $? -eq 0 ]; then
## il n'est pas nécésaire de demander le mot de passe pour avoir l'accès sudoers
echo "Installation en cours ..."
  git clone https://github.com/Xavier-Corbier/Projet-raspberry.git > /dev/null 2>&1
  ## création d'un utilisateur chat sur la raspberry sans mot de passe et sans interractiveté avec le terminal
  sudo adduser --disabled-password --gecos "" chat > /dev/null 2>&1
  ## copie du code source vers le répertoire de l'utilisateur chat
  sudo mv Projet-raspberry/ /home/chat/Projet-raspberry
  ## création de la commande chat
  sudo cp /home/chat/Projet-raspberry/chat /usr/bin/chat
  ## autorisation d'éxécuter la commande chat
  sudo chmod 777 /usr/bin/chat
  ## autorisation d'écritures de données
  sudo chmod 777 /home/chat/Projet-raspberry/données/messages.txt
  sudo chmod 777 /home/chat/Projet-raspberry/données/utilisateurs.txt
  echo "Installation terminé !"

elif echo $commande | grep -q '^sudo:'; then
## il est nécéssaire de demander le mot de passe pour avoir l'accès sudoers
echo "Erreur : Veuillez vérifier que vous avez tapper sudo avant la commande d'installation svp"
else
## l'utilisateur n'a pas les droits sudoers
echo "Erreur : Vous n'avez pas les droits administrateurs"
fi

