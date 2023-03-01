from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store_monitoring.db'
db = SQLAlchemy(app)

class StoreStatus(db.Model):
    store_id = db.Column(db.String(10), primary_key=True)
    timestamp_utc = db.Column(db.DateTime, primary_key=True)
    status = db.Column(db.String(10))

class BusinessHours(db.Model):
    store_id = db.Column(db.String(10), primary_key=True)
    day_of_week = db.Column(db.Integer, primary_key=True)
    start_time_local = db.Column(db.Time)
    end_time_local = db.Column(db.Time)

class Timezone(db.Model):
    store_id = db.Column(db.String(10), primary_key=True)
    timezone_str = db.Column(db.String(50))

# Load data from CSVs
store_status_df = pd.read_csv('store_status.csv')
store_status_df['timestamp_utc'] = pd.to_datetime(store_status_df['timestamp_utc'])
store_status_df.to_sql('store_status', db.engine, if_exists='replace', index=False)

business_hours_df = pd.read_csv('business_hours.csv')
business_hours_df['start_time_local'] = pd.to_datetime(business_hours_df['start_time_local']).dt.time
business_hours_df['end_time_local'] = pd.to_datetime(business_hours_df['end_time_local']).dt.time
business_hours_df.to_sql('business_hours', db.engine, if_exists='replace', index=False)

timezone_df = pd.read_csv('timezone.csv')
timezone_df.to_sql('timezone', db.engine, if_exists='replace', index=False)

db.create_all()
