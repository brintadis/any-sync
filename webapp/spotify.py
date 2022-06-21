import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from webapp.model import Playlist, db, Track
from datetime import timedelta

# Client Credentials Flow and Scope settings
# CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
# CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
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
    img_cover = playlist['images'][1]['url']
    save_playlist(
        playlist_name=playlist_name,
        owner_name=owner_name,
        img_cover=img_cover,
        tracks=playlist['tracks']['items'],
        id_playlist=playlist_id
    )

    return playlist


# def get_track_artist_list(playlist):
#     """Create list of dicts and append there all tracks from the playlist.
#     """
#     playlist_tracks = []
#     for track in playlist['tracks']['items']:
#         playlist_tracks.append({
#             'track_name': track['track']['name'],
#             'artist': track['track']['artists'][0]['name']
#             }
#         )
#     return playlist_tracks


def save_playlist(playlist_name, owner_name, tracks, id_playlist, img_cover):
    new_playlist = Playlist(playlist_name=playlist_name, owner_name=owner_name, img_cover=img_cover)
    db.session.add(new_playlist)
    db.session.commit()
    for track in tracks:
        duration_ms = int(track['track']['duration_ms'])
        duration = str(timedelta(milliseconds=duration_ms))
        new_track = Track(
            playlist=new_playlist.id, artist=track['track']['artists'][0]['name'],
            track_name=track['track']['name'], duration=duration)
        db.session.add(new_track)
    db.session.commit()


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
