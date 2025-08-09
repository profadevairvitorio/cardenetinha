from .dependencies import (
    Blueprint, render_template, flash, redirect, url_for, request, 
    login_required, current_user, datetime, ReportForm
)
from flask import Response
from app.services.report_service import ReportService

report_bp = Blueprint('report', __name__)

@report_bp.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    form = ReportForm(user=current_user)
    page = request.args.get('page', 1, type=int)
    per_page = 10

    report_service = ReportService()

    if form.validate_on_submit():
        return redirect(url_for('report.report',
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
            return redirect(url_for('report.report'))
        except ValueError:
            flash('Formato de data ou conta inválido na URL.', 'warning')
            return redirect(url_for('report.report'))

    return render_template('report.html', title='Relatórios', form=form, results=results, totals=totals)


@report_bp.route('/report/download/csv')
@login_required
def download_report_csv():
    report_service = ReportService()

    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    account_id_str = request.args.get('account_id')

    if not all([start_date_str, end_date_str, account_id_str]):
        flash('Parâmetros inválidos para gerar o relatório.', 'danger')
        return redirect(url_for('report.report'))

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
        return redirect(url_for('report.report'))
    except ValueError:
        flash('Parâmetros inválidos na URL.', 'danger')
        return redirect(url_for('report.report'))