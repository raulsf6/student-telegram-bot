import os
import mongoengine as me
from telegram.ext import Updater
from commands import (
    start_handler,
    agenda_handler,
    remove_handler,
    reminder_handler,
    event_handler
)
from extra_handlers import (
    error,
    unknown_command
)

# Environment variables
TOKEN = os.environ['TELEGRAM_TOKEN']

if __name__ == "__main__":
    # Connects to the mongo database (localhost by default)
    me.connect(db='Agenda')

    # Gets the bot updater and dispatcher
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Main commands
    dp.add_handler(start_handler)
    dp.add_handler(agenda_handler)
    dp.add_handler(remove_handler)
    dp.add_handler(reminder_handler)
    dp.add_handler(event_handler)
    dp.add_handler(unknown_command)

    # Logging error handler
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(clean=True)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
