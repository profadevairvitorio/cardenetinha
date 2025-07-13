from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange
from .models import User, Account

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nome de usuário já está em uso. Por favor, escolha outro.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já está registrado. Por favor, use outro.')


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

class EditAccountForm(FlaskForm):
    name_account = StringField(
        'Nome da Conta',
        validators=[
            DataRequired(message="O nome da conta é obrigatório."),
            Length(min=3, max=100, message="O nome deve ter entre 3 e 100 caracteres.")
        ]
    )
    submit = SubmitField('Salvar Alterações')

class TransactionForm(FlaskForm):
    description = StringField('Descrição', validators=[DataRequired(), Length(max=200)])
    amount = DecimalField('Valor', places=2, validators=[DataRequired(), NumberRange(min=0.01)])
    type = SelectField('Tipo', choices=[('entrada', 'Entrada'), ('saida', 'Saída')], validators=[DataRequired()])
    submit = SubmitField('Registrar Transação')