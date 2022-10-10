import os
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

today = datetime.today()
the_year = today.year

app = Flask(__name__)

app.secret_key = os.environ.get('SERVER_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Message(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(250), unique=False, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(5000), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def root():
    return render_template('index.html', year=the_year)


@app.route('/about')
def about():
    return render_template('about.html', year=the_year)


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        new_message = Message(
            date=datetime.today(),
            name=request.form['name'],
            email=request.form['email'],
            message=request.form['message']
        )
        db.session.add(new_message)
        db.session.commit()
        return render_template('contact.html', year=the_year, sent=True)
    return render_template('contact.html', year=the_year, sent=False)


@app.route('/show/<image>.<ext>')
def display(image, ext):
    title = f'{image}.{ext}'
    img = f"/static/assets/img/screens/{image}.png"
    return render_template('display.html', render=img, tlt=title)


if __name__ == '__main__':
    app.run(debug=True)
