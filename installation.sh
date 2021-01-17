commande=$(sudo -nv 2>&1)
## exécute la commande et vérifie qu'elle s'est éxécuté avec succés
if [ $? -eq 0 ]; then
## il n'est pas nécésaire de demander le mot de passe pour avoir l'accès sudoers
echo "Installation en cours ..."
  if which git | grep -q '^/'; then
    ## cacher le résultat du git clone
    echo "Téléchargement du programme chat ..."
  else
    ## la commande git n'est pas présente sur l'os
    echo "Installation programmes nécéssaire"
    sudo apt install git-all
    ## Fin installation programme nécéssaire
    echo "Installation programme nécéssaire fini"
    ## cacher le résultat du git clone
    echo "Téléchargement du programme chat ..."
  fi
  git clone https://github.com/Xavier-Corbier/Projet-raspberry.git > /dev/null 2>&1
  ## Création d'un utilisateur chat sur la raspberry sans mot de passe et sans interractiveté avec le terminal
  sudo adduser --disabled-password --gecos "" chat > /dev/null 2>&1


elif echo $commande | grep -q '^sudo:'; then
## il est nécéssaire de demander le mot de passe pour avoir l'accès sudoers
echo "Erreur : Veuillez vérifier que vous avez tapper sudo avant la commande d'installation svp"
else
## l'utilisateur n'a pas les droits sudoers
echo "Erreur : Vous n'avez pas les droits administrateurs"
fi

