#!/bin/bash

APP_NAME="meu_app_flask"

echo "Criando a estrutura para o projeto '$APP_NAME'..."

mkdir -p "$APP_NAME/app/templates"
mkdir -p "$APP_NAME/app/static/css"


cat << EOF > "$APP_NAME/run.py"
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
EOF

cat << EOF > "$APP_NAME/requirements.txt"
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.1
Flask-Login==0.6.3
Werkzeug==3.0.3
email-validator==2.2.0
EOF

cat << EOF > "$APP_NAME/.gitignore"
venv/
*.pyc
__pycache__/
.env
instance/
EOF

cat << EOF > "$APP_NAME/README.md"
# Meu App Flask com Login

Este é um projeto Flask básico que inclui um sistema de autenticação de usuários (registro, login, logout) usando SQLite.

## Como Iniciar

1.  **Crie e ative um ambiente virtual:**
    \`\`\`bash
    python3 -m venv venv
    source venv/bin/activate
    \`\`\`
    *(No Windows, use: \`venv\\Scripts\\activate\`)*

2.  **Instale as dependências:**
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`

3.  **Execute a aplicação:**
    \`\`\`bash
    python run.py
    \`\`\`
    *O banco de dados \`site.db\` será criado automaticamente no primeiro acesso.*

4.  **Acesse no seu navegador:** \`http://127.0.0.1:5000/\`
EOF


cat << EOF > "$APP_NAME/app/__init__.py"
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inicializa as extensões
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

def create_app():
    """Cria e configura uma instância da aplicação Flask."""
    app = Flask(__name__, instance_relative_config=True)

    # Carrega a configuração
    app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil-de-adivinhar'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa as extensões com a aplicação
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import routes
        from . import auth
        from . import models

        # Registra os Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        # Cria as tabelas do banco de dados se não existirem
        db.create_all()

    return app
EOF

cat << EOF > "$APP_NAME/app/models.py"
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

class User(UserMixin, db.Model):
    """Modelo de Usuário"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        """Cria o hash da senha."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    """Carrega o usuário a partir do ID da sessão."""
    return User.query.get(int(user_id))
EOF

cat << EOF > "$APP_NAME/app/forms.py"
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import User

class LoginForm(FlaskForm):
    """Formulário de Login"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    """Formulário de Registro"""
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nome de usuário já está em uso. Por favor, escolha outro.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já está registrado. Por favor, use outro.')
EOF

cat << EOF > "$APP_NAME/app/routes.py"
from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', title='Página Inicial')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Painel')
EOF

cat << EOF > "$APP_NAME/app/auth.py"
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm, RegistrationForm
from .models import User
from . import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login falhou. Verifique seu email e senha.', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Sua conta foi criada! Você já pode fazer login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Registrar', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('main.index'))
EOF


cat << EOF > "$APP_NAME/app/templates/base.html"
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Meu App Flask</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <nav>
            <a href="{{ url_for('main.index') }}" class="nav-brand">Meu App</a>
            <div class="nav-links">
                {% if current_user.is_authenticated %}
                    <a href="{{ url_for('main.dashboard') }}">Painel</a>
                    <a href="{{ url_for('auth.logout') }}">Sair</a>
                {% else %}
                    <a href="{{ url_for('auth.login') }}">Login</a>
                    <a href="{{ url_for('auth.register') }}">Registrar</a>
                {% endif %}
            </div>
        </nav>
    </header>
    <main>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </main>
</body>
</html>
EOF

cat << EOF > "$APP_NAME/app/templates/index.html"
{% extends "base.html" %}
{% block content %}
    <div class="container">
        <h1>Bem-vindo ao Meu App Flask!</h1>
        <p>Este é um projeto inicial com sistema de login.</p>
        <p>Use a navegação para fazer login ou se registrar.</p>
    </div>
{% endblock %}
EOF

cat << EOF > "$APP_NAME/app/templates/login.html"
{% extends "base.html" %}
{% block content %}
    <div class="form-container">
        <h2>Login</h2>
        <form method="POST" action="">
            {{ form.hidden_tag() }}
            <div class="form-group">
                {{ form.email.label }}
                {{ form.email(class="form-control") }}
                {% for error in form.email.errors %}
                    <span class="error-text">[{{ error }}]</span>
                {% endfor %}
            </div>
            <div class="form-group">
                {{ form.password.label }}
                {{ form.password(class="form-control") }}
                {% for error in form.password.errors %}
                    <span class="error-text">[{{ error }}]</span>
                {% endfor %}
            </div>
            <div class="form-group checkbox">
                {{ form.remember_me() }} {{ form.remember_me.label }}
            </div>
            <div class="form-group">
                {{ form.submit(class="btn") }}
            </div>
        </form>
        <p>Não tem uma conta? <a href="{{ url_for('auth.register') }}">Registre-se aqui</a></p>
    </div>
{% endblock %}
EOF

cat << EOF > "$APP_NAME/app/templates/register.html"
{% extends "base.html" %}
{% block content %}
    <div class="form-container">
        <h2>Registrar</h2>
        <form method="POST" action="">
            {{ form.hidden_tag() }}
            <div class="form-group">
                {{ form.username.label }}
                {{ form.username(class="form-control") }}
                {% for error in form.username.errors %}
                    <span class="error-text">[{{ error }}]</span>
                {% endfor %}
            </div>
            <div class="form-group">
                {{ form.email.label }}
                {{ form.email(class="form-control") }}
                 {% for error in form.email.errors %}
                    <span class="error-text">[{{ error }}]</span>
                {% endfor %}
            </div>
            <div class="form-group">
                {{ form.password.label }}
                {{ form.password(class="form-control") }}
                {% for error in form.password.errors %}
                    <span class="error-text">[{{ error }}]</span>
                {% endfor %}
            </div>
            <div class="form-group">
                {{ form.confirm_password.label }}
                {{ form.confirm_password(class="form-control") }}
                {% for error in form.confirm_password.errors %}
                    <span class="error-text">[{{ error }}]</span>
                {% endfor %}
            </div>
            <div class="form-group">
                {{ form.submit(class="btn") }}
            </div>
        </form>
        <p>Já tem uma conta? <a href="{{ url_for('auth.login') }}">Faça login aqui</a></p>
    </div>
{% endblock %}
EOF

# app/templates/dashboard.html: Página protegida
cat << EOF > "$APP_NAME/app/templates/dashboard.html"
{% extends "base.html" %}
{% block content %}
    <div class="container">
        <h1>Painel do Usuário</h1>
        <h2>Olá, {{ current_user.username }}!</h2>
        <p>Esta é uma página protegida, visível apenas para usuários logados.</p>
        <p>Seu email registrado é: {{ current_user.email }}</p>
    </div>
{% endblock %}
EOF


cat << EOF > "$APP_NAME/app/static/css/style.css"
body {
    font-family: Arial, sans-serif; margin: 0; background-color: #f4f4f4; color: #333;
}
main { padding-top: 20px; }
nav {
    background-color: #333; color: white; padding: 1rem; display: flex; justify-content: space-between; align-items: center;
}
nav a { color: white; text-decoration: none; margin: 0 10px; }
nav a.nav-brand { font-weight: bold; font-size: 1.2rem; }
.container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; }
.form-container { max-width: 400px; margin: auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
.form-group { margin-bottom: 15px; }
.form-group label { display: block; margin-bottom: 5px; }
.form-control { width: 95%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
.checkbox { display: flex; align-items: center; }
.checkbox input { margin-right: 5px; }
.btn {
    background-color: #5cb85c; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; width: 100%; font-size: 1rem;
}
.btn:hover { background-color: #4cae4c; }
.error-text { color: red; font-size: 0.8em; }
.alert { padding: 15px; margin: 20px auto; border: 1px solid transparent; border-radius: 4px; max-width: 800px; }
.alert-success { color: #155724; background-color: #d4edda; border-color: #c3e6cb; }
.alert-danger { color: #721c24; background-color: #f8d7da; border-color: #f5c6cb; }
.alert-info { color: #0c5460; background-color: #d1ecf1; border-color: #bee5eb; }
EOF

echo ""
echo "Projeto '$APP_NAME' criado com sucesso!"
echo ""
echo "Para começar, acesse o diretório do projeto:"
echo "   cd $APP_NAME"
echo ""
echo "Siga as instruções no arquivo README.md para rodar a aplicação."