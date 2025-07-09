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
