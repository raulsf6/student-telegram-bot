import mongoengine as me
from datetime import datetime
from utils import create_modifications_string

# Aqui pondremos la estructura de una colección de mongo (como una tabla en SQL).
# Cada clase representa la estructura de un documento (como una fila en SQL).
# El nombre de la colección se especifica en la variable meta de la clase Document

class Modification(me.EmbeddedDocument):
    author = me.StringField(required=True)
    date = me.DateTimeField(default=datetime.now)
    
class Event(me.Document):
    title = me.StringField(primary_key=True)
    start = me.DateTimeField(required=True) # TODO: Eventos sin hora empiezan a las 00:00
    end = me.DateTimeField()
    description = me.StringField()
    modifications = me.EmbeddedDocumentListField(Modification)

    def __str__(self):
        end = '- {}'.format(self.end) if not (self.end is None) else ''
        mods_string = create_modifications_string(self.modifications)
        return 'Titulo: {}\nDescripcion: {}\nFecha: {} {}\nModifications:\n{}'.format(
            self.title,
            self.description,
            self.start,
            end,
            mods_string
        )

    meta = {'collection': 'Events', 'allow_inheritance': True}


class Exam(Event):
    subject = me.StringField(required=True)
    professor = me.StringField(required=True)
    exam_type = me.StringField(required=True)
    classroom = me.StringField(required=True)

    def __str__(self):
        exam_str = 'Asignatura: {}\nTipo: {}\nProfesor: {}\nAula: {}\n'.format(
            self.subject, 
            self.exam_type, 
            self.professor, 
            self.classroom
        )
        return exam_str + super().__str__()
        

class Deadline(Event):
    moodle = me.StringField(required=True)
