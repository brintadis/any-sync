from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, URL


class PlaylistLinkForm(FlaskForm):
    link = URLField('Ссылка на плейлист', validators=[DataRequired(), URL()], render_kw={"class": "form-control"})
    # web_app = SelectField('Выберите музыкальный сервис', choices=[
    #     'Spotify', 'YandexMusic'], validators=[DataRequired()])
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})
