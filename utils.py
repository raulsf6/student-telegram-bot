from datetime import datetime, time

def collection_to_string(collection):
    """
    Converts a collection of documents to a string to be sent by the bot
    """
    string = ''
    for doc in collection:
        string += '{}\n\n'.format(doc.to_string())
    return string

def parse_event_args(args):
    """
    Extracts the date and the content of an event
    """
    # Joins the date and the hour in a string like 'dd/mm/aaaa hh:mm'
    string_date = ' '.join(args[0:2])
    title = args[2]
    # Gets the content as a string with the words separated by spaces
    content = ' '.join(args[3:])
    # Converts the date string to a datetime object
    # TODO: Ensure that the format of string_date is ok
    date = datetime.strptime(string_date, '%d/%m/%Y %H:%M')
    return date, title, content

def parse_reminder_args(args):
    reminder_time = time(int(args[0]), int(args[1]), 0)
    message = 'Reminder: {}'.format(' '.join(args[2:]))
    return reminder_time, message
