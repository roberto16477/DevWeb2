# main.py

from flask import Flask
# 1. Importe o 'db' do nosso novo arquivo
from database import db

# Cria a instância da aplicação
app = Flask(__name__)

# --- Configurações ---
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil-de-adivinhar'
# Corrigindo o caminho para a pasta instance, que o Flask cria automaticamente
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. Conecta a instância 'db' com a nossa aplicação 'app'
#    Isso é feito DEPOIS de todas as configurações do app.
db.init_app(app)

# 3. Agora que 'app' e 'db' estão totalmente configurados, podemos importar
#    os arquivos que dependem deles sem causar um ciclo.
with app.app_context():
    from models import *
    from routes import *
    # Se precisar criar as tabelas aqui (opcional)
    # db.create_all() 

if __name__ == "__main__":
    app.run()