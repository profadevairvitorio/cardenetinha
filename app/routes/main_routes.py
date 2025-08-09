from .dependencies import (
    Blueprint, render_template, request, login_required, current_user, db,
    datetime, Account, Category, Transaction
)
from sqlalchemy import func, extract

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