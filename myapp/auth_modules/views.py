from flask import Blueprint,request,render_template,redirect,url_for,flash,Flask,jsonify
import bcrypt
from myapp.auth_modules.forms import RegisterForm,LoginForm
from myapp.auth_modules.models import Users
from myapp.task_manager.views import todo_blu
from pymongo.errors import ServerSelectionTimeoutError
from mongoengine.errors import FieldDoesNotExist,ValidationError,NotUniqueError
from jinja2 import TemplateError,TemplateNotFound,UndefinedError,TemplateSyntaxError
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,create_refresh_token,jwt_refresh_token_required



blu_auth = Blueprint('valid',__name__,url_prefix='/valid')
# jwt = JWTManager(blu_auth)

@blu_auth.route('/')
def home():
    return redirect(url_for('valid.signup'))

@blu_auth.route('/signup', methods =['POST','GET'])
def signup():
    message = None
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate == False:
            flash('All fields are required')
            return render_template('/auth_temp/signup.html',form = form)
        else:
            try:
                staredPw = bcrypt.hashpw(request.form['password'].encode("utf-8"),bcrypt.gensalt())
                membs = Users()
                data = Users(name = request.form['name'],email = request.form['email'],password = staredPw)
                data.save()
                # return jsonify({
                #     "status" : 200,
                #     "data": data,
                #     "message": "Successfully Saved user"
                # }),200
                return render_template('/auth_temp/thank_you.html')
            except NotUniqueError as e:
                x = str(e)
                y = x.split()
                z = y[13]
                message = f'{z[0:5]} already exist'
                # added = Users.objects(name =request.form['name'],email=request.form['email']).first()
                return render_template('/auth_temp/signup.html', form = form, message = message )
    else:
        return render_template('/auth_temp/signup.html', form = form)


    
@blu_auth.route('/thank_you', methods=['POST','GET'])
def thank_you():
    name = request.form['name']
    return render_template('/auth_temp/thank_you.html', name = name )

@blu_auth.route('/login', methods = ['POST','GET'])
def login():
    message = None
    form = LoginForm()
    if request.method == 'POST':
        email = request.get_json()['email']
        password = request.get_json()['password']
        membs = Users.objects(email = email).first()
        if membs:
            logpw = password.encode("utf-8")
            if bcrypt.checkpw(logpw,membs['password'].encode("utf-8")):
                token = create_access_token({
                    "email":membs["email"]
                })
                return jsonify({
                    "status":200,
                    "message":"Login Successful",
                    "token"  : token
                }),200
                # return "Welcome User"
            else:
                return jsonify({
                    "status" : 400,
                    "message": "Invalid Credentials"
                }),400
                # return redirect('/task')
            # return render_template("/auth_temp/login.html", form = form, message = message )
        else:
            return jsonify({
                    "status" : 400,
                    "message": "Invalid Credentials"
                }),400

            # message = "Invalid credentials"
            # return render_template("/auth_temp/login.html", form = form, message = message )
    else:
        return render_template('/auth_temp/login.html', form = form)

@blu_auth.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404





