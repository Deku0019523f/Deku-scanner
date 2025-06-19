#!/data/data/com.termux/files/usr/bin/bash
echo "🔎 Analyse sans Root"
echo "📦 Stockage :"
df -h /data | grep -v Filesystem

echo ""
echo "🧠 RAM :"
free -h

echo ""
echo "🔋 Batterie :"
termux-battery-status

echo ""
echo "📱 Applications installées :"
pm list packages | head -n 10

echo ""
echo "🌐 Connexions réseau actives :"
netstat -antp | grep ESTABLISHED
