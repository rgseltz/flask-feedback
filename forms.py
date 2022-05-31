from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
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
