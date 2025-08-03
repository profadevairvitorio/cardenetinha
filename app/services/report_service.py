from sqlalchemy import func, case, desc
from .. import db
from ..models import Account, Category, Transaction


class ReportAuthorizationError(Exception):
    """Custom exception for report authorization failures."""
    pass


def _authorize_report_access(user_id, account_id):
    if account_id != 0:
        is_valid_account = db.session.query(Account.id).filter_by(
            id=account_id,
            user_id=user_id
        ).first()
        if not is_valid_account:
            raise ReportAuthorizationError("User does not have permission to access this account.")


def _build_report_query(user_id, start_date, end_date, account_id):
    total_entrada_expr = func.sum(case((Transaction.type == 'entrada', Transaction.amount), else_=0))
    total_saida_expr = func.sum(case((Transaction.type == 'saida', Transaction.amount), else_=0))

    query = db.session.query(
        Category.name,
        total_entrada_expr.label('total_entrada'),
        total_saida_expr.label('total_saida')
    ).join(Transaction.category).join(Account).filter(
        Account.user_id == user_id,
        Transaction.date.between(start_date, end_date)
    )

    if account_id != 0:
        query = query.filter(Account.id == account_id)

    return query.group_by(Category.name) \
        .having(total_entrada_expr + total_saida_expr > 0) \
        .order_by(desc(total_entrada_expr + total_saida_expr))


def _calculate_report_totals(all_results):
    total_entrada = sum(r.total_entrada for r in all_results if r.total_entrada)
    total_saida = sum(r.total_saida for r in all_results if r.total_saida)

    return {
        'total_entrada': total_entrada,
        'total_saida': total_saida,
        'balance': total_entrada - total_saida
    }


def generate_report_data(user_id, start_date, end_date, account_id, page, per_page):
    _authorize_report_access(user_id, account_id)

    results_query = _build_report_query(user_id, start_date, end_date, account_id)

    paginated_results = results_query.paginate(page=page, per_page=per_page, error_out=False)

    all_results = results_query.all()
    totals = _calculate_report_totals(all_results)

    return {'results': paginated_results, 'totals': totals}
