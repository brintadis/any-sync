import os
from flask import Flask, render_template
from webapp.forms import PlaylistLinkForm
from webapp.ya_playlist import name_tracks, artists_tracks, duration_tracks


def create_app():
    app = Flask(__name__)

    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    @app.route("/", methods=['GET', 'POST'])
    def index():
        title = "AnySync"
        url_form = PlaylistLinkForm()
        return render_template('index.html', page_title=title, form=url_form)

    @app.route("/tracklist")
    def tracklist():
        title = "Список треков"
        name = name_tracks
        artist = artists_tracks
        duration = duration_tracks
        return render_template('track_list.html', page_title=title, name=name,
                               artist=artist, duration=duration)

    return app
