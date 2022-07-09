from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired


class PlaylistLinkForm(FlaskForm):
    link = URLField(
        'Ссылка на плейлист',
        validators=[DataRequired(), URL()],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})
