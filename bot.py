import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pytube import YouTube, Playlist

# YouTube videoni yuklash funksiyasi
def download_video(url, chat_id, bot):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        filename = video.download()
        
        # Videoni foydalanuvchiga yuborish
        bot.send_video(chat_id=chat_id, video=open(filename, 'rb'))
        os.remove(filename)  # Yuklangan videoni o'chirish
    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f"Xatolik: {str(e)}")

# Playlistni yuklash funksiyasi
def download_playlist(url, chat_id, bot):
    try:
        playlist = Playlist(url)
        for video_url in playlist.video_urls:
            download_video(video_url, chat_id, bot)
    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f"Xatolik: {str(e)}")

# /start buyrug'ini qayta ishlash
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Salom! Menga YouTube havolasini yuboring.")

# URLni qayta ishlash
def handle_message(update: Update, context: CallbackContext):
    url = update.message.text
    chat_id = update.message.chat_id
    bot = context.bot

    if "playlist" in url.lower():
        bot.send_message(chat_id=chat_id, text="Playlist yuklanmoqda. Iltimos kuting...")
        download_playlist(url, chat_id, bot)
    else:
        bot.send_message(chat_id=chat_id, text="Video yuklanmoqda. Iltimos kuting...")
        download_video(url, chat_id, bot)

# Botni ishga tushirish
def main():
    TOKEN = "8072140256:AAGJP8_1wlMwUKQpJkXMm8PoSGzNOQnRSSo"
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
