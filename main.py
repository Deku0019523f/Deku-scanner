import os
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

ADMIN_ID = 1299831974
served_users_file = "users_served.json"
test_file = "comptes_test_africasurf.txt"
log_file = "logs.txt"

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

# 🚀 Menu principal
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or user.username
    log_action(user, "/start")

    text = f"👋 Bonjour {name} !\n\nBienvenue sur 🛒 Deku Shop – ton centre de services anime & tech !\n\n"
    text += "📦 Voici ce que je propose :\n"
    text += "1️⃣ Crunchyroll Premium – Anime en illimité VF/VOSTFR\n"
    text += "2️⃣ VPN AfricaSurf – Surf gratuit dans 10+ pays\n"
    text += "3️⃣ VPS Blackoft – Crée ton système VPN pro\n\n"
    text += "🛍️ Clique sur un bouton ci-dessous 👇"

    keyboard = [
        [InlineKeyboardButton("🎬 Crunchyroll", callback_data='crunchyroll')],
        [InlineKeyboardButton("🌍 VPN AfricaSurf", callback_data='vpn')],
        [InlineKeyboardButton("🖥️ VPS Blackoft", callback_data='vps')],
        [InlineKeyboardButton("🆘 Support", callback_data='support')],
    ]

    # Bouton /stock visible seulement pour l’admin
    if is_admin(user.id):
        keyboard.append([InlineKeyboardButton("📦 Voir le stock", callback_data='stock')])

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# 🆘 Commande /support
async def support_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_action(update.effective_user, "/support")
    await update.message.reply_text("📞 Support client :\nTelegram : @Deku225\nWhatsApp : +2250575719113")

# 📦 Commande /stock
async def stock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔ Tu n'es pas autorisé à voir ce stock.")
        return
    with open(test_file, "r") as f:
        lignes = f.readlines()
    total_served = len(served_users)
    await update.message.reply_text(f"📊 Stock restant : {len(lignes)} comptes tests\n👤 Utilisateurs servis : {total_served}")

# 🧠 Gestion des boutons
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    log_action(user, f"Click → {query.data}")

    if query.data == "crunchyroll":
        keyboard = [[InlineKeyboardButton("🔙 Retour", callback_data="retour")]]
        await query.edit_message_text(
            "🎬 Crunchyroll Premium\n\n📜 Tarifs :\n1 mois : 1500 FCFA\n2 mois : 3000 FCFA\n3 mois : 5000 FCFA\n6 mois : 10000 FCFA\n1 an : 20000 FCFA\n\n✅ Compte personnel\n💬 Pour commander : @Deku225 / WhatsApp : +2250575719113",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "vpn":
        keyboard = [
            [InlineKeyboardButton("📲 Acheter un compte", callback_data='acheter_vpn')],
            [InlineKeyboardButton("🧪 Obtenir un compte test", callback_data='test_vpn')],
            [InlineKeyboardButton("🔙 Retour", callback_data="retour")]
        ]
        await query.edit_message_text("🌍 VPN AfricaSurf – Choisis une option :", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "acheter_vpn":
        keyboard = [[InlineKeyboardButton("🔙 Retour", callback_data="vpn")]]
        await query.edit_message_text("📞 Pour commander : @Deku225 / WhatsApp : +2250575719113", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "test_vpn":
        user_id = str(user.id)
        if user_id in served_users:
            await query.edit_message_text("🧪 Tu as déjà reçu un compte test AfricaSurf.")
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
            await query.edit_message_text(f"🧪 Ton compte test AfricaSurf :\n`{compte}`", parse_mode="Markdown")

            if len(lines) < 3:
                await context.bot.send_message(chat_id=ADMIN_ID,
                    text=f"⚠️ Alerte stock ! Il ne reste que {len(lines)} comptes tests AfricaSurf.")
        except Exception:
            await query.edit_message_text("❌ Erreur lors de la distribution du compte test.")

    elif query.data == "vps":
        keyboard = [[InlineKeyboardButton("🔙 Retour", callback_data="retour")]]
        await query.edit_message_text(
            "🖥️ VPS – Blackoft Hosting\n\n🔥 Crée ton propre Free Surf !\n💻 Installe V2Ray, Xray, SlowDNS, UDP, SSH, etc.\n\n✅ Compatible avec :\n- MTN CM\n- MTN CI (Microsoft / Illimité)\n- MOOV Burkina / Niger / Togo\n- MTN Bénin\n- CAMTEL Cameroun\n- VODACOM RDC\n- MOOV CI\n- Orange Burkina\n- Orange CI (Packs Social)\n- CELTIS BÉNIN\n\n💸 Prix :\n• 8500F (config + VPS)\n• 5500F/mois VPS\n\n📞 Contact : @Deku225 / WhatsApp : +2250575719113",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "support":
        keyboard = [[InlineKeyboardButton("🔙 Retour", callback_data="retour")]]
        await query.edit_message_text("📞 Support : @Deku225 / WhatsApp : +2250575719113", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "stock" and is_admin(user.id):
        with open(test_file, "r") as f:
            lignes = f.readlines()
        total_served = len(served_users)
        keyboard = [[InlineKeyboardButton("🔙 Retour", callback_data="retour")]]
        await query.edit_message_text(
            f"📊 Stock restant : {len(lignes)} comptes tests\n👤 Utilisateurs servis : {total_served}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "retour":
        # Simule un /start
        return await start(update, context)

# ▶️ Lancement
app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("support", support_cmd))
app.add_handler(CommandHandler("stock", stock_cmd))
app.add_handler(CallbackQueryHandler(handle_button))
app.run_polling()
