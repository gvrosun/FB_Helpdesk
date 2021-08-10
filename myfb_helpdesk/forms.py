from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from myfb_helpdesk.models import User


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=5, max=35)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), ])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm')
    ])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            return False
        return True

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            return False
        return True
