#!/data/data/com.termux/files/usr/bin/bash

echo -e "\e[1;34m=== 🌐 CONNEXIONS ACTIVES ===\e[0m"
netstat -antp | grep ESTABLISHED || echo "Aucune connexion active"

echo -e "\n\e[1;34m=== 🌍 ADRESSES IP LOCALES ===\e[0m"
ip addr | grep 'inet '

echo -e "\n\e[1;34m=== 🔎 PORTS OUVERTS LOCAUX ===\e[0m"
netstat -tuln

echo -e "\n\e[1;34m=== 📡 PING GOOGLE ===\e[0m"
ping -c 3 google.com

echo -e "\n\e[1;34m=== 📶 SCAN DE RÉSEAU LOCAL (nmap requis) ===\e[0m"
if command -v nmap >/dev/null 2>&1; then
  ip route | awk '/default/ {print $3}' | xargs -I{} nmap -sn {}/24
else
  echo "⛔ nmap non installé. Installez-le avec : pkg install nmap"
fi
