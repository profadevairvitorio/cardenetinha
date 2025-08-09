from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class EditAccountForm(FlaskForm):
    name_account = StringField(
        'Nome da Conta',
        validators=[
            DataRequired(message="O nome da conta é obrigatório."),
            Length(min=3, max=100, message="O nome deve ter entre 3 e 100 caracteres.")
        ]
    )
    submit = SubmitField('Salvar Alterações')
