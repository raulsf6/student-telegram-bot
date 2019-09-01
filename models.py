import mongoengine as me
from datetime import datetime

# Aqui pondremos la estructura de una colección de mongo (como una tabla en SQL).
# Cada clase representa la estructura de un documento (como una fila en SQL).
# El nombre de la colección se especifica en la variable meta de la clase Document

class Event(me.Document):
    title = me.StringField(primary_key=True)
    start = me.DateTimeField(required=True)
    end = me.DateTimeField()
    description = me.StringField()
    last_modification = me.DateTimeField(default=datetime.utcnow)

    def to_string(self):
        return 'Titulo: {}\nDescripcion: {}\nFecha: {} - {}'.format(self.title, self.description, self.start, self.end)

    meta = {'collection': 'Events', 'allow_inheritance' : True}

class Exam(Event):
    subject = me.StringField(required=True)
    professor = me.StringField(required=True)
    exam_type = me.StringField(required=True)
    classroom = me.StringField(required=True)

class Submission(Event):
    moodle = me.StringField(required=True)