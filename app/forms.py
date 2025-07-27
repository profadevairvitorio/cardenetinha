from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange
from .models import User, Account, Category

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

class CategoryForm(FlaskForm):
    name = StringField('Nome da Categoria', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Salvar Categoria')

    def __init__(self, user_id, original_name=None, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
        self.user_id = user_id

    def validate_name(self, name):
        if name.data != self.original_name:
            category = Category.query.filter_by(name=name.data, user_id=self.user_id).first()
            if category:
                raise ValidationError('Esta categoria já existe.')