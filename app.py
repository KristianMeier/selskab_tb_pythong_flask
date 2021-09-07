from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2

app = Flask(__name__)

ENV = 'prod'  # Skift denne til f.eks. "Production". Ellers vil den lave DB på vores local host. Det fejler nok, hvis den ikke er åben.

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/lexus'  # user:pw@adress/dbNavn

    conn = psycopg2.connect(database="lexus", user="postgres", password="root", host="localhost")
    mycursor = conn.cursor()

else:
    app.debug = True
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgresql://hvaodzwnooceta:49698aa339a5e4a3ff8743ed59a43cab2baee8d3c1180bd2594a'\
                                     'c66cf8f9591c@ec2-34-249-247-7.eu-west-1.compute.amazonaws.com:5432/dc8mlg3f6b65g6'

    conn = psycopg2.connect(database="dc8mlg3f6b65g6",
                            user="hvaodzwnooceta",
                            password="49698aa339a5e4a3ff8743ed59a43cab2baee8d3c1180bd2594ac66cf8f9591c",
                            host="ec2-34-249-247-7.eu-west-1.compute.amazonaws.com")
    mycursor = conn.cursor()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'kal'  # Denne kan ændres til det TABELNAVN man ønsker
    id = db.Column(db.Integer, primary_key=True)
    kalorier = db.Column(db.Integer)
    dato = db.Column(db.Date, default=datetime.now().date())

    def __init__(self, kalorier):
        self.kalorier = kalorier  # ID og dato kommer auto (default og au)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/min_data')
def min_data():
    mycursor.execute("SELECT * from mytable limit 10;")
    data = mycursor.fetchall()
    return render_template('min_data.html', data=data)


@app.route('/min_data')
def min_data2():
    mycursor.execute("SELECT * from TB_Dinero6 limit 10;")
    data2 = mycursor.fetchall()
    return render_template('min_data.html', data=data2)


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        kalorier = request.form['kalorier']  # id kommer fra autoincrement og dato fra default value.
        if kalorier == '':
            return render_template('index.html')
            #  Ovenstående 2 linjer fungerer ikke. Jeg har sat default checked på radiobuttons, så det ikke fejler når der submittets tom værdi.
        if db.session.query(Feedback):
            data = Feedback(kalorier)
            db.session.add(data)
            db.session.commit()
            return render_template('index.html')


if __name__ == '__main__':
    app.run()
