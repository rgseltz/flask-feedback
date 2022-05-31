from click import password_option
from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import NewUserForm, UserForm
# from forms import UserForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/', methods=["GET"])
def show_index():
    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register_user():
    form = NewUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username=username, pwd=password,
                                 email=email, first=first_name, last=last_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/secret')
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            flash(f'Welcome back {user.first_name}')
            print(session)
            session['username'] = user.username
            return redirect('/secret')
        else:
            form.username.errors = ['Invalid username/password']
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)


@app.route('/secret', methods=["GET"])
def show_secret():
    if "username" not in session:
        return redirect('/')
    return render_template('secret.html')


@app.route('/logout', methods=["GET"])
def logout_user():
    session.pop("username")
    return redirect('/')
