from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    FileField,
    TextAreaField,
    StringField,
    SubmitField,
    FieldList,
)
from wtforms.validators import DataRequired, NumberRange


class ChestFormCreate(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    description = TextAreaField("Описание", validators=[DataRequired()])
    image = FileField("Картинка", validators=[DataRequired()])
    price = IntegerField("Цена", validators=[NumberRange(min=0)])

    items_count_min = IntegerField(
        "Минимальное количество предметов",
        validators=[NumberRange(min=0)],
    )
    items_count_max = IntegerField(
        "Максимальное количество предметов",
        validators=[NumberRange(min=0)],
    )
    coins_min = IntegerField(
        "Минимальное количество монет", validators=[NumberRange(min=0)]
    )
    coins_max = IntegerField(
        "Максимальное количество монет", validators=[NumberRange(min=0)]
    )
    item_types = StringField("Типы предметов через ;", validators=[DataRequired()])

    submit = SubmitField("Сохранить")


class ChestFormEdit(FlaskForm):
    id = IntegerField("Id")
    name = StringField("Название", validators=[DataRequired()])
    description = TextAreaField("Описание", validators=[DataRequired()])
    price = IntegerField("Цена", validators=[DataRequired()])

    items_count_min = IntegerField(
        "Минимальное количество предметов",
        validators=[DataRequired(), NumberRange(min=0)],
    )
    items_count_max = IntegerField(
        "Максимальное количество предметов",
        validators=[DataRequired(), NumberRange(min=0)],
    )
    coins_min = IntegerField(
        "Минимальное количество монет", validators=[DataRequired(), NumberRange(min=0)]
    )
    coins_max = IntegerField(
        "Максимальное количество монет", validators=[DataRequired(), NumberRange(min=0)]
    )
    item_types = StringField("Типы предметов через ;", validators=[DataRequired()])
    image = FileField("Картинка")
    submit = SubmitField("Сохранить")
