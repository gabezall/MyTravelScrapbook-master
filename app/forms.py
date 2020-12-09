from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, \
    SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Venue, City, Artist
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

class AddNewArtistForm(FlaskForm):
    new_artist = StringField('Artist Name', validators=[DataRequired()])
    town = StringField('Hometown')
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Artist')


class AddNewVenueForm(FlaskForm):
    venue = StringField('Venue Name', validators=[DataRequired()])
    #LIST TOWN
    city = SelectField(u'Venue Location', coerce=int)
    submit = SubmitField('Add Venue')


class AddEventForm(FlaskForm):
    event = StringField('Event Name', validators=[DataRequired()])
    time = DateTimeField('Date (MM-DD-YYYY)', format='%m-%d-%Y')
    #LIST VENUES
    venue = SelectField(u'Venue', coerce=int)
    artists = SelectMultipleField(u'Artist(s)', coerce=int)
    submit = SubmitField('Add Event')
