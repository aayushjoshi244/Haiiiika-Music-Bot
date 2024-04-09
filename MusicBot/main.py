import logging
from telegram.ext import Updater, CommandHandler
import youtube_dl

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Token for accessing the Telegram Bot API
TOKEN = '6432407505:AAEZyUN3TSyYmfFhflWfdgd1tyBFr9fM3k0'


# Function to handle the /start command
def start(update, context):
    update.message.reply_text('Welcome to MusicBot! Send /play <YouTube URL> to start streaming music.')


# Function to handle the /play command
def play(update, context):
    # Get the YouTube URL from the user's message
    url = context.args[0]

    # Download audio from YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        filename = ydl.prepare_filename(info)
        title = info['title']

    # Start a voice call with the user
    context.bot.send_message(chat_id=update.message.chat_id, text=f'Streaming {title}...')
    context.bot.send_voice(chat_id=update.message.chat_id, voice=open(filename, 'rb'))


# Main function
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    start_handler = CommandHandler('start', start)
    play_handler = CommandHandler('play', play)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(play_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
