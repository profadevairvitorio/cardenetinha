from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class AccountForm(FlaskForm):
    name_account = StringField(
        'Nome da Conta',
        validators=[
            DataRequired(message="O nome da conta é obrigatório."),
            Length(min=3, max=100, message="O nome deve ter entre 3 e 100 caracteres.")
        ]
    )

    initial_balance = DecimalField(
        'Saldo Inicial (Opcional)',
        places=2,
        validators=[
            Optional(),
            NumberRange(min=0, message="O saldo inicial não pode ser negativo.")
        ],
        default=0.00
    )

    submit = SubmitField('Criar Conta')
