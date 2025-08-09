from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from ..models import Account

class ReportForm(FlaskForm):
    start_date = DateField('Data de Início', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Data de Fim', format='%Y-%m-%d', validators=[DataRequired()])
    account = SelectField('Conta', coerce=int)
    submit = SubmitField('Gerar Relatório')

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        if 'user' in kwargs:
            user = kwargs['user']
            self.account.choices = [(0, 'Todas as Contas')] + [(a.id, a.name_account) for a in Account.query.filter_by(user_id=user.id).all()]
