import telebot
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mixtral-8x7b"  # Modèle gratuit et puissant

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
            bot.reply_to(message, f"❌ Erreur OpenRouter {response.status_code} : {response.text}")

    except Exception as e:
        bot.reply_to(message, f"❌ Erreur côté bot : {str(e)}")

bot.polling()
