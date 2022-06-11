from flask import Flask, render_template
from ya_playlist import name_tracks, artists_tracks, duration_tracks

app = Flask(__name__)


@app.route("/")
def index():
    title = "Список треков"
    name = name_tracks
    artist = artists_tracks
    duration = duration_tracks
    return render_template('track_list.html', page_title=title, name=name,
                           artist=artist, duration=duration)


if __name__ == "__main__":
    app.run(debug=True)
