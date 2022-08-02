from flask import Flask, render_template, send_from_directory
from flask_login import LoginManager
from flask_migrate import Migrate

from webapp.blueprints import init_blueprints
from webapp.db import db
from webapp.user.models import User


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate = Migrate(app, db)  # noqa: F841

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    init_blueprints(app)

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
