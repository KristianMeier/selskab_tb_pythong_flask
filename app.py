from io import StringIO
from flask import Flask, render_template, request, make_response
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from pandas.core.frame import DataFrame
import psycopg2
import pandas as pd
from werkzeug.utils import send_file
import numpy as np

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

def load_acc_knowledge_table_into_dataframe_array():
    mycursor.execute("SELECT * from selskab;")
    df_db = DataFrame(mycursor.fetchall(), columns=['type', 'bilag', 'dato', 'tekst', 'konto', 'momskode'])
    
def clean_data_and_prepare_for_merge():
    df.dropna(how='all', axis=1, inplace=True)  # Delete empty columns (economic specific)
    df.columns = ['fKontonr', 'tekst', 'debet']
    df["tekst"] = df["tekst"].str.lower()  # Python seems to be case-sensitive from using join.
    df = df.replace(r'^\s*$', np.NaN, regex=True)  # converts empty values to NaN
    df.dropna(subset=['tekst', 'debet'], inplace=True)
    df.drop(df[(df['debet'] == 0) | (df['debet'] == '0,00')].index, inplace=True)
    df.drop(df[(df['debet'] == '0') | (df['debet'] == '-0')].index, inplace=True)
    df = df[~df['tekst'].str.endswith('i alt', 'oresultat')]

def merge_acc_knowledge_dataframe_with_csv_dataframe():
    df_m = pd.merge(df, df_db, on='tekst', how='left')
    df_m = df_m.assign(type="F", bilag=1)
    df_m.drop(df_m[(df_m['debet'] == 0)].index, inplace=True)  # Høker Bugfix 26/08. Undersøg.
    df_m.dropna(subset=['debet'], inplace=True)   # Høker Bugfix 26/08. Undersøg.
    df_m.drop('fKontonr', axis=1, inplace=True)
    df_m = df_m[['type', 'bilag', 'dato', 'tekst', 'konto', 'momskode', 'debet']]  # Sort rows for Meneto
    df_m = df_m.drop_duplicates()

def minPandaFunktion(df):
    load_acc_knowledge_table_into_dataframe_array()
    clean_data_and_prepare_for_merge()
    merge_acc_knowledge_dataframe_with_csv_dataframe()
    return df_m

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/minKonvertRute', methods=['POST'])
def minKonvFunktion():
    '''Indlæs CSV i Pandaframe'''
    minCsvVariabel = request.files.get('minInputFil') 
    df = pd.read_csv(minCsvVariabel, sep=';')
    
    '''Converter Input til Output'''
    df = minPandaFunktion(df)

    '''Download Csv'''
    mitOutput = StringIO()
    df.to_csv(mitOutput,index=False, sep=';')
    mitResp = Response(mitOutput.getvalue(), mimetype="text/csv")
    mitResp.headers["Content-Disposition"] = "attachment; filename=\"saaaldo.csv\""
    return mitResp

if __name__ == '__main__':
    app.run()
