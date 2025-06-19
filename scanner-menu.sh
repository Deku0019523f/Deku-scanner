#!/data/data/com.termux/files/usr/bin/bash

clear
echo ""
echo "###################################"
echo "#                                 #"
echo "#        DEKU225-SCAN             #"
echo "#                                 #"
echo "###################################"

echo ""
echo "[1] Analyse SANS ROOT"
echo "[2] Analyse AVEC ROOT"
echo "[3] Quitter"

read -p $'
CHOISISSEZ UNE OPTION : ' option

case "$option" in
  1)
    bash scan_noroot.sh
    ;;
  2)
    tsu -c bash scan_root.sh
    ;;
  3)
    echo -e "\nFin du programme."
    exit 0
    ;;
  *)
    echo -e "\nOption invalide"
    ;;
esac
