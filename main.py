from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# pip install -r requirements.txt

from os import name
app = Flask (__name__)

# 1. Define o caminho para o arquivo do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

# 2. Desativa uma funcionalidade do SQLAlchemy que emite avisos (não vou usar)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Cria a instância do banco de dados, ligando-a ao nosso app.
db = SQLAlchemy(app)

from models import *
from routes import *

if __name__ == "__main__":
    app.run()