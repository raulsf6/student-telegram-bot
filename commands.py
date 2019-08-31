from utils import collection_to_string, parse_reminder_args, create_date
from emoji import emojize
from models import Event
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

DATE, TITLE, CONTENT = range(3)


def start(update, context):
    """
    Simple start command to introduce the bot functionality
    """
    update.message.reply_text('Hey! Type /agenda to check for events')


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
    context.bot.send_message(
        chat_id=context.job.context[0], text=context.job.context[1])


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


# Event creation

def event(update, context):
    user = update.message.from_user.first_name
    update.message.reply_text(
        "Hi {}! Introduce the date of the event with the format dd/mm/yyyy".format(user))
    return DATE


def date(update, context):
    try:
        date = create_date(update.message.text)
        context.chat_data['date'] = date
        update.message.reply_text("Now introduce the title of the event")
    except ValueError:
        update.message.reply_text(
            "Bad format, introduce the date again with format dd/mm/yyyy")
        return DATE

    return TITLE


def title(update, context):
    context.chat_data['title'] = update.message.text
    update.message.reply_text("Now introduce the content")

    return CONTENT


def content(update, context):
    context.chat_data['content'] = update.message.text
    event = Event(date=context.chat_data['date'], title=context.chat_data['title'], content=context.chat_data['content'])
    event.save()
    update.message.reply_text('New event added: {}'.format(event.to_string()))


def cancel(update, context):
    update.message.reply_text('Event canceled')
    return -1


event_handler = ConversationHandler(
    entry_points=[CommandHandler('event', event)],
    states={
        DATE: [MessageHandler(Filters.text, date)],
        TITLE: [MessageHandler(Filters.text, title)],
        CONTENT: [MessageHandler(Filters.text, content)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

start_handler = CommandHandler('start', start)
agenda_handler = CommandHandler('agenda', agenda)
remove_handler = CommandHandler('remove', remove)
reminder_handler = CommandHandler('reminder', reminder)