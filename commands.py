from utils import (
    collection_to_string,
    parse_reminder_args,
    parse_date,
    remove_messages_chain,
    show_candidate_events
)
from emoji import emojize
from models import Event, Modification, Exam, Deadline
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import InlineKeyboardButton as Button, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

DATE, TITLE, DESCRIPTION, EXAM_TYPE, PROFESSOR, SUBJECT, CLASSROOM, GROUP = range(8)
MULTIPLE_OPTIONS, MOD_SELECTION, MOD_APPLY = range(3)
EVENT_MOD_KEYBOARD = ReplyKeyboardMarkup([['Titulo', 'Descripcion'], ['Inicio', 'Fin'], ['Terminar']], one_time_keyboard=True)

def show_keyboard_options(update, context):
    update.message.reply_text('Selecciona el dato que quieres modificar', reply_markup=EVENT_MOD_KEYBOARD)


def start(update, context):
    """
    Simple start command to introduce the bot functionality
    """
    update.message.reply_text(
        'Hola! Escribe /agenda para ver los eventos guardados')


def agenda(update, context):
    """
    Displays all the events in the agenda
    """
    # Gets all the documents in the Events collection
    events = Event.objects
    if len(events) > 0:
        message = collection_to_string(events)
        update.message.reply_markdown(message)
    else:
        message = emojize(
            'La agenda está vacía :books:. Escribe /event para crear un nuevo evento!', use_aliases=True)
        update.message.reply_text(message)


def remove(update, context):
    """
    Removes an event from the agenda (it needs the event title as argument)
    """
    title = context.args[0]
    event = Event.objects(title=title)
    if event:
        event.delete()
        update.message.reply_text(
            "El evento '{}' ha sido eliminado".format(title))
    else:
        update.message.reply_text(
            "No se encuentra el evento '{}'".format(title))


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
            ':clock3: El recordatorio se activará a las {} :clock3:'.format(time), use_aliases=True))
    else:
        update.message.reply_text('Formato inválido')


# Event creation

def event(update, context):
    reply = update.message.reply_text(
        "Introduce la fecha y opcionalmente las horas de inicio y fin del evento con el formato dd/mm/yyyy hh:mm hh:mm. Si no se introduce ninguna hora se interpretará como que el evento dura todo el dia")
    context.user_data['messages'] = [reply]
    context.user_data['event'] = Event()

    return DATE


def exam(update, context):
    reply = update.message.reply_text("¿De qué asignatura es el examen?")
    context.user_data['messages'] = [reply]
    context.user_data['event'] = Exam()
    return SUBJECT


def subject(update, context):
    context.user_data['event'].subject = update.message.text
    reply = update.message.reply_text(
        "¿El examen es de tipo teórico o práctico?")
    context.user_data['messages'].extend([update.message, reply])

    return EXAM_TYPE


def exam_type(update, context):
    context.user_data['event'].exam_type = update.message.text
    reply = update.message.reply_text(
        "¿En qué grupo es el examen? Escribe 1, 2 o 3 para los practicos y 0 para grupo de teoria")
    context.user_data['messages'].extend([update.message, reply])

    return GROUP


def exam_group(update, context):
    context.user_data['event'].group = update.message.text
    reply = update.message.reply_text("¿Quién es el profesor del examen?")
    context.user_data['messages'].extend([update.message, reply])

    return PROFESSOR


def professor(update, context):
    context.user_data['event'].professor = update.message.text
    reply = update.message.reply_text("¿En qué aula es el examen?")
    context.user_data['messages'].extend([update.message, reply])

    return CLASSROOM


def classroom(update, context):
    context.user_data['event'].classroom = update.message.text
    reply = update.message.reply_text(
        "Introduce la fecha y opcionalmente las horas de inicio y fin con el formato dd/mm/yyyy hh:mm hh:mm. Si no se introduce ninguna hora se interpretará como que dura todo el dia")
    context.user_data['messages'].extend([update.message, reply])

    return DATE


# Conversational state
def date(update, context):
    try:
        start, end = parse_date(update.message.text)
    except ValueError:
        reply = update.message.reply_text(
            "Formato incorrecto, recuerda que el formato es dd/mm/yyyy hh:mm hh:mm y que las horas son opcionales")
        context.user_data['messages'].append(reply)
        return DATE

    context.user_data['event'].start = start
    context.user_data['event'].end = end
    reply = update.message.reply_text("Introduce un titulo")
    context.user_data['messages'].extend([update.message, reply])

    return TITLE


def title(update, context):
    context.user_data['event'].title = update.message.text
    reply = update.message.reply_text(
        "Para terminar introduce una descripción (en un examen por ejemplo estaria bien poner los temas que caen)")
    context.user_data['messages'].extend([update.message, reply])

    return DESCRIPTION


def description(update, context):
    context.user_data['event'].description = update.message.text
    context.user_data['messages'].append(update.message)
    save_event(update, context)

    return ConversationHandler.END


def save_event(update, context):
    event = context.user_data['event']
    event.chat_id = update.message.chat_id
    event.save()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="---- Nuevo evento añadido ----\n{}".format(str(event)))
    remove_messages_chain(context.user_data['messages'])


def cancel(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id, text='Proceso cancelado')
    context.user_data['messages'].append(update.message)
    remove_messages_chain(context.user_data['messages'])

    return ConversationHandler.END


def mod_event(update, context):
    result = Event.objects(title__iexact=' '.join(context.args))
    if len(result) > 1:
        context.user_data['options'] = result
        update.message.reply_text(show_candidate_events(result))
        return MULTIPLE_OPTIONS
    elif len(result) == 1:
        context.user_data['event'] = result[0]
        show_keyboard_options(update, context)
        return MOD_SELECTION
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id, text="Lo siento, no hay eventos con ese título")


def select_option(update, context):
    try:
        index = int(update.message.text)
    except ValueError:
        update.message.reply_text(
            "Opcion incorrecta. Vuelve a introducir el numero")
        return MULTIPLE_OPTIONS

    context.user_data['event'] = context.user_data['options'][index]
    show_keyboard_options(update, context)
    return MOD_SELECTION


def select_field(update, context):
    if update.message.text == 'Terminar':
        finish_mod(update, context)
    else:
        context.user_data['selection'] = update.message.text
        update.message.reply_text('Introduce el nuevo valor para ese campo', reply_markup=ReplyKeyboardRemove())
        return MOD_APPLY


def apply_mod(update, context):
    selection = context.user_data['selection']

    if selection == 'Descripcion':
        context.user_data['event'].description = update.message.text

    update.message.reply_text('El campo {} ha sido modificado'.format(selection.lower()))
    show_keyboard_options(update, context)
    
    return MOD_SELECTION


def finish_mod(update, context):
    event = context.user_data['event']
    event.save()
    event.modify(push__modifications=Modification(author=update.message.from_user.username))
    context.bot.send_message(
        chat_id=update.message.chat_id, 
        text="---- Evento modificado ----\n{}".format(str(event)), 
        reply_markup=ReplyKeyboardRemove())


# Commands definition
event_handler = ConversationHandler(
    entry_points=[CommandHandler('event', event),
                  CommandHandler('exam', exam)],
    states={
        DATE: [MessageHandler(Filters.text, date)],
        TITLE: [MessageHandler(Filters.text, title)],
        DESCRIPTION: [MessageHandler(Filters.text, description)],
        EXAM_TYPE: [MessageHandler(Filters.text, exam_type)],
        PROFESSOR: [MessageHandler(Filters.text, professor)],
        SUBJECT: [MessageHandler(Filters.text, subject)],
        CLASSROOM: [MessageHandler(Filters.text, classroom)],
        GROUP: [MessageHandler(Filters.text, exam_group)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

mod_event_handler = ConversationHandler(
    entry_points=[CommandHandler('mod', mod_event)],
    states={
        MULTIPLE_OPTIONS: [MessageHandler(Filters.text, select_option)],
        MOD_SELECTION: [MessageHandler(Filters.text, select_field)],
        MOD_APPLY: [MessageHandler(Filters.text, apply_mod)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

start_handler = CommandHandler('start', start)
agenda_handler = CommandHandler('agenda', agenda)
remove_handler = CommandHandler('remove', remove)
reminder_handler = CommandHandler('reminder', reminder)