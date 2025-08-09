from .dependencies import (
    Blueprint, render_template, flash, redirect, url_for, abort, request, 
    login_required, current_user, db, Goal, Account, GoalForm
)

goal_bp = Blueprint('goal', __name__)

@goal_bp.route('/goals')
@login_required
def goals():
    user_goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template('goal/index.html', title='Minhas Metas', goals=user_goals)


@goal_bp.route('/goal/new', methods=['GET', 'POST'])
@login_required
def new_goal():
    form = GoalForm()

    form.account.choices = [
        (acc.id, acc.name_account) for acc in
        Account.query.filter_by(user_id=current_user.id).order_by(Account.name_account).all()
    ]

    if form.validate_on_submit():
        selected_account = db.session.get(Account, form.account.data)

        if selected_account:
            new_goal = Goal(
                name=form.name.data,
                target_amount=form.target_amount.data,
                account=selected_account,
                user_id=current_user.id
            )
            db.session.add(new_goal)
            db.session.commit()
            flash('Meta criada com sucesso!', 'success')
            return redirect(url_for('goal.goals'))
        else:
            flash('Conta selecionada inválida.', 'danger')

    return render_template('goal/new.html', title='Nova Meta', form=form)

@goal_bp.route('/goal/edit/<int:goal_id>', methods=['GET', 'POST'])
@login_required
def edit_goal(goal_id):
    goal = db.session.get(Goal, goal_id)
    if goal is None or goal.user_id != current_user.id:
        abort(404)

    form = GoalForm()

    form.account.choices = [
        (acc.id, acc.name_account) for acc in
        Account.query.filter_by(user_id=current_user.id).order_by(Account.name_account).all()
    ]

    if form.validate_on_submit():
        selected_account = db.session.get(Account, form.account.data)

        goal.name = form.name.data
        goal.target_amount = form.target_amount.data
        goal.account = selected_account

        db.session.commit()
        flash('Meta atualizada com sucesso!', 'success')
        return redirect(url_for('goal.goals'))

    elif request.method == 'GET':
        form.name.data = goal.name
        form.target_amount.data = goal.target_amount
        form.account.data = goal.account.id

    return render_template('goal/edit.html', title='Editar Meta', form=form, goal=goal)

@goal_bp.route('/goal/delete/<int:goal_id>', methods=['POST'])
@login_required
def delete_goal(goal_id):
    goal = db.session.get(Goal, goal_id)
    if goal is None or goal.user_id != current_user.id:
        abort(404)
    db.session.delete(goal)
    db.session.commit()
    flash('Meta excluída com sucesso!', 'success')
    return redirect(url_for('goal.goals'))