from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_login import current_user
from ..models import Account

class GoalForm(FlaskForm):
    name = StringField('Nome da Meta', validators=[DataRequired(), Length(min=3, max=120)])
    target_amount = DecimalField('Valor do Objetivo', places=2, validators=[DataRequired(), NumberRange(min=1)])
    account = SelectField('Conta Vinculada', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar Meta')

    def __init__(self, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)
        self.account.choices = [
            (acc.id, acc.name_account) for acc in
            Account.query.filter_by(user_id=current_user.id).order_by(Account.name_account).all()
        ]
