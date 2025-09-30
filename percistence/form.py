from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


db = SQLAlchemy()

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    date = db.Column(db.Date, default=datetime.today)
    acceptPolitic = db.Column(db.Boolean, default=False)