from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import RegistrationForm, profileForm

# from app import db

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///offender.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    ID_number = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    phone = db.Column(db.String(13), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    offense_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    gender = db.Column(db.String(13), unique=False, nullable=False)
    offense = db.Column(db.String(200), unique=False, nullable=False)
    plate_number = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f"User('{self.ID_number}', '{self.first_name}', '{self.last_name}')"


class National(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    middle_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    address = db.Column(db.String(200), unique=False, nullable=False)
    marital_status = db.Column(db.String(50), unique=False, nullable=False)
    gender = db.Column(db.String(50), unique=False, nullable=False)
    dob = db.Column(db.String(50), unique=False, nullable=False)
    place_of_birth = db.Column(db.String(200), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    phone = db.Column(db.String(13), unique=False, nullable=False)
    no_of_cars = db.Column(db.String(120), unique=False, nullable=False)
    state = db.Column(db.String(120), unique=False, nullable=False)
    lga = db.Column(db.String(120), unique=False, nullable=False)
    nationality = db.Column(db.String(120), unique=False, nullable=False)
    occupation = db.Column(db.String(120), unique=False, nullable=False)
    profile_pics = db.Column(db.String(20), nullable=False, default='default.jpg')
    nok_fname = db.Column(db.String(120), unique=False, nullable=False)
    nok_lname = db.Column(db.String(120), unique=False, nullable=False)
    nok_email = db.Column(db.String(120), unique=False, nullable=False)
    nok_gender = db.Column(db.String(13), unique=False, nullable=False)
    nok_phone = db.Column(db.String(200), unique=False, nullable=False)
    nok_relationship = db.Column(db.String(120), unique=False, nullable=False)
    nok_address = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f"User('{self.user_id}', '{self.first_name}', '{self.last_name}')"


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        offender = User(ID_number=form.ID_number.data, first_name=form.first_name.data,
                        last_name=form.last_name.data, phone=form.phone.data, email=form.email.data,
                        offense_date=form.offense_date.data, gender=form.gender.data,
                        offense=form.offense.data, plate_number=form.plate_number.data)
        db.session.add(offender)
        db.session.commit()
        flash(f'{form.first_name.data} successfully booked!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/profile", methods=['POST', 'GET'])
def profile():
    title = "Profile an offender"
    return render_template('profile.html', title='profile')


@app.route("/display", methods=['GET', 'POST'])
def display():
    ID_number = request.form.get("ID_number")
    offender = User.query.filter_by(ID_number = ID_number).first()
    number_booked = User.query.filter_by(ID_number = ID_number).count()
    other_details = National.query.filter_by(user_id = ID_number).first()

    return render_template('display.html', offender=offender, number_booked=number_booked)


"""
@app.route("/display", methods=['GET', 'POST'])
def display():
    form = profileForm()
    if form.validate_on_submit():
        current_user.User_id = form.User_id.data
        db.session.commit()

    return render_template('display.html', title='Register', form=form)
"""

if __name__ == '__main__':
    app.run(debug=True)
