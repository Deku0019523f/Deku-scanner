#!/data/data/com.termux/files/usr/bin/bash

echo "📦 Installation des dépendances..."
pkg update -y && pkg upgrade -y
pkg install python -y
pkg install net-tools -y
pkg install termux-api -y
pkg install tsu -y
pkg install git -y

echo "✅ Dépendances installées."

chmod +x scan_root.sh scan_noroot.sh

echo "▶️ Lancement du serveur local :"
echo "  python server.py"
