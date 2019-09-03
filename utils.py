from datetime import datetime, time
import re

# Commands
def collection_to_string(collection):
    """
    Converts a collection of documents to a string to be sent by the bot
    """
    string = '*Agenda* \n'
    for doc in collection:
        string += '{}\n\n'.format(doc.__str__())
    return string


def parse_reminder_args(args):
    reminder_time = time(int(args[0]), int(args[1]), 0)
    message = 'Reminder: {}'.format(' '.join(args[2:]))
    return reminder_time, message


def parse_date(string):
    args = string.split(' ')
    if len(args) == 1:
        return datetime.strptime(args[0], '%d/%m/%Y'), None
    elif len(args) == 2:
        return datetime.strptime('{} {}'.format(args[0], args[1]), '%d/%m/%Y %H:%M'), None
    else:
        start = datetime.strptime('{} {}'.format(
            args[0], args[1]), '%d/%m/%Y %H:%M')
        end = datetime.strptime('{} {}'.format(
            args[0], args[2]), '%d/%m/%Y %H:%M')
        return start, end


def remove_messages_chain(messages):
    for message in messages[::-1]:
        message.delete()


# Models
def create_modifications_string(modifications):
    string = ''
    for m in modifications:
        string += '\t -> {} - {}'.format(m.author, m.date)
    return string
