from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from ..models import Category

class TransactionForm(FlaskForm):
    description = StringField('Descrição', validators=[DataRequired(), Length(max=200)])
    amount = DecimalField('Valor', places=2, validators=[DataRequired(), NumberRange(min=0.01)])
    type = SelectField('Tipo', choices=[('entrada', 'Entrada'), ('saida', 'Saída')], validators=[DataRequired()])
    category_id = SelectField('Categoria', coerce=int, validators=[Optional()])
    new_category = StringField('Nova Categoria', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Registrar Transação')

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        if 'user' in kwargs:
            user = kwargs['user']
            self.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=user.id).order_by(Category.name).all()]
            self.category_id.choices.insert(0, (0, 'Selecione uma categoria'))

    def validate(self, **kwargs):
        if not super().validate(**kwargs):
            return False
        if not self.category_id.data and not self.new_category.data:
            self.category_id.errors.append('Selecione uma categoria ou crie uma nova.')
            return False
        if self.category_id.data and self.new_category.data:
            self.new_category.errors.append('Escolha uma categoria existente ou crie uma nova, não ambos.')
            return False
        return True
