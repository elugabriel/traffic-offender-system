from flask_wtf import FlaskForm

from wtforms import StringField, DateField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    ID_number = StringField('Unique ID', validators=[DataRequired(), Length(min=2, max=30)])

    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone = StringField('Phone Number')
    email = StringField('Email')
    offense_date = DateField('Offense Date', format='%m/%d/%Y')
    gender = StringField('Gender')

    offense = SelectField('Offense', choices=[('speeding', 'Speeding'), ('bypass traffic Light', 'Bypass Light'),
                                              ('failure to stop', 'Failure to Stop'),
                                              ('suspicious', 'Suspicious')])

    plate_number = StringField('Plate Number', validators=[DataRequired()])
    submit = SubmitField('Book')


class profileForm(FlaskForm):
    ID_number = StringField('Unique ID', validators=[DataRequired(), Length(min=2, max=30)])
    offense_date = DateField('Offense Date', format='%m/%d/%Y', validators=[DataRequired()])

    submit = SubmitField('Login')
