import os
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

ADMIN_ID = 1299831974
served_users_file = "users_served.json"
test_file = "comptes_test_africasurf.txt"
log_file = "logs.txt"

# 🔁 URLs des images hébergées sur GitHub
IMG = {
    "crunchy": "https://raw.githubusercontent.com/Deku0019523f/Deku-scanner/main/images/Crunch.png",
    "vpn": "https://raw.githubusercontent.com/Deku0019523f/Deku-scanner/main/images/Africa.png",
    "vps": "https://raw.githubusercontent.com/Deku0019523f/Deku-scanner/main/images/VPS.png",
    "tuto": [
        "https://raw.githubusercontent.com/TON_USER/Deku0019523f/Deku-scanner/images/tuto1.png",
        "https://raw.githubusercontent.com/Deku0019523f/Deku-scanner/main/images/tuto2.png",
        "https://raw.githubusercontent.com/Deku0019523f/Deku-scanner/main/images/tuto3.png"
    ]
}

APK_LINK = "https://t.me/connexiontoutreseaus/4825"

if os.path.exists(served_users_file):
    with open(served_users_file, "r") as f:
        served_users = json.load(f)
else:
    served_users = {}

def is_admin(user_id):
    return user_id == ADMIN_ID

def log_action(user, action):
    with open(log_file, "a") as log:
        log.write(f"[{datetime.now()}] {user.username or user.id} → {action}\n")

async def send_main_menu(user, context, chat_id):
    name = user.first_name or user.username
    text = f"👋 Bonjour {name} !\n\nBienvenue sur 🛒 Deku Shop – ton centre de services anime & tech !\n\n"
    text += "📦 Voici ce que je propose :\n"
    text += "1️⃣ Crunchyroll Premium – Anime en illimité VF/VOSTFR\n"
    text += "2️⃣ VPN AfricaSurf – Surf gratuit dans +10 pays d’Afrique\n"
    text += "3️⃣ VPS Blackoft – Crée ton système VPN personnel\n\n"
    text += "🛍️ Clique sur un bouton ci-dessous 👇"

    keyboard = [
        [InlineKeyboardButton("🎬 Crunchyroll", callback_data='crunchyroll')],
        [InlineKeyboardButton("🌍 VPN AfricaSurf", callback_data='vpn')],
        [InlineKeyboardButton("🖥️ VPS Blackoft", callback_data='vps')],
        [InlineKeyboardButton("🆘 Support", callback_data='support')],
    ]
    if is_admin(user.id):
        keyboard.append([InlineKeyboardButton("📦 Voir le stock", callback_data='stock')])

    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(keyboard))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    log_action(user, "/start")
    await send_main_menu(user, context, update.effective_chat.id)

async def support_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_action(update.effective_user, "/support")
    await update.message.reply_text("📞 Support : @Deku225 / WhatsApp : +2250575719113")

async def stock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔ Tu n'es pas autorisé à voir ce stock.")
        return
    with open(test_file, "r") as f:
        lines = f.readlines()
    await update.message.reply_text(f"📦 Stock restant : {len(lines)} comptes tests\n👤 Utilisateurs servis : {len(served_users)}")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    data = query.data
    await query.answer()
    log_action(user, f"Click → {data}")

    if data == "crunchyroll":
        await context.bot.send_photo(chat_id=query.message.chat_id, photo=IMG["crunchy"],
            caption="🎬 Crunchyroll Premium\n\n📜 Tarifs :\n1 mois : 1500 FCFA\n2 mois : 3000 FCFA\n3 mois : 5000 FCFA\n6 mois : 10000 FCFA\n1 an : 20000 FCFA\n\n✅ Compte personnel\n💬 Contact : @Deku225 / WhatsApp : +2250575719113",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Retour", callback_data="retour")]]))

    elif data == "vpn":
        keyboard = [
            [InlineKeyboardButton("📲 Acheter un compte", callback_data='acheter_vpn')],
            [InlineKeyboardButton("🧪 Obtenir un compte test", callback_data='test_vpn')],
            [InlineKeyboardButton("❓ Comment utiliser le compte", callback_data='tuto_vpn')],
            [InlineKeyboardButton("🔙 Retour", callback_data="retour")]
        ]
        await context.bot.send_photo(chat_id=query.message.chat_id, photo=IMG["vpn"],
            caption="🌍 VPN AfricaSurf – Compatible avec :\n- MTN CM\n- MTN CI (Microsoft / illimité)\n- MOOV Burkina / Niger / Togo\n- MTN Bénin\n- CAMTEL Cameroun\n- VODACOM RDC\n- MOOV CI\n- Orange Burkina\n- Orange CI (Social)\n- CELTIS BÉNIN",
            reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "acheter_vpn":
        await query.edit_message_text("📞 Pour commander : @Deku225 / WhatsApp : +2250575719113",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Retour", callback_data="vpn")]]))

    elif data == "test_vpn":
        user_id = str(user.id)
        if user_id in served_users:
            await query.edit_message_text("🧪 Tu as déjà reçu un compte test.")
            return
        try:
            with open(test_file, "r") as f:
                lines = f.readlines()
            if not lines:
                await query.edit_message_text("❌ Tous les comptes test ont été utilisés.")
                return
            compte = lines.pop(0).strip()
            served_users[user_id] = compte
            with open(served_users_file, "w") as f:
                json.dump(served_users, f)
            with open(test_file, "w") as f:
                f.writelines(lines)
            await query.edit_message_text(f"🧪 Ton compte test :\n`{compte}`", parse_mode="Markdown")
            if len(lines) < 3:
                await context.bot.send_message(ADMIN_ID, f"⚠️ Alerte : il reste {len(lines)} comptes tests.")
        except Exception:
            await query.edit_message_text("❌ Erreur lors de la distribution du compte test.")

    elif data == "tuto_vpn":
        media = [InputMediaPhoto(media=url) for url in IMG["tuto"]]
        await context.bot.send_media_group(chat_id=query.message.chat_id, media=media)
        await context.bot.send_message(chat_id=query.message.chat_id,
            text=f"📥 Télécharge l'APK ici : [Lien APK]({APK_LINK})",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Retour", callback_data="vpn")]]))

    elif data == "vps":
        await context.bot.send_photo(chat_id=query.message.chat_id, photo=IMG["vps"],
            caption="🖥️ VPS – Blackoft Hosting\n\n🔥 Gère ton propre VPN (V2Ray, SlowDNS...)\n\n📶 Compatible :\n- MTN CI, MOOV, CAMTEL, VODACOM, Orange, etc.\n\n💸 Prix :\n• 8500F (config + VPS)\n• 5500F / mois\n\n📞 @Deku225 / WhatsApp : +2250575719113",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Retour", callback_data="retour")]]))

    elif data == "support":
        await query.edit_message_text("📞 Support : @Deku225 / WhatsApp : +2250575719113",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Retour", callback_data="retour")]]))

    elif data == "stock" and is_admin(user.id):
        with open(test_file, "r") as f:
            lines = f.readlines()
        await query.edit_message_text(f"📦 Stock : {len(lines)} comptes\n👤 Utilisateurs servis : {len(served_users)}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Retour", callback_data="retour")]]))

    elif data == "retour":
        await query.delete_message()
        await send_main_menu(user, context, query.message.chat_id)

# ▶️ Lancement
app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("support", support_cmd))
app.add_handler(CommandHandler("stock", stock_cmd))
app.add_handler(CallbackQueryHandler(handle_button))
app.run_polling()
