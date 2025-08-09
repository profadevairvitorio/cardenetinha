from .dependencies import (
    Blueprint, render_template, flash, redirect, url_for, abort, request, 
    login_required, current_user, db, Category, CategoryForm
)

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories')
@login_required
def categories():
    user_categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()
    return render_template('category/index.html', title='Gerenciar Categorias', categories=user_categories)


@category_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm(user_id=current_user.id)
    if form.validate_on_submit():
        new_category = Category(name=form.name.data, user_id=current_user.id)
        db.session.add(new_category)
        db.session.commit()
        flash('Categoria criada com sucesso!', 'success')
        return redirect(url_for('category.categories'))
    return render_template('category/new.html', title='Nova Categoria', form=form)


@category_bp.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('category.categories'))
    elif request.method == 'GET':
        form.name.data = category.name

    return render_template('category/edit.html', title='Editar Categoria', form=form, category=category)