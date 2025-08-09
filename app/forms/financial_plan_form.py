from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length, NumberRange
from ..models import Category

class FinancialPlanForm(FlaskForm):
    description = StringField('Descrição', validators=[DataRequired(), Length(max=200)])
    amount = DecimalField('Valor', places=2, validators=[DataRequired(), NumberRange(min=0.01)])
    type = SelectField('Tipo', choices=[('entrada', 'Entrada'), ('despesa', 'Despesa')], validators=[DataRequired()])
    plan_date = DateField('Data do Planejamento', format='%Y-%m-%d', validators=[DataRequired()])
    category_id = SelectField('Categoria', coerce=int, validators=[DataRequired(message="Selecione uma categoria.")])
    submit = SubmitField('Adicionar ao Planejamento')

    def __init__(self, *args, **kwargs):
        super(FinancialPlanForm, self).__init__(*args, **kwargs)
        if 'user' in kwargs:
            user = kwargs['user']
            self.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=user.id).order_by(Category.name).all()]
