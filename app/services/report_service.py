import io
import csv
from sqlalchemy import func, case, desc
from .. import db
from ..models import Account, Category, Transaction

class ReportService:
    """
    A service class for generating financial reports.
    """
    class AuthorizationError(Exception):
        """Custom exception for report authorization failures."""
        pass

    def _authorize_report_access(self, user_id, account_id):
        if account_id != 0:
            is_valid_account = db.session.query(Account.id).filter_by(
                id=account_id,
                user_id=user_id
            ).first()
            if not is_valid_account:
                raise self.AuthorizationError("User does not have permission to access this account.")

    def _build_report_query(self, user_id, start_date, end_date, account_id):
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

    def _build_csv_query(self, user_id, start_date, end_date, account_id):
        query = db.session.query(
            Category.name,
            func.sum(case((Transaction.type == 'entrada', Transaction.amount), else_=0)).label('total_entrada'),
            func.sum(case((Transaction.type == 'saida', Transaction.amount), else_=0)).label('total_saida')
        ).join(Transaction.category).join(Account).filter(
            Account.user_id == user_id,
            Transaction.date.between(start_date, end_date)
        )
        if account_id != 0:
            query = query.filter(Account.id == account_id)
        return query.group_by(Category.name).order_by(Category.name)

    def _format_results_to_csv(self, results):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Categoria', 'Total Entrada (R$)', 'Total Saída (R$)', 'Balanço (R$)'])
        for r in results:
            balance = (r.total_entrada or 0) - (r.total_saida or 0)
            writer.writerow([
                r.name,
                f'{r.total_entrada or 0:.2f}',
                f'{r.total_saida or 0:.2f}',
                f'{balance:.2f}'
            ])
        return output.getvalue()

    def _calculate_report_totals(self, all_results):
        total_entrada = sum(r.total_entrada for r in all_results if r.total_entrada)
        total_saida = sum(r.total_saida for r in all_results if r.total_saida)
        return {
            'total_entrada': total_entrada,
            'total_saida': total_saida,
            'balance': total_entrada - total_saida
        }

    def generate_report_data(self, user_id, start_date, end_date, account_id, page, per_page):
        self._authorize_report_access(user_id, account_id)
        results_query = self._build_report_query(user_id, start_date, end_date, account_id)
        paginated_results = results_query.paginate(page=page, per_page=per_page, error_out=False)
        all_results = results_query.all()
        totals = self._calculate_report_totals(all_results)
        return {'results': paginated_results, 'totals': totals}

    def generate_csv_report(self, user_id, start_date, end_date, account_id):
        self._authorize_report_access(user_id, account_id)
        query = self._build_csv_query(user_id, start_date, end_date, account_id)
        results = query.all()
        csv_data = self._format_results_to_csv(results)
        return csv_data
