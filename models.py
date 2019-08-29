import mongoengine as me

# Aqui pondremos la estructura de una colección de mongo (como una tabla en SQL).
# Cada clase representa la estructura de un documento (como una fila en SQL).
# El nombre de la colección se especifica en la variable meta de la clase Document

class Event(me.Document):
    date = me.DateTimeField()
    content = me.StringField()

    meta = {'collection': 'Events'}
