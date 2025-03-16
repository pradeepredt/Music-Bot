from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import yt_dlp
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("TOKEN")
FFMPEG_PATH = os.getenv("FFMPEG_PATH")

# Write the cookies from environment variable to a file
cookies_content = os.getenv("YOUTUBE_COOKIES")
if cookies_content:
    with open("cookies.txt", "w") as file:
        file.write(cookies_content)
        
# Start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send me a YouTube link to download as MP3.")

# Handles MP3 download process
async def download_mp3(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    chat_id = update.message.chat_id
    
    await update.message.reply_text("Downloading MP3... Please wait.")
    
    # Download options for yt-dlp
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
        "ffmpeg_location": FFMPEG_PATH,
        "cookiefile": "cookies.txt"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace(info["ext"], "mp3")

        # Send the file to the user
        with open(filename, "rb") as file:
            await context.bot.send_audio(chat_id=chat_id, audio=file)

        os.remove(filename)  # Delete file after sending
        await update.message.reply_text("MP3 download complete.")

    except Exception as e:
        await update.message.reply_text(f"Download failed: {str(e)}")

# Main function to run the bot
def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_mp3))
    
    print("Bot is running...")
    application.run_polling()

# Run the bot
if __name__ == "__main__":
    main()
