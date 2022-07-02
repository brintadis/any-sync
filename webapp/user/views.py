from flask import Blueprint, current_app, flash, redirect, render_template
from flask import url_for
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from webapp.db import db
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.user.token import generate_confirmation_token, confirm_token
from webapp.user.email import send_email

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = "Авторизация"
    login_form = LoginForm()

    return render_template(
        'user/login.html',
        page_title=title,
        form=login_form
    )


@blueprint.route("/process-login", methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли на сайт')
            return redirect(url_for('index'))
    flash('Неправильное имя пользователя или пароль')

    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')

    return redirect(url_for('index'))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = "Регистрация"
    form = RegistrationForm()

    return render_template(
        'user/registration.html',
        page_title=title,
        form=form
    )


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            role='user',
            confirmed=False
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        token = generate_confirmation_token(new_user.email, current_app.config)
        confirm_url = url_for('user.confirm_email',
                              token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(current_app.config, new_user.email, subject, html)
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.unconfirmed'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле \
                    "{getattr(form, field).label.text}": - {error}')
        return redirect(url_for('user.register'))


@blueprint.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(current_app.config, token)
    except:  # noqa: E722
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('index'))


@blueprint.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    html = render_template('user/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('user.unconfirmed'))


@blueprint.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('index')
    flash('Please confirm your account!', 'warning')
    return render_template('user/unconfirmed.html')
