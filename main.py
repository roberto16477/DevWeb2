from flask import Flask
from database import db
from flask_login import LoginManager

# Cria a instância da aplicação
app = Flask(__name__)

# --- Configurações ---
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil-de-adivinhar'
# Corrigindo o caminho para a pasta instance, que o Flask cria automaticamente
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Conecta a instância 'db' com a nossa aplicação 'app'
# Isso é feito DEPOIS de todas as configurações do app.
db.init_app(app)

# Criando e configurando o gerenciador de login
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Informa qual é a rota de login
login_manager.login_message_category = 'info' # Categoria da mensagem flash

#Agora que 'app' e 'db' estão totalmente configurados, podemos importar os arquivos que dependem deles sem causar um ciclo.
with app.app_context():
    from models import *

    # Esta função é usada pelo Flask-Login para recarregar o objeto do usuário, a partir do ID de usuário armazenado na sessão.
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes import * 

if __name__ == "__main__":
    app.run()