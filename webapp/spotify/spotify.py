import os
from datetime import datetime, timedelta

import spotipy
from flask_login import current_user
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from webapp.db import db
from webapp.playlist.models import Playlist, Track

# Client Credentials Flow and Scope settings
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
# REDIRECT_URI = "http://example.com"
REDIRECT_URI = "http://127.0.0.1:5000/users/spotifyoauth"
SCOPE = """user-library-read,
    playlist-read-private,
    playlist-modify-private,
    playlist-modify-public,
    user-read-private,
    user-library-modify,
    user-library-read"""

CACHES_FOLDER = "webapp/spotify/spotify_caches/"
if not os.path.exists(CACHES_FOLDER):
    os.makedirs(CACHES_FOLDER)


def get_playlist_tracks(sp, playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results["items"]
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])
    return tracks


def get_playlist_by_id(playlist_url):
    """Get full information about playlist by it url and save it to a DB.

    Args:
        playlist_url (`str`): An url of a playlist.

    Returns:
        function: Return saved playlist function.
    """
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET
        )
    )

    playlist_id = playlist_url.split("/")[-1]

    if "?" in playlist_id:
        playlist_id = playlist_id.split("?")[0]

    playlist = sp.playlist(playlist_id=playlist_id)
    playlist_name = playlist["name"]
    owner_name = playlist["owner"]["display_name"]
    img_cover = playlist["images"][0]["url"]
    tracks = get_playlist_tracks(sp=sp, playlist_id=playlist_id)

    return save_playlist(
        playlist_name=playlist_name,
        owner_name=owner_name,
        img_cover=img_cover,
        tracks=tracks,
        id_playlist=playlist_id,
    )


def session_cache_path():
    return CACHES_FOLDER + str(current_user.id)


def spotify_auth():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path()
    )

    auth_manager = SpotifyOAuth(
        scope=SCOPE,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        show_dialog=True,
        cache_handler=cache_handler
        # cache_path=f"webapp/spotify/cache/{current_user.id}/token.txt",
    )

    return auth_manager


def sync_to_spotify(playlist_ids, public_playlist, auth_manager):
    """Creating a playlist and adding tracks into the playlist.

    Args:
        tracks (`SQLQeury`): list of tracks from DB.
        playlist_to_create (`SQLQeury`): Playlist from DB,
        that you want to create.
        public_playlist (`bool`): Will be the playlist private or not.
    """

    sp = spotipy.Spotify(auth_manager=auth_manager)

    user_id = sp.current_user()["id"]

    for playlist_id in playlist_ids:
        print(playlist_id)
        playlist_to_create = Playlist.query.filter(
            Playlist.id == int(playlist_id)
        ).first()
        tracks = Track.query.filter(Track.playlist == int(playlist_id))

        # Searching Spotify for songs by title and artist
        songs_uris = []
        for track in tracks:
            search_results = sp.search(
                q=f"track:{track.track_name}, artist:{track.artist}", type="track"
            )
            try:
                uri = search_results["tracks"]["items"][0]["uri"]
                songs_uris.append(uri)
            except IndexError:
                print(
                    f"{track.track_name} by {track.artist}\
                    doesn't exist in Spotify. Skipped."
                )

        # Creating a private playlist
        playlist = sp.user_playlist_create(
            user=user_id, name=playlist_to_create.playlist_name, public=public_playlist
        )

        # Adding songs found to the new playlist
        sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uris)

        # Updating an exist playlist's cover
        # sp.playlist_upload_cover_image(
        #     playlist_id=playlist["id"],
        #     image_b64=playlist_to_create.img_cover
        # )


def save_playlist(playlist_name, owner_name, tracks, id_playlist, img_cover):
    new_playlist = Playlist(
        playlist_name=playlist_name,
        owner_name=owner_name,
        img_cover=img_cover,
        user=current_user.id,
        last_update=datetime.today()
    )

    db.session.add(new_playlist)
    db.session.commit()

    for track in tracks:
        duration_ms = int(track["track"]["duration_ms"])
        duration_and_random_date = datetime(1970, 1, 1) + timedelta(
            milliseconds=duration_ms
        )
        duration = duration_and_random_date.strftime("%M:%S")

        new_track = Track(
            playlist=new_playlist.id,
            artist=track["track"]["artists"][0]["name"],
            track_name=track["track"]["name"],
            duration=duration,
            img_cover=track["track"]["album"]["images"][0]["url"],
        )
        db.session.add(new_track)
    db.session.commit()

    return new_playlist
