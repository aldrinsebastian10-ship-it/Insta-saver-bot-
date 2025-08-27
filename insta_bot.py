import os
import telebot
import instaloader

# Telegram bot token from BotFather
BOT_TOKEN = os.getenv("8286656584:AAH0t5BP6kXB3TtQZB-KzhP5oqILnDps4Vc", "8286656584:AAH0t5BP6kXB3TtQZB-KzhP5oqILnDps4Vc")
bot = telebot.TeleBot(8286656584:AAH0t5BP6kXB3TtQZB-KzhP5oqILnDps4Vc)

# Instagram loader
loader = instaloader.Instaloader()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Hi! Send me any public Instagram post/reel/story link and I’ll download it for you.")

@bot.message_handler(func=lambda msg: True)
def download_instagram(message):
    url = message.text.strip()

    if "instagram.com" not in url:
        bot.reply_to(message, "⚠️ Please send me a valid Instagram link.")
        return

    try:
        post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
        filename = f"{post.shortcode}.jpg"

        loader.download_post(post, target="downloads")
        filepath = os.path.join("downloads", filename)

        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                bot.send_photo(message.chat.id, f)
        else:
            bot.reply_to(message, "❌ Couldn’t fetch the media.")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")

bot.polling()
