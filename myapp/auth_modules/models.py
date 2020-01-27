import mongoengine as medb
import datetime

class Users(medb.Document):
    name = medb.StringField(required=True,max_length=50,unique = True)
    email = medb.EmailField(required=True,max_length=30,unique= True)
    password = medb.StringField(required=True)
    datecreated = medb.DateTimeField(default=datetime.datetime.utcnow)

class Products(medb.Document):
    description = medb.StringField(required=True,max_length=500)
    price = medb.IntField(required=True,max_value=15)
    