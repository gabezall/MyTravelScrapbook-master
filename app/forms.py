from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, \
    SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, City, State, Country, CityToState, StateToCountry
from wtforms.fields.html5 import DateField, DateTimeField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CreateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
       'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_username(self, username):
       user = User.query.filter_by(username=username.data).first()
       if user is not None:
           raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class NewFutureLocation(FlaskForm):
    country = StringField('Country', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    city = StringField('City')
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Location')


class NewPastLocation(FlaskForm):
    country = StringField('Country', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    city = StringField('City')
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Location')


class AddEventForm(FlaskForm):
    event = StringField('Event Name', validators=[DataRequired()])
    time = DateTimeField('Date (MM-DD-YYYY)', format='%m-%d-%Y')
    #LIST VENUES
    venue = SelectField(u'Venue', coerce=int)
    artists = SelectMultipleField(u'Artist(s)', coerce=int)
    submit = SubmitField('Add Event')
