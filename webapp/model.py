from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_name = db.Column(db.String, nullable=False)
    owner_name = db.Column(db.String, nullable=False)
    last_update = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.Text, nullable=True)
    img_cover = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Playlist {self.playlist_name} {self.owner}>"


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
    artist = db.Column(db.String, nullable=False)
    track_name = db.Column(db.String, nullable=False)
    duration = db.Column(db.String, nullable=True)
    img_cover = db.Column(db.String, nullable=True)
    track_spotify_id = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Track {self.track_name} by {self.artist}>"
