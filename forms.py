from flask_wtf import FlaskForm

from wtforms import StringField, DateField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    ID_number = StringField('Unique ID', validators=[DataRequired(), Length(min=2, max=30)])
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=30)])
    phone = StringField('Phone Number',
                        validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    offense_date = DateField('Offense Date', format='%m/%d/%Y', validators=[DataRequired()])
    gender = StringField('Gender',
                         validators=[DataRequired()])
    offense = TextAreaField('Offense', validators=[DataRequired()])
    plate_number= StringField('Plate Number', validators=[DataRequired()])
    submit = SubmitField('Book')


class profileForm(FlaskForm):
    User_id = StringField('Unique Number',
                        validators=[DataRequired()])

    submit = SubmitField('Login')
