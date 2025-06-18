from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('user', 'User'), ('creator', 'Event Creator')], validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EventForm(FlaskForm):
    title = StringField('Event Name', validators=[DataRequired()])
    date = DateTimeField('Date (YYYY-MM-DD HH:MM)', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    venue = StringField('Venue', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Event')