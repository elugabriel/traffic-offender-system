import pandas as pd
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import RegistrationForm, profileForm
import numpy as np
import pickle
import sqlite3
import matplotlib.pyplot as plt
from datetime import date
import seaborn as sns
import vonage

# from app import db


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///offender.db'
db = SQLAlchemy(app)
model = pickle.load(open("model.pkl", "rb"))

client = vonage.Client(key="e841a316", secret="L30yj65nXWDBWhwp")
sms = vonage.Sms(client)

dataset = pd.read_csv("/home/gabriel/Documents/number_detection/realTimeResult.csv")


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    ID_number = db.Column(db.Integer, nullable=False)
    offense_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    offense = db.Column(db.String(200), unique=False, nullable=False)
    plate_number = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f"User('{self.ID_number}', '{self.offense_date}', '{self.plate_number}')"


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
    number = dataset.number
    image = dataset.id

    latest_number = number.iloc[-1]
    detected = str(latest_number)
    image_name = image.iloc[-1]
    string_image_name = str(image_name)
    img_source = "number_detection/detected_images/" + string_image_name

    return render_template('about.html', title='About', number=detected)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        offender = User(ID_number=form.ID_number.data, first_name=" ",
                        last_name=" ", phone=' ', email=" ",
                        offense_date=form.offense_date.data, gender=' ',
                        offense=form.offense.data, plate_number=form.plate_number.data)
        db.session.add(offender)
        db.session.commit()
        flash(f'{form.ID_number.data} successfully booked!', 'success')
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
    offender = User.query.filter_by(ID_number=ID_number).first()
    number_booked = User.query.filter_by(ID_number=ID_number).count()
    other_details = National.query.filter_by(user_id=ID_number).first()

    return render_template('display.html', offender=offender, number_booked=number_booked, other_details=other_details)


@app.route("/predict", methods=['POST', 'GET'])
def predict():
    title = "Predict  offender"
    return render_template('predict.html', title='profile')


@app.route("/show_prediction", methods=['GET', 'POST'])
def show_prediction():
    num = [int(x) for x in request.form.values()]
    value = [np.array(num)]
    prediction = model.predict(value)

    return render_template('show_prediction.html', prediction=prediction)


@app.route("/mail", methods=['POST', 'GET'])
def mail():
    title = "Message offender"
    return render_template('mail.html', title='profile')


@app.route("/send_mail", methods=['GET', 'POST'])
def send_mail():
    number = request.form.get("number")
    responseData = sms.send_message(
        {
            "from": "Traffic Management",
            "to": number,
            "text": "You have Violated traffic offense",
        }
    )

    if responseData["messages"][0]["status"] == "0":
        message = "Message sent successfully."
    else:
        message = f"Message failed with error: {responseData['messages'][0]['error-text']}"

    return render_template('send_mail.html', message=message)


@app.route("/report")
def report():
    con = sqlite3.connect("offender.db")
    df = pd.read_sql_query("SELECT * from User", con)

    df['Dates'] = pd.to_datetime(df['offense_date']).dt.date
    df['Time'] = pd.to_datetime(df['offense_date']).dt.time
    df['date'] = pd.to_datetime(df['Dates'])
    L = ['year', 'month', 'day']
    df = df.join(pd.concat([getattr(df['date'].dt, i).rename(i) for i in L], axis=1))
    df['number_booked'] = np.random.randint(18, 45, size=len(df))
    df = df.sort_values('month')
    df['month'] = df['month'].map({1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN', 7: 'JUL',
                                   8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'})

    top_month = df.year.value_counts()
    plt.figure(figsize=(10, 6))
    plt.title('Offense bar chart!')
    plt.xticks(rotation=75)
    plt.xlabel("Year")
    plt.ylabel("Total offender booked")
    sns.barplot(x=top_month.index, y=top_month)
    plt.savefig('static/images/plot3.png')

    top_month = df.month.value_counts()
    plt.figure(figsize=(10, 6))
    # plt.title('Offense bar chart!')
    plt.xticks(rotation=75)
    plt.xlabel("Month of the year")
    plt.ylabel("Total offender booked")
    sns.barplot(x=top_month.index, y=top_month)
    plt.savefig('static/images/plot2.png')

    return render_template('report.html', url='/static/images/plot2.png', url2='static/images/plot3.png')


@app.route("/booking", methods=['POST', 'GET'])
def booking():
    conn = sqlite3.connect('offender.db')
    cursor = conn.cursor()

    ID_number = request.form.get("ID_number")
    offense_date = request.form.get("offense_date")
    offense = request.form.get("offense")
    plate_number = request.form.get("plate_number")
    cursor.execute("""INSERT INTO book(ID_number, offense_date, offense, plate_number)  VALUES (?,?,?,?)""",
                   (ID_number, offense_date, offense, plate_number))
    conn.commit()
    flash(f'{ID_number} successfully booked!', 'success')
    return render_template('booking.html', title='Register')


@app.route("/show_booking", methods=['POST', 'GET'])
def show_booking():
    title = "  offender"
    return render_template('show_booking.html', title='profile')

if __name__ == '__main__':
    app.run(debug=True)
