import mongoengine as me
from datetime import datetime

# Aqui pondremos la estructura de una colección de mongo (como una tabla en SQL).
# Cada clase representa la estructura de un documento (como una fila en SQL).
# El nombre de la colección se especifica en la variable meta de la clase Document

class Event(me.Document):
    title = me.StringField(primary_key=True)
    date = me.DateTimeField()
    content = me.StringField()
    last_modified = me.DateTimeField(default=datetime.utcnow())

    def to_string(self):
        return '{} - {}\n{}\nLast modified:{}'.format(self.date, self.title, self.content, self.last_modified)

    meta = {'collection': 'Events'}
