from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from webapp.db import db
from webapp.playlist.models import Playlist


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    email = db.Column(db.String(50))

    def __repr__(self):
        return '<User {} id {}>'.format(self.username, self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def count_playlist(self):
        return Playlist.query.filter(Playlist.user == self.id).count()
