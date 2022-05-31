from ast import In
from tokenize import String
from xml.dom import InuseAttributeErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email


class NewUserForm(FlaskForm):
    username = StringField("Create Username", validators=[InputRequired()])

    password = PasswordField("Create Password", validators=[InputRequired()])

    email = StringField("Enter Email", validators=[InputRequired(), Email()])

    first_name = StringField("Enter First Name", validators=[InputRequired()])

    last_name = StringField("Enter Last Name", validators=[InputRequired()])


class UserForm(FlaskForm):
    username = StringField("Enter Username", validators=[InputRequired()])

    password = PasswordField("Enter Password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    title = StringField("Feedback Title", validators=[InputRequired()])

    content = TextAreaField("Enter Feedback", validators=[InputRequired()])
