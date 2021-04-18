from flask_wtf import FlaskForm
from data import db_session
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from data.db_models import type_table


# session = db_session.create_session() нужно исправить ошибку!
# type = session.query(type_table).all()
TYPE = ['Другое', 'Развлечения', 'Рестораны и кафе', 'Коммунальные платежи']


class RegistrationForm(FlaskForm):
    name = StringField('Имя:', validators=[DataRequired()])
    email = StringField('E-mail:', validators=[DataRequired(), Email('Некорректный адрес')])
    inn = IntegerField('ИНН:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    check_password = PasswordField('Повторите пароль:',
                                   validators=[EqualTo(fieldname='password', message='Пароли должны совпадать!')])
    submit = SubmitField('Зарегистрироваться')


class SettingsForm(FlaskForm):
    name = StringField('Имя:')
    email = StringField('E-mail:', validators=[Email('Некорректный адрес')])
    inn = IntegerField('ИНН:', validators=[DataRequired()])
    password = PasswordField('Пароль:')
    check_password = PasswordField('Повторите пароль:',
                                   validators=[EqualTo(fieldname='password', message='Пароли должны совпадать!')])
    submit = SubmitField('Применить')


class LoginForm(FlaskForm):
    email = StringField('E-mail:', validators=[DataRequired(), Email('Некорректный адрес')])
    inn = IntegerField('ИНН:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class CreateTypeForm(FlaskForm):
    name = StringField('Имя типа  расходов:', validators=[DataRequired()])
    submit = SubmitField('Создать')


class AddCheckForm(FlaskForm):
    str_Qr = StringField('Расшифрованный Qr код из чека:', validators=[DataRequired()])
    description = TextAreaField('Описание:', validators=[DataRequired()])
    id_type = SelectField('Тип расходов:', choices=TYPE, coerce=str, default='другое')
    information = StringField('Дополнительная информация:', validators=[DataRequired()])
    submit = SubmitField('Добавить')
