from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask_login import login_required, current_user

from app import db
from app.forms import AccountForm, EditAccountForm, TransactionForm
from app.models import Account, Transaction

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', title='Página Inicial')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    last_account = Account.query.filter_by(user_id=current_user.id, is_active=True).order_by(Account.id.desc()).first()
    return render_template('dashboard.html', title='Painel', last_account=last_account)


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

    form = TransactionForm()

    if form.validate_on_submit():
        try:
            new_transaction = Transaction(
                description=form.description.data,
                amount=form.amount.data,
                type=form.type.data,
                account_id=account.id
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