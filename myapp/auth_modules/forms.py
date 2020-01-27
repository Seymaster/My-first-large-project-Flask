from flask_wtf import FlaskForm
from wtforms import TextField,IntegerField,TextAreaField,SubmitField,RadioField,PasswordField,SelectField
from wtforms import validators, ValidationError

class RegisterForm(FlaskForm):
    name = TextField("Name",[validators.Required("Please enter your name")])
    email = TextField("Email",[validators.Required("Please enter your email address"),
        validators.Email("Please enter a valid email ")])
    password = PasswordField("Password",[validators.Required("Please enter your password")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = TextField("Username",[validators.Required("Please enter your username")])
    password = PasswordField("Password",[validators.Required("Please Enter your password")])
    submit = SubmitField('Login')