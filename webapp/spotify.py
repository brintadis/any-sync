import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from webapp.model import Playlist, db, Track

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
    return save_playlist(
        playlist_name=playlist_name,
        owner_name=owner_name,
        tracks=playlist['tracks']['items'],
        id_playlist=playlist_id
    )


def save_playlist(playlist_name, owner_name, tracks, id_playlist):
    new_playlist = Playlist(playlist_name=playlist_name, owner_name=owner_name)
    db.session.add(new_playlist)
    db.session.commit()
    for track in tracks:
        duration = str(int(track['track']['duration_ms']) * 0.000016)
        duration = f'{duration[:1]}:{duration[2:4]}'
        new_track = Track(
            playlist=new_playlist.id, artist=track['track']['artists'][0]['name'],
            track_name=track['track']['name'], duration=duration)
        db.session.add(new_track)
    db.session.commit()
    return new_playlist


if __name__ == "__main__":
    # import json

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
        )
    )

    playlist_url = 'https://open.spotify.com/playlist/1ctLnyNe1eIHblFYt5cj41'
    playlist_id = playlist_url.split('/')[-1]
    if '?' in playlist_id:
        playlist_id = playlist_id.split('?')[0]
    playlist = sp.playlist(playlist_id=playlist_id)
    print(type(playlist['tracks']['items'][0]['track']['duration_ms']))
