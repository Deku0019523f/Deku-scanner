import telebot
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openai/gpt-3.5-turbo"  # Tu peux aussi tester "mistralai/mixtral-8x7b"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.first_name or message.chat.username
    welcome_text = f"👋 Bonjour {username} !\n\n"
    welcome_text += "Je suis un bot qui génère du code automatiquement.\n"
    welcome_text += "Envoie-moi une demande comme :\n"
    welcome_text += "➡️ Crée un bot Telegram qui répond ‘Bonjour’\n"
    welcome_text += "➡️ Génère une page HTML simple pour un portfolio"
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def generate_code(message):
    try:
        prompt = message.text
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://t.me/IA_Deku_Bot",  # Personnalise si tu veux
            "X-Title": "CodeGenerator"
        }

        data = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": f"Génère ce code : {prompt}"}
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            bot.reply_to(message, content)
        else:
            bot.reply_to(message, "❌ Une erreur est survenue avec OpenRouter.")
            print("Erreur OpenRouter:", response.text)

    except Exception as e:
        print("Erreur Python:", e)
        bot.reply_to(message, "❌ Une erreur est survenue. Vérifie ta clé OpenRouter.")

bot.polling()
