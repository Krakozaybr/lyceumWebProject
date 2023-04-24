from flask_wtf import FlaskForm
from wtforms import IntegerField, FileField, TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired


class ItemTypeFormCreate(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    description = TextAreaField("Описание", validators=[DataRequired()])
    image = FileField("Картинка", validators=[DataRequired()])
    rare = IntegerField("Редкость", validators=[DataRequired()])
    submit = SubmitField("Сохранить")


class ItemTypeFormEdit(FlaskForm):
    id = IntegerField("Id")
    name = StringField("Название")
    description = TextAreaField("Описание")
    image = FileField("Картинка")
    rare = IntegerField("Редкость")
    submit = SubmitField("Сохранить")
