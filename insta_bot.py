import requests
import re
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Paste your Telegram bot token here
TELEGRAM_TOKEN = "8286656584:AAH0t5BP6kXB3TtQZB-KzhP5oqILnDps4Vc"

# Paste your Instagram sessionid here
SESSION_ID = "45664980228%3AALbNp6y6waA5gZ%3A16%3AAYcHC2_F0KD3o8kcXKAdTJvPR_Fc2c7d9bg3SrCVMw"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Cookie": f"sessionid={SESSION_ID};",
}

def extract_video_url(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            match = re.search(r'"video_url":"(.*?)"', response.text)
            if match:
                return match.group(1).replace("\\u0026", "&")
    except requests.exceptions.RequestException:
        return None
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me an Instagram Reel URL and I will fetch the video.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com/reel/" not in url:
        await update.message.reply_text("Please send a valid Instagram Reel URL.")
        return

    await update.message.reply_text("Fetching video... Please wait.")
    time.sleep(2)  # Basic rate limiting

    video_url = extract_video_url(url)
    if video_url:
        try:
            await update.message.reply_video(video_url)
        except:
            await update.message.reply_text("Video too large for Telegram to send directly.")
    else:
        await update.message.reply_text("Failed to fetch video. Session may be invalid or post is private.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
