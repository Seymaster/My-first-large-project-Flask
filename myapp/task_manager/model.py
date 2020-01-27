import mongoengine as me
import datetime

class Taskman(me.Document):
        task =  me.StringField(required=True,max_length=300)
        date_created = me.DateTimeField(default=datetime.datetime.utcnow())