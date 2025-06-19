#!/data/data/com.termux/files/usr/bin/bash
echo "🔒 Analyse Root"
echo "📦 Stockage complet :"
df -h

echo ""
echo "🧠 RAM :"
free -h

echo ""
echo "🔋 Batterie :"
termux-battery-status

echo ""
echo "📱 Toutes les apps installées :"
pm list packages

echo ""
echo "👀 Processus suspects :"
ps aux | grep -i "crypto\|miner\|tor\|root"

echo ""
echo "🌐 Ports ouverts :"
netstat -tuln
