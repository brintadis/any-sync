from flask import Flask, render_template, send_from_directory
from flask_login import LoginManager
from flask_migrate import Migrate

from webapp.admin.views import blueprint as admin_blueprint
from webapp.db import db
from webapp.playlist.views import blueprint as playlist_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate = Migrate(app, db)  # noqa: F841

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(playlist_blueprint)
    app.register_blueprint(user_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    def index():
        title = "AnySync"
        return render_template("index.html", page_title=title)

    @app.route("/media/<name>")
    def send_media(name):
        print(app.config["UPLOAD_FOLDER"], name)
        return send_from_directory(app.config["UPLOAD_FOLDER"], name)

    return app
