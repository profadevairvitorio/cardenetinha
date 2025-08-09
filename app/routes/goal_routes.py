from .dependencies import (
    Blueprint, render_template, flash, redirect, url_for, abort, request, 
    login_required, current_user, db, Goal, Account, GoalForm, jsonify
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

    if form.validate_on_submit():
        selected_account = db.session.get(Account, form.account.data)
        if not selected_account:
            return jsonify({'success': False, 'errors': {'account': ['Conta inválida.']}})

        new_goal = Goal(
            name=form.name.data,
            target_amount=form.target_amount.data,
            account=selected_account,
            user_id=current_user.id
        )
        db.session.add(new_goal)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Meta criada com sucesso!'})

    if request.method == 'GET':
        return render_template('goal/_goal_form.html', form=form, action_url=url_for('goal.new_goal'))
    
    return jsonify({'success': False, 'errors': form.errors})

@goal_bp.route('/goal/edit/<int:goal_id>', methods=['GET', 'POST'])
@login_required
def edit_goal(goal_id):
    goal = db.session.get(Goal, goal_id)
    if goal is None or goal.user_id != current_user.id:
        abort(404)

    form = GoalForm(obj=goal)

    if form.validate_on_submit():
        selected_account = db.session.get(Account, form.account.data)
        if not selected_account:
            return jsonify({'success': False, 'errors': {'account': ['Conta inválida.']}})

        goal.name = form.name.data
        goal.target_amount = form.target_amount.data
        goal.account = selected_account
        db.session.commit()
        return jsonify({'success': True, 'message': 'Meta atualizada com sucesso!'})

    if request.method == 'GET':
        form.account.data = goal.account_id
        return render_template('goal/_goal_form.html', form=form, action_url=url_for('goal.edit_goal', goal_id=goal_id))

    return jsonify({'success': False, 'errors': form.errors})

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
