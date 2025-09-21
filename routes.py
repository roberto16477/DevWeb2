from flask import render_template, url_for, flash, redirect, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from main import app
from database import db
from models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from forms import RegistrationForm, LoginForm, UpdateProfileForm, PostForm


#rotas
@app.route("/")
def index():
    # url_for('login') encontra a URL da função chamada 'login'.
    return redirect(url_for('login'))

@app.route("/home")
def homepage():
    # Busca todos os posts no banco de dados, ordenando pelos mais recentes
    posts = Post.query.order_by(Post.data_criacao.desc()).all()
    # Passa a lista de posts para o template
    return render_template('homepage.html', title='Página Inicial', posts=posts)

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
        
        # Redireciona o usuário para a página de login
        return redirect(url_for('login')) 
    
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
    return redirect(url_for('login'))

@app.route("/perfil", methods=['GET', 'POST'])
@login_required # Protege a rota, só usuários logados podem acessar
def perfil():
    form = UpdateProfileForm()
    # Se o formulário for enviado e validado
    if form.validate_on_submit():
        current_user.nome = form.nome.data
        current_user.sobrenome = form.sobrenome.data
        current_user.email = form.email.data
        current_user.biografia = form.biografia.data
        db.session.commit()
        return redirect(url_for('perfil'))
    # Se for a primeira vez que a página é carregada
    elif request.method == 'GET':
        form.nome.data = current_user.nome
        form.sobrenome.data = current_user.sobrenome
        form.email.data = current_user.email
        form.biografia.data = current_user.biografia
    return render_template('perfil.html', title='Meu Perfil', form=form)

@app.route('/delete_profile', methods=['POST'])
@login_required
def delete_profile():
    # Pega o usuário que está logado no momento
    user_to_delete = User.query.get(current_user.id)
    
    # Faz o logout do usuário para invalidar a sessão
    logout_user()
    
    # Apaga o usuário do banco de dados
    db.session.delete(user_to_delete)
    db.session.commit()
    
    # Redireciona para a página principal
    return redirect(url_for('index'))

@app.route("/post/new", methods=['GET', 'POST'])
@login_required # Apenas usuários logados podem criar posts
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # Cria um novo post com os dados do formulário e o autor logado
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        # Redireciona para a homepage para ver o novo post
        return redirect(url_for('homepage'))
    return render_template('create_post.html', title='Novo Post', form=form)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    # Busca o post pelo ID ou retorna um erro 404 (Não Encontrado) se não existir
    post = Post.query.get_or_404(post_id)
    
    # VERIFICAÇÃO DE SEGURANÇA:
    # Se o autor do post for diferente do usuário logado, exibe um erro 403 (Proibido)
    if post.author != current_user:
        abort(403)
        
    form = PostForm()
    # Se o formulário for enviado e validado
    if form.validate_on_submit():
        post.titulo = form.titulo.data
        post.corpo = form.corpo.data
        db.session.commit() # Não precisa de 'add', pois o post já está no banco
        return redirect(url_for('homepage'))
    # Se for a primeira vez que a página é carregada (GET)
    elif request.method == 'GET':
        # Preenche o formulário com os dados atuais do post
        form.titulo.data = post.titulo
        form.corpo.data = post.corpo
        
    # Usa o mesmo template de criação, mas passa uma legenda diferente
    return render_template('create_post.html', title='Editar Post',
                           form=form, legend='Editar Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    # Busca o post pelo ID ou retorna um erro 404 se não existir
    post = Post.query.get_or_404(post_id)
    
    # VERIFICAÇÃO DE SEGURANÇA:
    # Garante que o usuário logado é o autor do post
    if post.author != current_user:
        abort(403) # Erro de 'Proibido'
        
    # Apaga o post do banco de dados
    db.session.delete(post)
    db.session.commit()
    
    # Redireciona de volta para a homepage
    return redirect(url_for('homepage'))