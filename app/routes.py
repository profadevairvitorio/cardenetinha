from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask_login import login_required, current_user
from sqlalchemy import func, extract
from datetime import datetime

from app import db
from app.forms import AccountForm, EditAccountForm, TransactionForm, CategoryForm
from app.models import Account, Transaction, Category

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', title='Página Inicial')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    month = request.args.get('month', current_month, type=int)
    year = request.args.get('year', current_year, type=int)
    account_id = request.args.get('account_id', type=int)

    accounts = Account.query.filter_by(user_id=current_user.id, is_active=True).all()

    query = db.session.query(
        Category.name,
        Transaction.type,
        func.sum(Transaction.amount).label('total_amount')
    ).join(Transaction.category).join(Account).filter(
        Account.user_id == current_user.id,
        extract('month', Transaction.date) == month,
        extract('year', Transaction.date) == year
    )

    if account_id:
        query = query.filter(Account.id == account_id)

    transactions = query.group_by(Category.name, Transaction.type).all()

    income_by_category = {}
    expenses_by_category = {}
    total_income = 0
    total_expenses = 0

    for category_name, trans_type, total_amount in transactions:
        if trans_type == 'entrada':
            income_by_category[category_name] = total_amount
            total_income += total_amount
        elif trans_type == 'saida':
            expenses_by_category[category_name] = total_amount
            total_expenses += total_amount

    return render_template(
        'dashboard.html',
        title='Dashboard',
        income_by_category=income_by_category,
        expenses_by_category=expenses_by_category,
        total_income=total_income,
        total_expenses=total_expenses,
        month=month,
        year=year,
        accounts=accounts,
        selected_account_id=account_id
    )


@main_bp.route('/accounts')
@login_required
def accounts():
    user_accounts = Account.query.filter_by(user_id=current_user.id, is_active=True).all()
    return render_template('account/index.html', title='Suas Contas', accounts=user_accounts)


@main_bp.route('/account/new', methods=['GET', 'POST'])
@login_required
def new_account():
    form = AccountForm()
    if form.validate_on_submit():
        new_account = Account(
            name_account=form.name_account.data,
            balance=form.initial_balance.data,
            user_id=current_user.id
        )

        db.session.add(new_account)
        db.session.commit()

        flash(f"Conta '{form.name_account.data}' criada com sucesso!", 'success')
        return redirect(url_for('main.accounts'))

    return render_template('account/new.html', title='Criar Nova Conta', form=form)


@main_bp.route('/account/edit/<int:account_id>', methods=['GET', 'POST'])
@login_required
def edit_account(account_id):
    account = db.session.get(Account, account_id)
    if account is None or account.user_id != current_user.id:
        abort(404)

    form = EditAccountForm()
    if form.validate_on_submit():
        account.name_account = form.name_account.data
        db.session.commit()
        flash('Conta atualizada com sucesso!', 'success')
        return redirect(url_for('main.accounts'))
    elif request.method == 'GET':
        form.name_account.data = account.name_account

    return render_template('account/edit.html', title='Editar Conta', form=form, account=account)


@main_bp.route('/account/disable/<int:account_id>')
@login_required
def disable_account(account_id):
    account = db.session.get(Account, account_id)
    if account is None or account.user_id != current_user.id:
        abort(404)

    account.is_active = False
    db.session.commit()
    flash('Conta desabilitada com sucesso!', 'info')
    return redirect(url_for('main.accounts'))


@main_bp.route('/account/<int:account_id>', methods=['GET', 'POST'])
@login_required
def account_detail(account_id):
    account = db.session.get(Account, account_id)
    if account is None or account.user_id != current_user.id:
        abort(404)

    form = TransactionForm(user=current_user)

    if form.validate_on_submit():
        try:
            new_transaction = Transaction(
                description=form.description.data,
                amount=form.amount.data,
                type=form.type.data,
                account_id=account.id,
                category_id=form.category_id.data
            )
            db.session.add(new_transaction)
            db.session.flush()
            db.session.commit()
            db.session.refresh(account)
            flash('Transação registrada com sucesso!', 'success')
            return redirect(url_for('main.account_detail', account_id=account.id))
        except ValueError as e:
            flash(str(e), 'danger')
            db.session.rollback()

    return render_template('account/detail.html', title=account.name_account, account=account, form=form)


@main_bp.route('/account/<int:account_id>/transactions')
@login_required
def transaction_history(account_id):
    account = db.session.get(Account, account_id)
    if account is None or account.user_id != current_user.id:
        abort(404)

    page = request.args.get('page', 1, type=int)
    per_page = 10
    transactions = Transaction.query.filter_by(account_id=account.id).order_by(Transaction.date.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('transaction/history.html', title=f'Histórico de Transações - {account.name_account}', account=account, transactions=transactions)


@main_bp.route('/categories')
@login_required
def categories():
    user_categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()
    return render_template('category/index.html', title='Gerenciar Categorias', categories=user_categories)


@main_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm(user_id=current_user.id)
    if form.validate_on_submit():
        new_category = Category(name=form.name.data, user_id=current_user.id)
        db.session.add(new_category)
        db.session.commit()
        flash('Categoria criada com sucesso!', 'success')
        return redirect(url_for('main.categories'))
    return render_template('category/new.html', title='Nova Categoria', form=form)


@main_bp.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = db.session.get(Category, category_id)
    if category is None or category.user_id != current_user.id:
        abort(404)

    form = CategoryForm(original_name=category.name, user_id=current_user.id)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('main.categories'))
    elif request.method == 'GET':
        form.name.data = category.name

    return render_template('category/edit.html', title='Editar Categoria', form=form, category=category)