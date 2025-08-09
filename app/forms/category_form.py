from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from ..models import Category

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
