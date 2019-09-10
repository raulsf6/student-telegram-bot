import mongoengine as me
from datetime import datetime

# Aqui pondremos la estructura de una colección de mongo (como una tabla en SQL).
# Cada clase representa la estructura de un documento (como una fila en SQL).
# El nombre de la colección se especifica en la variable meta de la clase Document

def date():
    return datetime.now().replace(microsecond=0)


class Modification(me.EmbeddedDocument):
    author = me.StringField(required=True)
    date = me.DateTimeField(default=date)

    def __repr__(self):
        return '{} - {}'.format(self.author, self.date)
    
class Event(me.Document):
    chat_id = me.IntField(required=True)
    title = me.StringField(required=True)
    start = me.DateTimeField(required=True)
    end = me.DateTimeField()
    description = me.StringField(required=True)
    modifications = me.EmbeddedDocumentListField(Modification)

    def __str__(self):
        return 'Titulo: {}\nInicio: {}\nFin: {}\nDescripcion: {}\nModificaciones:\n{}'.format(
            self.title,
            self.start,
            self.end if self.end else 'No definida',
            self.description,
            self.modifications
        )

    meta = {'collection': 'Events', 'allow_inheritance': True}


class Exam(Event):
    subject = me.StringField(required=True)
    professor = me.StringField(required=True)
    exam_type = me.StringField(required=True)
    classroom = me.StringField(required=True)
    group = me.StringField(required=True)

    def __str__(self):
        exam_str = 'Asignatura: {}\nTipo: {}\nGrupo: {}\nProfesor: {}\nAula: {}\n'.format(
            self.subject, 
            self.exam_type,
            self.group, 
            self.professor, 
            self.classroom
        )
        return exam_str + super().__str__()
        

class Deadline(Event):
    moodle = me.StringField(required=True)
