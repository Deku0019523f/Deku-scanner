# 📱 Analyse Téléphone Android (Termux + Web UI)

Ce projet permet de lancer une analyse de votre téléphone Android directement via **Termux**, avec une interface **web simple** accessible depuis le navigateur local.

## ⚙️ Fonctionnalités
- 📦 Vérification du stockage
- 🔋 Batterie
- 🧠 Utilisation de la RAM
- 📱 Liste des apps installées
- 🌐 Connexions réseau et ports ouverts
- 🔐 Analyse avec ou sans root

## ▶️ Lancer le projet

1. Installez les dépendances dans Termux :
```bash
pkg install python termux-api net-tools tsu -y
chmod +x scan_*.sh
python server.py
```

2. Ouvrez le navigateur sur :
```
http://localhost:8000
```

## 🧭 Interface
Deux boutons vous permettent de choisir le type d’analyse :

- **Analyse avec Root** 🔐
- **Analyse sans Root** 🔓

## 🖼️ Ajouter un logo

Ajoutez une image `logo.png` dans le dossier et modifiez `index.html` pour l’inclure :

```html
<img src="logo.png" width="100"/>
```

---

## 📄 Licence

Distribué sous licence MIT. Voir `LICENSE` pour plus de détails.
