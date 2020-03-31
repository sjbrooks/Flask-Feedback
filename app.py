from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import createUserForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()
toolbar = DebugToolbarExtension(app)

@app.route('/')
def get_root():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def get_register():

    form = createUserForm()

    ## How do we loop through to extract these instead of hardcoding?
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        flash(f'Added {username}')

        user = User(username=username, 
                    password=password, 
                    email=email, 
                    first_name=first_name,
                    last_name=last_name)

        db.session.add(user)
        db.session.commit()

        return redirect('/secret')

    else:
        return render_template('user-registration-form.html', 
                               form=form)
