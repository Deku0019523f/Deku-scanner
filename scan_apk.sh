#!/data/data/com.termux/files/usr/bin/bash

APK="$1"

if [ -z "$APK" ]; then
  echo -e "\e[31m❌ Chemin de l'APK manquant.\e[0m"
  echo "Usage : bash scan_apk.sh /chemin/vers/fichier.apk"
  exit 1
fi

if [ ! -f "$APK" ]; then
  echo -e "\e[31m❌ Fichier introuvable : $APK\e[0m"
  exit 1
fi

echo -e "\e[34m=== 📄 FICHIER APK ===\e[0m"
echo "Nom du fichier : $(basename "$APK")"
echo "Taille : $(du -h "$APK" | cut -f1)"
echo "SHA256 : $(sha256sum "$APK" | cut -d' ' -f1)"

echo -e "\n\e[34m=== 🔐 PERMISSIONS (si aapt est installé) ===\e[0m"
if command -v aapt >/dev/null 2>&1; then
  aapt dump permissions "$APK"
else
  echo "⚠️ 'aapt' non trouvé. Installez-le avec : pkg install aapt"
fi

read -p $'\n\e[33m👉 Voulez-vous envoyer l'APK à VirusTotal ? (o/n) : \e[0m' answer
if [[ "$answer" =~ ^[Oo]$ ]]; then
  echo -e "\n⏳ Envoi à VirusTotal..."
  RESPONSE=$(curl --silent --request POST \
    --url https://www.virustotal.com/api/v3/files \
    --header 'x-apikey: 1131775d5d74f8457607cad7681f4ac68d904c176f9b1f6eeeb660374db398ed' \
    --form file=@"$APK")

  SCAN_ID=$(echo "$RESPONSE" | grep -o '"id": *"[^"]*' | cut -d'"' -f4)
  if [ -n "$SCAN_ID" ]; then
    echo -e "\n✅ Fichier envoyé ! Résultats en attente..."
    echo "Lien : https://www.virustotal.com/gui/file/$SCAN_ID"
  else
    echo -e "\n❌ Erreur d’envoi. Réponse :"
    echo "$RESPONSE"
  fi
else
  echo -e "\n⏭️ Envoi annulé."
fi
