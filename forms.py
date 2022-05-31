from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Email


class NewUserForm(FlaskForm):
    username = StringField("Create Username", validators=[InputRequired()])

    password = StringField("Create Password", validators=[InputRequired()])

    email = StringField("Enter Email", validators=[InputRequired(), Email()])

    first_name = StringField("Enter First Name", validators=[InputRequired()])

    last_name = StringField("Enter Last Name", validators=[InputRequired()])
