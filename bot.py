import os
import re
import mega
import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from mega import Mega

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
MEGA_EMAIL = ''
MEGA_PASSWORD = ''

# Define a few command handlers. These usually take the two arguments update and context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
    update.message.reply_text('Please provide your MEGA email and password in the format: email,password')


def rename_files(update: Update, context: CallbackContext) -> None:
    """Rename files in MEGA account."""
    global MEGA_EMAIL, MEGA_PASSWORD
    msg = update.message.text
    if ',' not in msg:
        update.message.reply_text('Please provide credentials in the correct format: email,password')
        return

    MEGA_EMAIL, MEGA_PASSWORD = map(str.strip, msg.split(','))

    try:
        mega = Mega()
        m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)
        files = m.get_files()
        counter = 1
        for file_id in files:
            file = files[file_id]
            file_name = file['a']['n']
            file_ext = os.path.splitext(file_name)[1]
            new_name = f'file_{counter}{file_ext}'
            m.rename(file_id, new_name)
            counter += 1
        update.message.reply_text('All files have been renamed successfully.')
    except Exception as e:
        update.message.reply_text(f'An error occurred: {str(e)}')


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.getenv("TELEGRAM_BOT_TOKEN"))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    # on non command i.e message - rename files
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, rename_files))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT.
    updater.idle()


if __name__ == '__main__':
    main()
