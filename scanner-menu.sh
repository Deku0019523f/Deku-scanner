#!/data/data/com.termux/files/usr/bin/bash

clear
echo -e "\e[36m###################################\e[0m"
echo -e "\e[36m#                                 #\e[0m"
echo -e "\e[36m#        \e[1;33mDEKU225-SCAN\e[0;36m             #\e[0m"
echo -e "\e[36m#                                 #\e[0m"
echo -e "\e[36m###################################\e[0m"

echo -e "\n\e[32m[1] Analyse SANS ROOT"
echo -e "[2] Analyse AVEC ROOT"
echo -e "[3] Quitter\e[0m"

read -p $'\n\e[34mCHOISISSEZ UNE OPTION : \e[0m' option

case "$option" in
  1)
    echo -e "\n\e[33m🔎 Lancement de l'analyse sans root...\e[0m\n"
    bash scan_noroot.sh
    ;;
  2)
    echo -e "\n\e[31m🔐 Lancement de l'analyse avec root...\e[0m\n"
    tsu -c bash scan_root.sh
    ;;
  3)
    echo -e "\n\e[35m🔚 Fin du programme.\e[0m"
    exit 0
    ;;
  *)
    echo -e "\n\e[31m❌ Option invalide\e[0m"
    ;;
esac
