from flask import render_template, url_for, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from main import app
from database import db
from models import User, Post
from forms import RegistrationForm # Importe seu novo formulário


#rotas
@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/blog")
def blog():
    return "bem vindo ao blog"

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # Se o formulário for enviado e for válido...
    if form.validate_on_submit():
        # Criptografa a senha antes de salvar
        hashed_password = generate_password_hash(form.senha.data)
        
        # Cria um novo usuário com os dados do formulário
        user = User(nome=form.nome.data,
                    sobrenome=form.sobrenome.data,
                    email=form.email.data, 
                    senha=hashed_password)
        
        # Adiciona o novo usuário ao banco de dados
        db.session.add(user)
        db.session.commit()
        
        # Mostra uma mensagem de sucesso
        flash(f'Conta criada com sucesso para {form.nome.data}!', 'success')
        
        # Redireciona o usuário para a página de login (ou outra página)
        return redirect(url_for('homepage')) # Supondo que você tenha uma rota 'homepage'
    
    # Se for a primeira vez que o usuário acessa a página (GET), apenas mostra o formulário
    return render_template('register.html', title='Registrar', form=form)
