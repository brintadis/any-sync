import spotipy
import os

from flask_login import current_user

from webapp.db import db
from webapp.playlist.models import Playlist, Track

from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from datetime import timedelta, datetime

# Client Credentials Flow and Scope settings
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/users/spotifyoauth"
SCOPE = (
    '''user-library-read,
    playlist-read-private,
    playlist-modify-private,
    playlist-modify-public,
    user-read-private,
    user-library-modify,
    user-library-read'''
)


def get_playlist_by_id(playlist_url):
    """Get full information about playlist by it url.
    """
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
    )

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


def sync_to_spotify(tracks, playlist_to_create, public_playlist):
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=SCOPE,
            redirect_uri=REDIRECT_URI,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            show_dialog=True,
            cache_path="webapp/spotify/token.txt"
        )
    )
    user_id = sp.current_user()["id"]

    # Searching Spotify for songs by title and artist
    songs_uris = []
    for track in tracks:
        search_results = sp.search(
            q="artist:" + track.artist + " track:" + track.track_name,
            type="track"
        )
        try:
            uri = search_results["tracks"]["items"][0]["uri"]
            songs_uris.append(uri)
        except IndexError:
            print(
                f"{track.track_name} by {track.artist}\
                doesn't exist in Spotify. Skipped."
            )
    print('as', songs_uris)

    # Creating a private playlist
    playlist = sp.user_playlist_create(
        user=user_id,
        name=playlist_to_create.playlist_name,
        public=public_playlist
    )

    # Updating an exist playlist's cover
    # sp.playlist_upload_cover_image(
    #     playlist_id=playlist["id"],
    #     image_b64=playlist_to_create.img_cover
    # )

    # Adding songs found to the new playlist
    sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uris)


def save_playlist(playlist_name, owner_name, tracks, id_playlist, img_cover):
    new_playlist = Playlist(
        playlist_name=playlist_name,
        owner_name=owner_name,
        img_cover=img_cover,
        user=current_user.id
    )

    db.session.add(new_playlist)
    db.session.commit()

    for track in tracks:
        duration_ms = int(track['track']['duration_ms'])
        duration_and_random_date = datetime(1970, 1, 1) + \
            timedelta(milliseconds=duration_ms)
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
