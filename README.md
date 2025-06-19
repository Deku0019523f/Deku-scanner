# 📱 Deku-Scanner

> Un scanner de téléphone Android basé sur Termux avec interface Web, avec ou sans accès root.

![Logo](logo.png)

## 🚀 Fonctionnalités
- Analyse du stockage, RAM, batterie
- Liste des applications installées
- Détection de processus suspects (root)
- Analyse réseau : ports ouverts, connexions actives
- Interface Web en local avec deux choix : rooté / non-rooté

---

## 📥 Installation automatique (Termux)

```bash
pkg update && pkg install git -y
git clone https://github.com/Deku0019523f/Deku-scanner.git
cd Deku-scanner
bash install.sh
```

---

## ▶️ Lancer le scanner

```bash
python server.py
```

Puis ouvre ton navigateur sur :  
**http://localhost:8000**

---

## 📄 Licence

MIT – libre d’usage, modification et distribution.
