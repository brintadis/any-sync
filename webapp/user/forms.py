"""
Init user forms
"""
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.user.models import User


class LoginForm(FlaskForm):
    """
    Login form
    """
    username = StringField(
        "Имя пользователя",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    password = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    remember_me = BooleanField(
        "Запомнить меня", default=True, render_kw={"class": "form-check-input"}
    )
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    """
    Registration form
    """
    username = StringField(
        "Имя пользователя",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    email = StringField(
        "Электронная почта",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"},
    )
    password = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    password2 = PasswordField(
        "Повторите пароль",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        """
        Validating an username
        """
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError("Пользователь с таким именем уже существует")

    def validate_email(self, email):
        """
        Validating an email
        """
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError("Пользователь с такой почтой уже существует")


class YandexLoginForm(FlaskForm):
    """
    Yandex login form
    """
    email = StringField(
        "Электронная почта",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"},
    )
    password = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})
