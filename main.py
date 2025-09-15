from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# pip install -r requirements.txt

from os import name
app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import *
from routes import *
    
if __name__ == "__main__":
    app.run()