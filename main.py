import os
import datetime
import mongoengine as me
from models import Event
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Environment variables
TOKEN = os.environ['TELEGRAM_TOKEN']

################
# Bot commands #
################


def start(bot, update):
    """Simple start command to introduce the bot functionality"""
    update.message.reply_text('Hey! Type /agenda to check for nearby events')


def unknown(bot, update):
    """Executed when command is not implemented"""
    update.message.reply_text("Sorry, I didn't understand that command.")


def agenda(bot, update):
    """Implementation of the agenda command"""
    update.message.reply_text("Not implemented")

def add_event(bot, update, args):
    """Implementation of the addevent command"""
    update.message.reply_text("Not implemented")
    

# Connects to the mongo database (localhost by default)
me.connect()

# Gets the bot updater and dispatcher
updater = Updater(TOKEN)
dp = updater.dispatcher

# Main commands
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('agenda', agenda))
dp.add_handler(CommandHandler('addevent', add_event))

# Not implemented commands
dp.add_handler(MessageHandler(Filters.command, unknown))

# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()
