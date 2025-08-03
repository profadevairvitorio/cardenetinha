from flask import Blueprint, render_template, flash, redirect, url_for, abort, request, make_response, Response
from flask_login import login_required, current_user
from sqlalchemy import func, extract, or_, case

from app.forms import *
from app.models import *
from app.services.report_service import ReportService

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

    global_balance = 0
    if account_id:
        account = db.session.get(Account, account_id)
        if account and account.user_id == current_user.id:
            global_balance = account.balance
    else:
        total_balance_query = db.session.query(func.sum(Account.balance)).filter(
            Account.user_id == current_user.id, Account.is_active == True
        )
        total_balance = total_balance_query.scalar() or 0
        global_balance = total_balance

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
        selected_account_id=account_id,
        global_balance=global_balance
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
    search_query = request.args.get('search', '')
    category_id = request.args.get('category_id', type=int)
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    query = Transaction.query.filter_by(account_id=account.id)

    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            or_(
                Transaction.description.ilike(search_term),
                func.cast(Transaction.amount, db.String).ilike(search_term),
                func.strftime('%Y-%m-%d', Transaction.date).ilike(search_term)
            )
        )

    if category_id:
        query = query.filter(Transaction.category_id == category_id)

    if start_date:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        query = query.filter(Transaction.date >= start_date_obj)

    if end_date:
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        query = query.filter(Transaction.date <= end_date_obj)

    transactions = query.order_by(Transaction.date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()

    return render_template(
        'transaction/history.html',
        title=f'Histórico de Transações - {account.name_account}',
        account=account,
        transactions=transactions,
        search_query=search_query,
        categories=categories,
        selected_category_id=category_id,
        start_date=start_date,
        end_date=end_date
    )


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


@main_bp.route('/perfil')
@login_required
def perfil():
    return render_template('perfil/index.html', title='Seu Perfil')


@main_bp.route('/perfil/edit', methods=['GET', 'POST'])
@login_required
def edit_perfil():
    form = UpdateProfileForm(original_username=current_user.username, original_email=current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash('Seu perfil foi atualizado com sucesso!', 'success')
        return redirect(url_for('main.perfil'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('perfil/edit.html', title='Editar Perfil', form=form)





@main_bp.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    form = ReportForm(user=current_user)
    page = request.args.get('page', 1, type=int)
    per_page = 10

    report_service = ReportService()

    if form.validate_on_submit():
        return redirect(url_for('main.report',
                                start_date=form.start_date.data.strftime('%Y-%m-%d'),
                                end_date=form.end_date.data.strftime('%Y-%m-%d'),
                                account_id=form.account.data,
                                page=1))

    results = None
    totals = {}
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    account_id_str = request.args.get('account_id')

    if start_date_str and end_date_str and account_id_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            account_id = int(account_id_str)
            form.start_date.data = start_date
            form.end_date.data = end_date
            form.account.data = account_id

            report_data = report_service.generate_report_data(
                user_id=current_user.id,
                start_date=start_date,
                end_date=end_date,
                account_id=account_id,
                page=page,
                per_page=per_page
            )
            results = report_data.get('results')
            totals = report_data.get('totals', {})

        except report_service.AuthorizationError:
            flash('Acesso negado. A conta solicitada não é válida ou não pertence a você.', 'danger')
            return redirect(url_for('main.report'))
        except ValueError:
            flash('Formato de data ou conta inválido na URL.', 'warning')
            return redirect(url_for('main.report'))

    return render_template('report.html', title='Relatórios', form=form, results=results, totals=totals)


@main_bp.route('/report/download/csv')
@login_required
def download_report_csv():
    report_service = ReportService()

    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    account_id_str = request.args.get('account_id')

    if not all([start_date_str, end_date_str, account_id_str]):
        flash('Parâmetros inválidos para gerar o relatório.', 'danger')
        return redirect(url_for('main.report'))

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        account_id = int(account_id_str)

        csv_data = report_service.generate_csv_report(
            user_id=current_user.id,
            start_date=start_date,
            end_date=end_date,
            account_id=account_id
        )

        return Response(
            csv_data,
            mimetype="text/csv",
            headers={
                "Content-Disposition": f"attachment;filename=relatorio_{start_date_str}_a_{end_date_str}.csv"
            }
        )

    except report_service.AuthorizationError:
        flash('Acesso negado. A conta solicitada não é válida ou não pertence a você.', 'danger')
        return redirect(url_for('main.report'))
    except ValueError:
        flash('Parâmetros inválidos na URL.', 'danger')
        return redirect(url_for('main.report'))