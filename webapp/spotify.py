# import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Client Credentials Flow and Scope settings
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://example.com"
SCOPE = ('''user-library-read, playlist-read-private,
    playlist-modify-private, playlist-modify-public, user-read-private,
    user-library-modify, user-library-read''')


class Spotify:

    def __init__(self) -> None:
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope=SCOPE,
                redirect_uri=REDIRECT_URI,
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                show_dialog=True,
                cache_path="cache/token.txt"
            )
        )

    def get_playlist_by_id(self, playlist_id):
        # Get full information about playlist by it id.
        self.playlist = self.sp.playlist(playlist_id=playlist_id)
        # Return it in dict.
        return self.playlist

    def get_track_artist_list(self, playlist):
        # Create list of dicts and append there all tracks from the playlist.
        playlist_tracks = []
        for track in playlist['tracks']['items']:
            playlist_tracks.append({
                'track_name': track['track']['name'],
                'artist': track['track']['artists'][0]['name']
                }
            )
        # Return it in list.
        return playlist_tracks


# FOR TESTING
# ///
# spot = Spotify()
# playlist_id = '1ctLnyNe1eIHblFYt5cj41'
# playlist = spot.get_playlist_by_id(playlist_id=playlist_id)
# tracks = spot.get_track_artist_list(playlist=playlist)
# print(tracks)
