from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from webapp.db import db
from webapp.playlist.models import Playlist


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), index=True)
    email = db.Column(db.String(50), nullable=False)
    registration_date = db.Column(db.String(20), nullable=False)
    yandex_token = db.Column(db.String(100), nullable=True)
    spotify_token = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return "<User {} id {}>".format(self.username, self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == "admin"

    def count_playlist(self):
        return Playlist.query.filter(Playlist.user == self.id).count()
