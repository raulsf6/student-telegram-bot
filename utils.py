from datetime import datetime, time

def collection_to_string(collection):
    """
    Converts a collection of documents to a string to be sent by the bot
    """
    string = ''
    for doc in collection:
        string += '{}\n\n'.format(doc.to_string())
    return string

def parse_reminder_args(args):
    reminder_time = time(int(args[0]), int(args[1]), 0)
    message = 'Reminder: {}'.format(' '.join(args[2:]))
    return reminder_time, message

def create_date(string):
    return datetime.strptime(string, '%d/%m/%Y')
