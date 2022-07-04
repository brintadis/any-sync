from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from webapp.db import db

from webapp.spotify.spotify import sync_to_spotify

from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.playlist.models import Playlist, Track

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route("/profile")
@login_required
def profile():
    title = 'Мой AnySync'
    playlists = Playlist.query.filter(Playlist.user == current_user.id)

    return render_template(
        'user/my_anysync.html',
        title=title,
        playlists=playlists
    )


@blueprint.route("/spotifyoauth")
@login_required
def spotifyoauth():
    return redirect(url_for('user.sync_playlist'))


@blueprint.route("/sync-playlist")
@login_required
def sync_playlist():
    playlist_ids = request.values.getlist('playlist')
    # if len(playlist_ids) == 0:
    #     redire
    music_service = request.values.get('music_service')
    public_playlist = request.values.get('public_playlist') == 'True'

    if music_service == 'Spotify':
        for playlist_id in playlist_ids:
            print(playlist_id)
            playlist_to_create = Playlist.query.filter(
                Playlist.id == int(playlist_id)
            ).first()
            tracks = Track.query.filter(
                Track.playlist == int(playlist_id)
            )

            sync_to_spotify(
                tracks=tracks,
                playlist_to_create=playlist_to_create,
                public_playlist=public_playlist
            )

    return redirect(url_for('user.synchronization'))


@blueprint.route("/synchronization")
@login_required
def synchronization():
    title = "Синхронизация плейлистов"
    playlists = Playlist.query.filter(Playlist.user == current_user.id)

    return render_template(
        'user/synchronization.html',
        title=title,
        playlists=playlists
    )


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
            registration_date=datetime.today().strftime('%Y-%d-%m %H:%M:%S')
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле \
                    "{getattr(form, field).label.text}": - {error}')
        return redirect(url_for('user.register'))
