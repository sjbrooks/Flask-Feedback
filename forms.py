from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class createUserForm(FlaskForm):
    """Form for creating a new user."""

    username = StringField("Username",
                           validators=[InputRequired(),
                                       Length(min=1, max=20)])
    password = PasswordField("Password",
                             validators=[InputRequired()])
    email = StringField("Email", 
                        validators=[InputRequired(), 
                                    Email(), 
                                    Length(min=1, max=50)])
    first_name = StringField("First Name",
                             validators=[InputRequired(),
                                         Length(min=1, max=30)])
    last_name = StringField("Last Name",
                            validators=[InputRequired(),
                                        Length(min=1, max=30)])


class loginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField("Username",
                           validators=[InputRequired()])
    password = PasswordField("Password",
                             validators=[InputRequired()])

