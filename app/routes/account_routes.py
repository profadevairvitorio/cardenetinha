from .dependencies import (
    Blueprint, render_template, flash, redirect, url_for, abort, request, 
    login_required, current_user, db, Account, Transaction, Category, 
    AccountForm, EditAccountForm, TransactionForm
)

account_bp = Blueprint('account', __name__)

@account_bp.route('/accounts')
@login_required
def accounts():
    user_accounts = Account.query.filter_by(user_id=current_user.id, is_active=True).all()
    return render_template('account/index.html', title='Suas Contas', accounts=user_accounts)


@account_bp.route('/account/new', methods=['GET', 'POST'])
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
        return redirect(url_for('account.accounts'))

    return render_template('account/new.html', title='Criar Nova Conta', form=form)


@account_bp.route('/account/edit/<int:account_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('account.accounts'))
    elif request.method == 'GET':
        form.name_account.data = account.name_account

    return render_template('account/edit.html', title='Editar Conta', form=form, account=account)


@account_bp.route('/account/disable/<int:account_id>')
@login_required
def disable_account(account_id):
    account = db.session.get(Account, account_id)
    if account is None or account.user_id != current_user.id:
        abort(404)

    account.is_active = False
    db.session.commit()
    flash('Conta desabilitada com sucesso!', 'info')
    return redirect(url_for('account.accounts'))


@account_bp.route('/account/<int:account_id>', methods=['GET', 'POST'])
@login_required
def account_detail(account_id):
    account = db.session.get(Account, account_id)
    if account is None or account.user_id != current_user.id:
        abort(404)

    form = TransactionForm(user=current_user)

    if form.validate_on_submit():
        try:
            category_id = form.category_id.data
            if form.new_category.data:
                new_category_name = form.new_category.data
                existing_category = Category.query.filter_by(name=new_category_name, user_id=current_user.id).first()
                if existing_category:
                    flash('Essa categoria já existe.', 'warning')
                    category_id = existing_category.id
                else:
                    new_category = Category(name=new_category_name, user_id=current_user.id)
                    db.session.add(new_category)
                    db.session.flush()
                    category_id = new_category.id
                    flash(f'Nova categoria "{new_category_name}" criada com sucesso!', 'success')

            new_transaction = Transaction(
                description=form.description.data,
                amount=form.amount.data,
                type=form.type.data,
                account_id=account.id,
                category_id=category_id
            )
            db.session.add(new_transaction)
            db.session.flush()
            db.session.commit()
            db.session.refresh(account)
            flash('Transação registrada com sucesso!', 'success')
            return redirect(url_for('account.account_detail', account_id=account.id))
        except ValueError as e:
            flash(str(e), 'danger')
            db.session.rollback()

    return render_template('account/detail.html', title=account.name_account, account=account, form=form)