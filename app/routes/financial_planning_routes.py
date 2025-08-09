from .dependencies import (
    Blueprint, render_template, flash, redirect, url_for, abort, request, 
    login_required, current_user, db, datetime, FinancialPlan, FinancialPlanForm
)
from sqlalchemy import extract

financial_planning_bp = Blueprint('financial_planning', __name__)

@financial_planning_bp.route('/financial-planning/edit/<int:item_id>', methods=['POST'])
@login_required
def edit_plan_item(item_id):
    item = db.session.get(FinancialPlan, item_id)
    if item is None or item.user_id != current_user.id:
        abort(404)
    form = FinancialPlanForm(user=current_user)
    if form.validate_on_submit():
        item.description = form.description.data
        item.amount = form.amount.data
        item.type = form.type.data
        item.plan_date = form.plan_date.data
        item.category_id = form.category_id.data
        db.session.commit()
        flash('Item do planejamento atualizado com sucesso!', 'success')
    else:
        flash('Ocorreu um erro ao atualizar o item.', 'danger')
    return redirect(url_for('financial_planning.financial_planning'))


@financial_planning_bp.route('/financial-planning/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_plan_item(item_id):
    item = db.session.get(FinancialPlan, item_id)
    if item is None or item.user_id != current_user.id:
        abort(404)
    db.session.delete(item)
    db.session.commit()
    flash('Item do planejamento excluído com sucesso!', 'success')
    return redirect(url_for('financial_planning.financial_planning'))


@financial_planning_bp.route('/financial-planning', methods=['GET', 'POST'])
@login_required
def financial_planning():
    form = FinancialPlanForm(user=current_user)
    if form.validate_on_submit():
        new_plan_item = FinancialPlan(
            description=form.description.data,
            amount=form.amount.data,
            type=form.type.data,
            plan_date=form.plan_date.data,
            category_id=form.category_id.data,
            user_id=current_user.id
        )
        db.session.add(new_plan_item)
        db.session.commit()
        flash('Item adicionado ao planejamento com sucesso!', 'success')
        return redirect(url_for('financial_planning.financial_planning'))

    month = request.args.get('month', datetime.utcnow().month, type=int)
    year = request.args.get('year', datetime.utcnow().year, type=int)

    base_query = FinancialPlan.query.filter(
        FinancialPlan.user_id == current_user.id,
        extract('month', FinancialPlan.plan_date) == month,
        extract('year', FinancialPlan.plan_date) == year
    )

    income_items = base_query.filter_by(type='entrada').order_by(FinancialPlan.amount.desc()).all()
    expense_items = base_query.filter_by(type='despesa').order_by(FinancialPlan.amount.desc()).all()

    total_income = sum(item.amount for item in income_items)
    total_expense = sum(item.amount for item in expense_items)
    balance = total_income - total_expense

    months = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
        (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
        (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')
    ]

    return render_template('financial_planning.html', title='Planejamento Financeiro', form=form,
                           income_items=income_items, expense_items=expense_items,
                           month=month, year=year, total_income=total_income,
                           total_expense=total_expense, balance=balance, months=months)