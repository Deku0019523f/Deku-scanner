#!/data/data/com.termux/files/usr/bin/bash

clear
echo -e "\e[36m##########################################\e[0m"
echo -e "\e[36m#                                        #\e[0m"
echo -e "\e[36m#          \e[1;33mDEKU225-SCAN TOOLKIT\e[0;36m         #\e[0m"
echo -e "\e[36m#                                        #\e[0m"
echo -e "\e[36m##########################################\e[0m"

echo -e "\n\e[32m[1] Scan SYSTÈME (sans root)"
echo "[2] Scan AVANCÉ (root requis)"
echo "[3] Scan SÉCURITÉ (réseau, ports, connexions)"
echo "[4] Scan APK malveillant"
echo "[5] Quitter\e[0m"

read -p $'\n\e[34mCHOISISSEZ UNE OPTION : \e[0m' option

case "$option" in
  1)
    echo -e "\n\e[33m🔎 Scan Système...\e[0m\n"
    bash scan_noroot.sh
    ;;
  2)
    echo -e "\n\e[31m🔐 Scan Avancé (Root)...\e[0m\n"
    tsu -c bash scan_root.sh
    ;;
  3)
    echo -e "\n\e[36m🛡️ Scan de sécurité réseau...\e[0m\n"
    bash scan_network.sh
    ;;
  4)
    read -p $'\n📂 Chemin vers l'APK à analyser : ' chemin
    bash scan_apk.sh "$chemin"
    ;;
  5)
    echo -e "\n\e[35m🔚 Fin du programme.\e[0m"
    exit 0
    ;;
  *)
    echo -e "\n\e[31m❌ Option invalide\e[0m"
    ;;
esac
