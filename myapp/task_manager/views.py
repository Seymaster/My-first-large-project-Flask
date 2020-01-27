from flask import Blueprint, render_template, redirect, request,url_for,jsonify
from myapp.task_manager.model import Taskman
from bson import ObjectId
import datetime
import json
from jinja2 import TemplateError,TemplateNotFound,UndefinedError,TemplateSyntaxError
from pymongo.errors import ServerSelectionTimeoutError
from mongoengine.errors import FieldDoesNotExist,ValidationError,NotUniqueError
from flask_jwt_extended import create_access_token,jwt_required,create_refresh_token,jwt_refresh_token_required

todo_blu = Blueprint('task',__name__, url_prefix='/task')
@todo_blu.route('/')
@jwt_required
def index():
    try:
        tasks = Taskman.objects()
        data = [json.loads(task.to_json()) for task in tasks]
       
        return jsonify({
            "status" :200,
            "message": "Fetched tasks",
            "data" : data
            
        })
    except TemplateNotFound as e:
        return f"Template Error {e.message} This template does not exist"
    except ServerSelectionTimeoutError as e:
        return f"DB Error {e.message} Could not connect to database"
    


@todo_blu.route('/create' ,methods=['POST'])
def create():
    try:
        # declaring error 
        error = None
        # targeting the contents
        task   = request.form['content']
        # date_created = datetime.datetime.utcnow()
        # Assigning to database 
        tasks = Taskman( task  = task
                        )
        # Inserting to the database
        tasks.save()  
    except FieldDoesNotExist as e:
        return f'{e}'  
    return redirect(url_for('task.index'))
    # return "landing page"

@todo_blu.route('/delete')
def deleteTodo():
    # targeting the data with the id
    id = request.values.get('id')
    # deleting it in the database 
    Taskman.objects(id = ObjectId(id)).delete()
    return redirect(url_for('task.index'))

@todo_blu.route('/update')
def update():
    if request.method == "POST":
        task  = request.form['content']
        id     = request.values.get('id')
        Taskman.objects( id = ObjectId(id)).update( task = task)
        return redirect(url_for('task.index'))
    else:
        id = request.values.get('id')
        tasks = Taskman.objects(id = ObjectId(id)).first()
        return render_template('auth_temp/update.html',tasks = tasks)


@todo_blu.route('/search' )
def search():
    key   = request.values.get("key")
    field = request.values.get("field")
    query = {}
    query[field] = key
    # print(query)
    tasks = Taskman.objects(**query)
    return render_template('/auth_temp/searchresult.html', tasks = tasks)


@todo_blu.app_errorhandler(404)
def error404(e):
    return render_template('/404.html'),404