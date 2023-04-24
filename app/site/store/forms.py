from flask_wtf import FlaskForm
from wtforms import IntegerField, FileField, TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length


class ProductCreateForm(FlaskForm):
    description = TextAreaField("Описание", validators=[DataRequired()])
    price = IntegerField(
        "Цена за единицу", validators=[DataRequired(), NumberRange(min=1)]
    )
    count = IntegerField("Количество", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Сохранить")


class ProductEditForm(FlaskForm):
    id = IntegerField("ID")
    description = TextAreaField("Описание", validators=[DataRequired()])
    price = IntegerField(
        "Цена за единицу", validators=[DataRequired(), NumberRange(min=1)]
    )
    count = IntegerField("Количество", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Сохранить")


class ProductBuyForm(FlaskForm):
    count = IntegerField("Количество", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Купить")


class CommentForm(FlaskForm):
    text = TextAreaField("Текст комментария", validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField("Добавить комментарий")
