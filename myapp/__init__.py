from flask import Flask
from mongoengine import connect
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__, instance_relative_config= True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
connect(host = app.config['MONGOURI'])
app.config['CSRF_ENABLED']
app.config['CSRF_SECRET_KEY']
app.config['SECRET_KEY']
app.config['JWT_SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES']  
jwt =    JWTManager(app)
cors = CORS(app)
from myapp.auth_modules.views import blu_auth
from myapp.task_manager.views import todo_blu
app.register_blueprint(blu_auth)
app.register_blueprint(todo_blu)