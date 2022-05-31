from email import contentmanager
from http.client import UNAUTHORIZED
from click import password_option
from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import NewUserForm, UserForm, FeedbackForm
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
        flash('You successfully signed up!')
        return redirect('/login')
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
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Invalid username/password']
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)


@app.route('/logout', methods=["GET"])
def logout_user():
    session.pop("username")
    return redirect('/')


@app.route('/users/<username>', methods=["GET"])
def show_user(username):
    user = User.query.get_or_404(username)
    feedback = user.feedback
    if session["username"] == username:
        return render_template('user-details.html', user=user, feedback=feedback)
    else:
        flash('You are not authorized to access that page!')
        return redirect('/login')


@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username = session["username"]
        new_feedback = Feedback(
            title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        return render_template('feedback-form.html', form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    f = Feedback.query.get(feedback_id)
    form = FeedbackForm(obj=f)
    if form.validate_on_submit():
        f.title = form.title.data
        f.content = form.content.data
        return redirect(f'/users/{f.user.username}')
    return render_template('feedback-edit.html', form=form)


@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.user.username
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{username}')
