import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

ADMIN_ID = 1299831974
served_users_file = "users_served.json"
if os.path.exists(served_users_file):
    with open(served_users_file, "r") as f:
        served_users = json.load(f)
else:
    served_users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or user.username
    text = f"👋 Bonjour {name} !\n\nBienvenue sur 🛒 Deku Shop – ton centre de services anime & tech !\n\n"
    text += "📦 Voici ce que je propose :\n"
    text += "1️⃣ Crunchyroll Premium – Anime en illimité VF/VOSTFR\n"
    text += "2️⃣ VPN AfricaSurf – Surf gratuit dans 7 pays d’Afrique\n"
    text += "3️⃣ VPS Blackoft – Gère toi-même ton système VPN privé\n\n"
    text += "🛍️ Clique sur un bouton ci-dessous pour commencer 👇"

    keyboard = [
        [InlineKeyboardButton("🎬 Crunchyroll", callback_data='crunchyroll')],
        [InlineKeyboardButton("🌍 VPN AfricaSurf", callback_data='vpn')],
        [InlineKeyboardButton("🖥️ VPS Blackoft", callback_data='vps')],
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "crunchyroll":
        await query.edit_message_text(
            "🎬 Crunchyroll Premium\n\n📜 Tarifs :\n1 mois : 1500 FCFA\n2 mois : 3000 FCFA\n3 mois : 5000 FCFA\n6 mois : 10000 FCFA\n1 an : 20000 FCFA\n\n✅ Compte personnel, sans pub\n💬 Pour commander :\nTelegram: @Deku225\nWhatsApp: +2250575719113"
        )

    elif query.data == "vpn":
        keyboard = [
            [InlineKeyboardButton("📲 Acheter un compte", callback_data='acheter_vpn')],
            [InlineKeyboardButton("🧪 Obtenir un compte test", callback_data='test_vpn')],
        ]
        await query.edit_message_text("🌍 VPN AfricaSurf – Choisis une option :", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "acheter_vpn":
        await query.edit_message_text("📞 Pour commander :\nTelegram : @Deku225\nWhatsApp : +2250575719113")

    elif query.data == "test_vpn":
        user_id = str(query.from_user.id)
        if user_id in served_users:
            await query.edit_message_text("🧪 Tu as déjà reçu un compte test AfricaSurf.")
            return
        try:
            with open("comptes_test_africasurf.txt", "r") as f:
                lines = f.readlines()
            if not lines:
                await query.edit_message_text("❌ Tous les comptes test ont été utilisés.")
                return
            compte = lines.pop(0).strip()
            served_users[user_id] = compte
            with open(served_users_file, "w") as f:
                json.dump(served_users, f)
            with open("comptes_test_africasurf.txt", "w") as f:
                f.writelines(lines)
            await query.edit_message_text(f"🧪 Voici ton compte test AfricaSurf :\n`{compte}`", parse_mode="Markdown")

            if len(lines) < 3:
                await context.bot.send_message(chat_id=ADMIN_ID,
                    text=f"⚠️ Alerte stock ! Il ne reste plus que {len(lines)} comptes tests AfricaSurf.")
        except Exception as e:
            await query.edit_message_text("❌ Erreur lors de la distribution du compte test.")

    elif query.data == "vps":
        await query.edit_message_text(
            "🖥️ VPS – Blackoft Hosting\n\n🔥 Tu veux ton propre Free Surf ?\n💻 Crée ton système VPN toi-même (V2Ray, Xray, SlowDNS, etc.)\n\n🌐 Compatible avec :\nMTN CI, Moov, Orange, Vodacom, etc.\n\n💸 Tarifs :\n• 8500 FCFA (config + VPS)\n• 5500 FCFA / mois\n\n📞 Pour commander :\nTelegram : @Deku225\nWhatsApp : +2250575719113"
        )

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_button))
app.run_polling()
