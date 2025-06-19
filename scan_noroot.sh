#!/data/data/com.termux/files/usr/bin/bash

echo -e "\e[1;34m=== 📦 STOCKAGE ===\e[0m"
df -h /data | grep -v Filesystem

echo -e "\n\e[1;34m=== 🧠 MÉMOIRE (RAM) ===\e[0m"
free -h

echo -e "\n\e[1;34m=== 🔋 BATTERIE ===\e[0m"
termux-battery-status | jq

echo -e "\n\e[1;34m=== 📱 APPLICATIONS INSTALLÉES ===\e[0m"
pm list packages | head -n 10

echo -e "\n\e[1;34m=== 🌐 CONNEXIONS RÉSEAU ACTIVES ===\e[0m"
netstat -antp | grep ESTABLISHED || echo "Aucune connexion active"
