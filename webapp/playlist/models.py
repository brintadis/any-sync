"""
Init playlist models
"""
from webapp.db import db


class Track(db.Model):
    """
    Track model
    """
    id = db.Column(db.Integer, primary_key=True)
    playlist = db.Column(db.Integer, db.ForeignKey("playlist.id"))
    artist = db.Column(db.String, nullable=False)
    track_name = db.Column(db.String, nullable=False)
    duration = db.Column(db.String, nullable=False)
    img_cover = db.Column(db.String, nullable=True)

    def __repr__(self):
        """
        Rerp of a Playlist model
        """
        return f"<Track {self.track_name} by {self.artist}>"


class Playlist(db.Model):
    """
    Playlist model
    """
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    playlist_name = db.Column(db.String, nullable=False)
    owner_name = db.Column(db.String, nullable=False)
    last_update = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text, nullable=True)
    img_cover = db.Column(db.String, nullable=True)
    kind = db.Column(db.String, nullable=True)

    def __repr__(self):
        """
        Rerp of a Playlist model
        """
        return f"<Playlist {self.playlist_name} {self.owner_name}>"

    def count_tracks(self):
        """
        Playlist's count tracks
        """
        return Track.query.filter(Track.playlist == self.id).count()
