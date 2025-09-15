# models.py

from main import db
from datetime import datetime

# Tabela auxiliar para a relação muitos-para-muitos entre User e Post (likes)
# Esta não é uma classe de modelo, mas uma tabela de associação.
likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

# Tabela: user
# Corresponde à classe User em Python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    sobrenome = db.Column(db.String(255), nullable=False)
    senha = db.Column(db.String(255), nullable=False) # Atenção: Lembre-se de hashear a senha!
    email = db.Column(db.String(255), unique=True, nullable=False)
    biografia = db.Column(db.Text, nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    data_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relação: Um usuário tem muitos posts.
    # O 'backref' cria um atributo 'author' no modelo Post para acessar o usuário autor do post.
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.nome}', '{self.email}')"

# Tabela: post
# Corresponde à classe Post em Python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    corpo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Chave estrangeira que liga o post ao seu autor (user).
    # 'user.id' refere-se à tabela 'user', coluna 'id'.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relação muitos-para-muitos: Um post pode ser curtido por muitos usuários.
    # 'secondary=likes' diz ao SQLAlchemy para usar nossa tabela de associação 'likes'.
    liked_by = db.relationship('User', secondary=likes, backref=db.backref('liked_posts', lazy='dynamic'))

    def __repr__(self):
        return f"Post('{self.titulo}', '{self.data_criacao}')"