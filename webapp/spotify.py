import spotipy
import os

from webapp.model import db
from webapp.playlist.models import Playlist, Track

from spotipy.oauth2 import SpotifyClientCredentials
from datetime import timedelta, datetime

# Client Credentials Flow and Scope settings
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://example.com"
SCOPE = ('''user-library-read, playlist-read-private, playlist-modify-private, playlist-modify-public, user-read-private,
          user-library-modify, user-library-read''')

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        # scope=SCOPE,
        # redirect_uri=REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        # show_dialog=True,
        # cache_path="cache/token.txt"
    )
)


def get_playlist_by_id(playlist_url, sp=sp):
    """Get full information about playlist by it id.
    """
    playlist_id = playlist_url.split('/')[-1]

    if '?' in playlist_id:
        playlist_id = playlist_id.split('?')[0]

    playlist = sp.playlist(playlist_id=playlist_id)
    playlist_name = playlist['name']
    owner_name = playlist['owner']['display_name']
    img_cover = playlist['images'][0]['url']

    return save_playlist(
        playlist_name=playlist_name,
        owner_name=owner_name,
        img_cover=img_cover,
        tracks=playlist['tracks']['items'],
        id_playlist=playlist_id
    )


def save_playlist(playlist_name, owner_name, tracks, id_playlist, img_cover):
    new_playlist = Playlist(
        playlist_name=playlist_name,
        owner_name=owner_name,
        img_cover=img_cover
    )

    db.session.add(new_playlist)
    db.session.commit()

    for track in tracks:
        duration_ms = int(track['track']['duration_ms'])
        duration_and_random_date = datetime(1970, 1, 1) + timedelta(milliseconds=duration_ms)
        duration = duration_and_random_date.strftime("%M:%S")

        new_track = Track(
            playlist=new_playlist.id,
            artist=track['track']['artists'][0]['name'],
            track_name=track['track']['name'],
            duration=duration,
            img_cover=track['track']['album']['images'][0]['url']
        )
        db.session.add(new_track)
    db.session.commit()

    return new_playlist
