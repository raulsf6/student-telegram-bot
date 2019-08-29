import os
import mongoengine as me
from utils import collection_to_string, parse_event_args, parse_reminder_args
from emoji import emojize
from models import Event
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Environment variables
TOKEN = os.environ['TELEGRAM_TOKEN']

################
# Bot commands #
################


def start(update, context):
    """
    Simple start command to introduce the bot functionality
    """
    update.message.reply_text('Hey! Type /agenda to check for events')


def unknown(update, context):
    """
    Executed when command is not implemented
    """
    update.message.reply_text("Sorry, I didn't understand that command.")


def agenda(update, context):
    """
    Displays all the events in the agenda
    """
    # Gets all the documents in the Events collection
    events = Event.objects
    if len(events) > 0:
        message = collection_to_string(events)
        update.message.reply_text(message)
    else:
        message = emojize(
            'The agenda is empty :books:. Type /event to create a new one!', use_aliases=True)
        update.message.reply_text(message)


def event(update, context):
    """
    Adds a new event to the agenda or modifies an existing one.
    The arguments must have the following format: dd/mm/aaaaa hh:mm content
    """
    if len(context.args) >= 4:
        date, title, content = parse_event_args(context.args)
        # Creates a new event document
        event = Event(title=title, date=date, content=content)
        event.save()  # Save event in the db
        update.message.reply_text(
            'New event added: {}'.format(event.to_string()))
    else:
        update.message.reply_text('Invalid command format')


def remove(update, context):
    """
    Removes an event from the agenda (it needs the event title as argument)
    """
    title = context.args[0]
    event = Event.objects(title=title)
    if event:
        event.delete()
        update.message.reply_text('Event {} has been removed'.format(title))
    else:
        update.message.reply_text('Event {} not found'.format(title))


def timer_message(context):
    """
    Callback executed when reminder is trigered
    """
    context.bot.send_message(chat_id=context.job.context[0], text=context.job.context[1])


def reminder(update, context):
    """
    Sets a reminder at the specified time.
    The arguments must be like: hour minute message
    """
    if len(context.args) >= 3:
        time, message = parse_reminder_args(context.args)
        job_queue = context.job_queue
        job_queue.run_daily(timer_message, time, context=[
                            update.message.chat_id, message])
        update.message.reply_text(emojize(
            ':clock3: Reminder will trigger at {} :clock3:'.format(time), use_aliases=True))
    else:
        update.message.reply_text('Invalid command format')


# Connects to the mongo database (localhost by default)
me.connect(db='Agenda')

# Gets the bot updater and dispatcher
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

# Main commands
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('agenda', agenda))
dp.add_handler(CommandHandler('event', event))
dp.add_handler(CommandHandler('remove', remove))
dp.add_handler(CommandHandler('reminder', reminder))

# Not implemented commands
dp.add_handler(MessageHandler(Filters.command, unknown))

# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()
