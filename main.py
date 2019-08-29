import os
import mongoengine as me
from utils import collection_to_string, parse_event_args
from models import Event
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Environment variables
TOKEN = os.environ['TELEGRAM_TOKEN']

################
# Bot commands #
################


def start(bot, update):
    """
    Simple start command to introduce the bot functionality
    """
    update.message.reply_text('Hey! Type /agenda to check for events')


def unknown(bot, update):
    """
    Executed when command is not implemented
    """
    update.message.reply_text("Sorry, I didn't understand that command.")


def agenda(bot, update):
    """
    Displays all the events in the agenda
    """
    # Gets all the documents in the Events collection
    events = Event.objects
    if len(events) > 0:
        message = collection_to_string(events)
        update.message.reply_text(message)
    else:
        update.message.reply_text('The agenda is empty')


def event(bot, update, args):
    """
    Adds a new event to the agenda or modifies an existing one.
    The arguments must have the following format: dd/mm/aaaaa hh:mm content
    """
    if len(args) >= 3:
        date, title, content = parse_event_args(args)
        # Creates a new event document
        event = Event(title=title, date=date, content=content)
        event.save()  # Save event in the db
        update.message.reply_text(
            'New event added: {}'.format(event.to_string()))
    else:
        update.message.reply_text('Invalid command format')
    
def remove(bot, update, args):
    title = args[0]
    event = Event.objects(title=title)
    print(event)
    if event:
        event.delete()
        update.message.reply_text('Event {} has been removed'.format(title))
    else:
        update.message.reply_text('Event {} not found'.format(title))


# Connects to the mongo database (localhost by default)
me.connect(db='Agenda')

# Gets the bot updater and dispatcher
updater = Updater(TOKEN)
dp = updater.dispatcher

# Main commands
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('agenda', agenda))
dp.add_handler(CommandHandler('event', event, pass_args=True))
dp.add_handler(CommandHandler('remove', remove, pass_args=True))

# Not implemented commands
dp.add_handler(MessageHandler(Filters.command, unknown))

# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()
