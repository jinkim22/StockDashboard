from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from Users import trader

def invalid_input(form, field):
    """ Check username and password"""
    username = form.username.data
    password = field.data
    user_object = trader.query.filter_by(username=username).first()
    if user_object is None:
        raise ValidationError("Username already exists. Pick a different username.")
    elif password != user_object.password:
        raise ValidationError("Username or Password is incorrect")

class RegistrationForm(FlaskForm):
    """ Registration form"""

    username = StringField('username', validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    password = PasswordField('password', validators=[InputRequired(message="Password required"), Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pswd', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])


    def validate_username(self, username):
        user_object = trader.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists. Pick a different username.")

class LoginForm(FlaskForm):
    username = StringField('username_label', validators = [InputRequired(message="Username required")])
    password = PasswordField('password_label', validators = [InputRequired(message="Password required"),invalid_input])
    submit_button = SubmitField('login')
