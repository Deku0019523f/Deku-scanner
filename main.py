import os
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuration
ADMIN_ID = 1299831974
BOT_TOKEN = os.getenv("BOT_TOKEN")

IMG = {
    "crunchy": "https://raw.githubusercontent.com/Deku0019523f/Deku-scanner/main/images/Crunch.png",
    "vpn": "https://raw.githubusercontent.com/Deku0019523f/Deku-scanner/main/images/Africa.png",
    "vps": "https://raw.githubusercontent.com/Deku0019523f/Deku-scanner/main/images/VPS.png",
    "tuto": [
        "https://raw.githubusercontent.com/Deku0019523f/Deku-scanner/main/images/tuto1.png",
        "https://raw.githubusercontent.com/Deku0019523f/Deku-scanner/main/images/tuto2.png",
        "https://raw.githubusercontent.com/Deku0019523f/Deku-scanner/main/images/tuto3.png"
    ]
}

APK_LINK = "https://t.me/connexiontoutreseaus/4825"
TEST_FILE = "comptes_test_africasurf.txt"
USERS_FILE = "users_served.json"
PRODUITS_FILE = "produits.json"

# Fonctions utilitaires
def is_admin(uid):
    return uid == ADMIN_ID

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f)

def get_test_account():
    if not os.path.exists(TEST_FILE): return None
    with open(TEST_FILE, "r") as f:
        lines = f.readlines()
    if not lines: return None
    compte = lines[0].strip()
    with open(TEST_FILE, "w") as f:
        f.writelines(lines[1:])
    return compte

def remaining_test_accounts():
    if not os.path.exists(TEST_FILE): return 0
    with open(TEST_FILE, "r") as f:
        return len(f.readlines())

def load_products():
    if os.path.exists(PRODUITS_FILE):
        with open(PRODUITS_FILE, "r") as f:
            return json.load(f)
    return []

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    produits = load_products()
    boutons = [[InlineKeyboardButton(p['nom'], callback_data=f"produit_{p['nom']}")] for p in produits]
    boutons.append([InlineKeyboardButton("🆘 Support", callback_data="support")])
    if is_admin(user.id):
        boutons.append([InlineKeyboardButton("📦 Voir utilisateurs", callback_data="admin_users")])
    texte = (
        f"👋 Bonjour {user.first_name} !\n\n"
        "Bienvenue sur *Deku225-Shop* 🛍️ !\n\n"
        "Je propose des comptes VPN, Crunchyroll et VPS Free Surf à petits prix !\n\n"
        "Clique sur l’un des produits ci-dessous pour voir les détails 👇"
    )
    await update.message.reply_text(texte, reply_markup=InlineKeyboardMarkup(boutons), parse_mode="Markdown")

# Gestion des boutons
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()
    data = query.data
    produits = load_products()

    if data.startswith("produit_"):
        nom = data.split("_", 1)[1]
        produit = next((p for p in produits if p["nom"] == nom), None)
        if not produit: return

        buttons = [[InlineKeyboardButton("🛒 Acheter un compte", url="https://t.me/Deku225")]]

        if nom.lower() == "africasurf vpn":
            buttons.append([InlineKeyboardButton("🧪 Compte test", callback_data="test_account")])

        buttons.append([InlineKeyboardButton("🔙 Retour", callback_data="retour")])

        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=produit["image"],
            caption=f"📌 *{produit['nom']}*\n\n{produit['description']}\n💰 *{produit['prix']}*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "test_account":
        users = load_users()
        if str(user.id) in users:
            await context.bot.send_message(user.id, "⚠️ Tu as déjà reçu un compte test.")
            return

        compte = get_test_account()
        if not compte:
            await context.bot.send_message(user.id, "❌ Plus de comptes test disponibles.")
            return

        users[str(user.id)] = compte
        save_users(users)

        await context.bot.send_message(user.id, f"✅ Ton compte test :\n`{compte}`", parse_mode="Markdown")

        if remaining_test_accounts() < 3:
            await context.bot.send_message(ADMIN_ID, "🚨 Attention ! Il reste moins de 3 comptes test disponibles.")

        await context.bot.send_message(user.id, f"📥 *Voici comment utiliser le compte :*", parse_mode="Markdown")
        await context.bot.send_message(user.id, f"🔗 Télécharger l'APK : {APK_LINK}")
        for url in IMG["tuto"]:
            await context.bot.send_photo(chat_id=user.id, photo=url)

    elif data == "support":
        await query.edit_message_text(
            "📞 Contact : @Deku225\n📱 WhatsApp : +225 0575719113",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Retour", callback_data="retour")]])
        )

    elif data == "admin_users":
        users = load_users()
        message = f"👤 Utilisateurs : {len(users)}\n\n"
        for uid, val in users.items():
            message += f"{uid} → {val}\n"
        await context.bot.send_message(ADMIN_ID, message)

    elif data == "retour":
        await start(update, context)

# Lancement
if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    print("✅ BOT LANCÉ (polling)")
    app.run_polling()
