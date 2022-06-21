import os
from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from webapp.forms import PlaylistLinkForm, LoginForm
from webapp.model import db, User, Playlist
from webapp.ya_playlist import get_playlist_ya
from webapp.spotify import get_playlist_by_id


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/", methods=['GET', 'POST'])
    def index():
        title = "AnySync"
        url_form = PlaylistLinkForm()
        if url_form.validate_on_submit():
            if 'spotify' in url_form.link.data:
                get_playlist_by_id(url_form.link.data)
            elif 'yandex' in url_form.link.data:
                get_playlist_ya(url_form.link.data)
            # return redirect
        return render_template('index.html', page_title=title, form=url_form)

    @app.route("/playlists")
    def get_playlist():
        title = "Список плейлистов"
        playlists = Playlist.query.all()
        return render_template('playlists.html', page_title=title, playlists=playlists)

    # @app.route("/playlist/<playlist_id>", methods=['GET', 'POST'])
    # def playlist(playlist):

    @app.route("/login")
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route("/process-login", methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы вошли на сайт')
                return redirect(url_for('index'))
        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))

    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return 'Привет админ'
        else:
            return 'Ты не админ!'

    return app
