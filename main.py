import telebot
import openai
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.first_name or message.chat.username
    welcome_text = f"👋 Bonjour {username} !\n\n"
    welcome_text += "Je suis un bot qui génère du code automatiquement.\n"
    welcome_text += "Envoie-moi une demande comme :\n"
    welcome_text += "➡️ Crée un bot Telegram qui répond ‘Bonjour’\n"
    welcome_text += "➡️ Génère une page HTML simple pour un portfolio\n"
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def generate_code(message):
    try:
        prompt = f"Génère ce code : {message.text}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        generated_code = response['choices'][0]['message']['content']
        bot.reply_to(message, generated_code)
    except Exception as e:
        bot.reply_to(message, "❌ Une erreur est survenue. Vérifie les clés API.")

bot.polling()
