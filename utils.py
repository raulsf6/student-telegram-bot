from datetime import datetime, time

# Commands
def collection_to_string(collection):
    """
    Converts a collection of documents to a string to be sent by the bot
    """
    string = '*Agenda* \n'
    for doc in collection:
        string += '{}\n\n'.format(str(doc))
    return string


def parse_reminder_args(args):
    hour, minute = int(args[0]), int(args[1])
    reminder_time = time(hour, minute, 0)
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

def show_candidate_events(events):
    string = "Hay varios eventos con el mismo título, dime el numero de la lista que coincide con el que quieres:\n"
    for index, event in enumerate(events):
        string += "{} -> {} | {}\n".format(index, event.start, event.description)
    print(string)
    return string