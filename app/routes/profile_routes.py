from .dependencies import (
    Blueprint, render_template, flash, redirect, url_for, request, 
    login_required, current_user, db, UpdateProfileForm
)

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/perfil')
@login_required
def perfil():
    return render_template('perfil/index.html', title='Seu Perfil')


@profile_bp.route('/perfil/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('profile.perfil'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('perfil/edit.html', title='Editar Perfil', form=form)