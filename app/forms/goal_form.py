from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class GoalForm(FlaskForm):
    name = StringField('Nome da Meta', validators=[DataRequired(), Length(min=3, max=120)])
    target_amount = DecimalField('Valor do Objetivo', places=2, validators=[DataRequired(), NumberRange(min=1)])

    account = SelectField(
        'Conta Vinculada',
        coerce=int,
        validators=[DataRequired()]
    )
    submit = SubmitField('Salvar Meta')
