from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
# from yandex_music import Client

from webapp.db import db
from webapp.playlist.models import Playlist
from webapp.spotify.spotify import spotify_auth, sync_to_spotify
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.tasks import new_playlist
from webapp.ya_music.token_ya import get_token, sel_driver


blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route("/profile")
@login_required
def profile():
    title = "Мой AnySync"
    playlists = Playlist.query.filter(Playlist.user == current_user.id)
    return render_template("user/my_anysync.html", title=title, playlists=playlists)


@blueprint.route("/startspotoauth")
@login_required
def start_spot_oauth():
    auth_manager = spotify_auth()
    auth_url = auth_manager.get_authorize_url()
    print(auth_url)

    return redirect(auth_url)


@blueprint.route("/spotifyoauth")
@login_required
def spotifyoauth():
    auth_manager = spotify_auth()
    print(request.args)
    auth_manager.get_access_token(request.args.get("code"))

    return redirect(url_for("user.synchronization", music_service="Spotify"))


@blueprint.route("/yandexoauth")
@login_required
def yandexoauth():
    if current_user.yandex_token is None:
        qr_url, driver = sel_driver()
        print(1)
        print(qr_url)
        return render_template(
            "user/yandexoauth.html",
            qr_url=qr_url,
        )
        get_token(driver)
    return redirect(url_for("user.synchronization", music_service="Yandex Music"))


@blueprint.route("/sync-playlist")
@login_required
def sync_playlist():
    playlist_ids = request.values.getlist("playlist")
    music_service = request.values.get("music_service")
    public_playlist = request.values.get("public_playlist") == "True"

    if music_service == "Spotify":
        auth_manager = spotify_auth()
        sync_to_spotify(
            playlist_ids=playlist_ids,
            public_playlist=public_playlist,
            auth_manager=auth_manager,
        )
    elif music_service == "Yandex Music":
        # token = current_user.yandex_token
        # client = Client(token).init()
        new_playlist.delay(playlist_ids=playlist_ids)
    return redirect(url_for('user.profile'))


@blueprint.route("/synchronization/<music_service>")
@login_required
def synchronization(music_service):
    title = "Синхронизация плейлистов"
    playlists = Playlist.query.filter(Playlist.user == current_user.id)

    return render_template(
        "user/synchronization.html",
        title=title,
        playlists=playlists,
        music_service=music_service,
    )


@blueprint.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    title = "Авторизация"
    login_form = LoginForm()

    return render_template("user/login.html", page_title=title, form=login_form)


@blueprint.route("/process-login", methods=["POST"])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Вы успешно вошли на сайт")
            return redirect(url_for("index"))
    flash("Неправильное имя пользователя или пароль")

    return redirect(url_for("user.login"))


@blueprint.route("/logout")
def logout():
    logout_user()
    flash("Вы успешно разлогинились")

    return redirect(url_for("index"))


@blueprint.route("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    title = "Регистрация"
    form = RegistrationForm()

    return render_template("user/registration.html", page_title=title, form=form)


@blueprint.route("/process-reg", methods=["POST"])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            role="user",
            registration_date=datetime.today().strftime("%Y-%d-%m %H:%M:%S"),
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Вы успешно зарегистрировались!")
        return redirect(url_for("user.login"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    f'Ошибка в поле \
                    "{getattr(form, field).label.text}": - {error}'
                )
        return redirect(url_for("user.register"))
