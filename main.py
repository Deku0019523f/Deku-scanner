import os
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURATION ---
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
LOG_FILE = "logs.txt"

# --- UTILS ---
def is_admin(uid):
    return uid == ADMIN_ID

def log_action(user, action):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {user.id} ({user.username}) → {action}\n")

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f)

def load_products():
    if os.path.exists(PRODUITS_FILE):
        with open(PRODUITS_FILE, "r") as f:
            return json.load(f)
    return []

def save_products(data):
    with open(PRODUITS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_test_account():
    if not os.path.exists(TEST_FILE): return None
    with open(TEST_FILE, "r") as f:
        lines = f.readlines()
    if not lines: return None
    account = lines[0].strip()
    with open(TEST_FILE, "w") as f:
        f.writelines(lines[1:])
    return account

def remaining_test_accounts():
    if not os.path.exists(TEST_FILE): return 0
    with open(TEST_FILE, "r") as f:
        return len(f.readlines())

# --- COMMANDES ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    produits = load_products()
    buttons = [[InlineKeyboardButton(p['nom'], callback_data=f"produit_{p['nom']}")] for p in produits]
    buttons.append([InlineKeyboardButton("🆘 Support", callback_data="support")])
    if is_admin(user.id):
        buttons.append([InlineKeyboardButton("📦 Voir les utilisateurs", callback_data="admin_users")])
    await update.message.reply_text(
        f"👋 Bonjour {user.first_name} !\nBienvenue sur Deku Shop.\nChoisis un service 👇",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    log_action(user, "/start")

async def addtest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    compte = " ".join(context.args).strip()
    if not compte: return await update.message.reply_text("❌ Utilise : /addtest email:mdp")
    with open(TEST_FILE, "a") as f:
        f.write(compte + "\n")
    await update.message.reply_text("✅ Compte ajouté.")

async def addproduct(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    data = " ".join(context.args).split("|")
    if len(data) != 4:
        return await update.message.reply_text("❌ Format : /addproduct nom | description | prix | image_url")
    nom, description, prix, image = [d.strip() for d in data]
    produits = load_products()
    produits.append({"nom": nom, "description": description, "prix": prix, "image": image})
    save_products(produits)
    await update.message.reply_text(f"✅ Produit {nom} ajouté.")

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    data = load_users()
    text = f"👤 Utilisateurs : {len(data)}\n\n"
    for uid, val in data.items():
        text += f"{uid} : {val}\n"
    await update.message.reply_text(text)

# --- CALLBACKS ---
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user = query.from_user
    await query.answer()
    log_action(user, f"Click → {data}")

    if data.startswith("produit_"):
        nom = data.split("_", 1)[1]
        produits = load_products()
        produit = next((p for p in produits if p["nom"] == nom), None)
        if not produit: return
        buttons = [[InlineKeyboardButton("🛒 Acheter un compte", url="https://t.me/Deku225")]]
        if nom.lower() == "africasurf vpn":
            buttons.append([InlineKeyboardButton("🧪 Compte test", callback_data="test_account")])
        buttons.append([InlineKeyboardButton("🔙 Retour", callback_data="retour")])
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=produit["image"],
            caption=f"🛍️ {produit['nom']}\n\n{produit['description']}\n💰 {produit['prix']}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "test_account":
        users = load_users()
        if str(user.id) in users:
            await query.edit_message_text("⚠️ Tu as déjà reçu un compte test.")
            return
        account = get_test_account()
        if not account:
            await query.edit_message_text("❌ Stock de comptes test épuisé.")
            return
        users[str(user.id)] = account
        save_users(users)
        await context.bot.send_message(user.id, f"🧪 Ton compte test :\n`{account}`", parse_mode="Markdown")
        if remaining_test_accounts() < 3:
            await context.bot.send_message(ADMIN_ID, "🚨 Il reste moins de 3 comptes test AfricaSurf.")
        await context.bot.send_message(user.id, "📥 Voici comment utiliser le compte :")
        await context.bot.send_message(user.id, f"🔗 Télécharger l’APK : {APK_LINK}")
        for url in IMG["tuto"]:
            await context.bot.send_photo(chat_id=user.id, photo=url)

    elif data == "support":
        await query.edit_message_text("📞 Contacte @Deku225 / WhatsApp : +2250575719113",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Retour", callback_data="retour")]]))

    elif data == "admin_users":
        await users(update, context)

    elif data == "retour":
        await start(update, context)

# --- LANCEMENT POLLING ---
if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addtest", addtest))
    app.add_handler(CommandHandler("addproduct", addproduct))
    app.add_handler(CommandHandler("users", users))
    app.add_handler(CallbackQueryHandler(handle_button))
    print("✅ Bot lancé en mode polling...")
    app.run_polling()
