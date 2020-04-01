from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import createUserForm, loginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

app.config["SECRET_KEY"] = "abc123"

connect_db(app)

# use as needed to drop all tables
# db.drop_all()
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def get_root():
    """Redirect root to /register."""
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """If the request is POST and form data is valid, create a new instance of User class
    with submitted values and redirect to the /users/<username> route. Otherwise, render the form template."""

    form = createUserForm()

    ## How do we loop through to extract these instead of hardcoding?
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        flash(f'Added {username}')

        user = User.register(username,
                             password,
                             email,
                             first_name,
                             last_name)

        db.session.add(user)
        db.session.commit()

        session["user_username"] = user.username

        return redirect(f'/users/{user.username}')

    else:
        return render_template('user-registration-form.html',
                               form=form)


@app.route('/login', methods=['GET', 'POST'])
def log_in():
    """If the request is POST and form data is valid, check credential to authenticate.
    If authentication is true, add current user to the session and redirect to /users/<username> route.
    Otherwise, render the form template."""

    if "user_username" in session:
        return redirect(f'/users/{session["user_username"]}')

    form = loginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        print("\n\n\n THE USER IS", user)

        if user:
            session["user_username"] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid username/password"]

    return render_template('login-form.html',
                           form=form)


@app.route('/users/<username>')
def user_detail(username):
    """"Check if username in session, render user page if username in session. If not in session, redirect to homepage and flash message that must be logged in to view that page."""

    if "user_username" not in session:
        flash("You must be logged in to view")
        return redirect('/')

    user = User.query.get(username)

    return render_template('user.html',
                           user=user)

@app.route('/logout')
def logout():
    """Logout user and redirect to homepage."""

    session.pop("user_username", None)

    return redirect("/")
