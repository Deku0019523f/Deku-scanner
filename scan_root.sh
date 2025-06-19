#!/data/data/com.termux/files/usr/bin/bash

echo -e "\e[1;31m=== 📦 STOCKAGE COMPLET ===\e[0m"
df -h

echo -e "\n\e[1;31m=== 🧠 RAM ===\e[0m"
free -h

echo -e "\n\e[1;31m=== 🔋 BATTERIE ===\e[0m"
termux-battery-status

echo -e "\n\e[1;31m=== 📱 APPLICATIONS INSTALLÉES ===\e[0m"
pm list packages

echo -e "\n\e[1;31m=== 👀 PROCESSUS SUSPECTS ===\e[0m"
ps aux | grep -i "crypto\|miner\|tor\|root" || echo "Aucun processus suspect trouvé"

echo -e "\n\e[1;31m=== 🌐 PORTS OUVERTS ===\e[0m"
netstat -tuln
