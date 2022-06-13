from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, SelectField, StringField, PasswordField
from wtforms.validators import DataRequired, URL


class PlaylistLinkForm(FlaskForm):
    link = URLField('Ссылка на плейлист', validators=[DataRequired(), URL()])
    web_app = SelectField('Выберите музыкальный сервис', choices=['Spotify', 'YandexMusic'],
                          validators=[DataRequired()])
    submit = SubmitField('Отправить')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отпарвить', render_kw={"class": "btn btn-primary"})
