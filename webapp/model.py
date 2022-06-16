from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    def __repr__(self):
        return '<User {} id {}>'.format(self.username, self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist = db.Column(db.Integer, db.ForeignKey('playlist.id'))
    artist = db.Column(db.String, nullable=False)
    track_name = db.Column(db.String, nullable=False)
    duration = db.Column(db.String, nullable=False)
    img_cover = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Track {self.track_name} by {self.artist}>"


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_name = db.Column(db.String, nullable=False)
    owner_name = db.Column(db.String, nullable=False)
    last_update = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.Text, nullable=True)
    img_cover = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Playlist {self.playlist_name} {self.owner_name}>"

    def count_tracks(self):
        return Track.query().filter(Track.playlist == self.id).count
