from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/min_data')
def min_data():
    mycursor.execute("SELECT * from mytable limit 10;")
    data = mycursor.fetchall()
    return render_template('min_data.html', data=data)

@app.route('/min_data2')
def min_data2():
    mycursor.execute("SELECT * from din limit 10;")
    data2 = mycursor.fetchall()
    return render_template('min_data2.html', data=data2)

if __name__ == '__main__':
    app.run()
