from .dependencies import (
    Blueprint, render_template, request, abort, login_required, current_user, db,
    datetime, Transaction, Account, Category
)
from sqlalchemy import or_, func

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/account/<int:account_id>/transactions')
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