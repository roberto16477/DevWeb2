from flask import render_template, url_for, flash, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash
from main import app
from database import db
from models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from forms import RegistrationForm, LoginForm


#rotas
@app.route("/")
def index():
    # url_for('login') encontra a URL da função chamada 'login'.
    return redirect(url_for('login'))

@app.route("/home")
def homepage():
    # A sua antiga homepage agora vive exclusivamente na rota /home.
    return render_template('homepage.html', title='Página Inicial')

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

@app.route("/login", methods=['GET', 'POST'])
def login():
    # Se o usuário já estiver logado, redireciona para a homepage
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Busca o usuário no banco de dados pelo email
        user = User.query.filter_by(email=form.email.data).first()
        
        # Verifica se o usuário existe e se a senha está correta
        if user and check_password_hash(user.senha, form.senha.data):
            login_user(user, remember=form.lembrar_me.data)
            flash('Login realizado com sucesso!', 'success')
            # Redireciona para a página que o usuário tentava acessar, ou para a homepage
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('homepage'))
        else:
            flash('Login sem sucesso. Por favor, verifique o email e a senha.', 'danger')
            
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))
