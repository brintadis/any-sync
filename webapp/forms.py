from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

class PlaylistLinkForm(FlaskForm):
    link = URLField('Ссылка на плейлист', validators=[DataRequired(), URL()])
    web_app = SelectField('Выберите музыкальный сервис', choices=['Spotify', 'YandexMusic'], validators=[DataRequired()])
    submit = SubmitField('Отправить')