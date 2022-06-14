import spotipy
from spotipy.oauth2 import SpotifyOAuth

from model import db, Playlist, Track

# Client Credentials Flow and Scope settings
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://example.com"
SCOPE = ('user-library-read, playlist-read-private, playlist-modify-private, playlist-modify-public, user-read-private, user-library-modify, user-library-read')


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
        # Return dict.
        return self.playlist

    def get_track_artist_list(self, playlist):
        # Create list of dicts and append there all tracks from the playlist.
        playlist_tracks = []
        for track in playlist['tracks']['items']:
            playlist_tracks.append({
                'track_name': track['track']['name'],
                'artist': track['track']['artists'][0]['name'],
                'img_cover': track['track']['album']['images'][0]['url'],
                'track_spotify_id': track['track']['id']
                }
            )
        # Return list of dict.
        for track in playlist_tracks:
            self.save_track_to_db(
                track['artist'],
                track['track_name'],
                track['img_cover'],
                track['track_spotify_id']
            )
        # return playlist_tracks

    def save_track_to_db(self, artist, track_name, img_cover, track_spotify_id):
        new_track = Track(artist, track_name, img_cover, track_spotify_id)
        db.session.add(new_track)
        db.session.commit()


# FOR TESTING
if __name__ == "__main__":
    import json
    spot = Spotify()
    playlist_id = '1ctLnyNe1eIHblFYt5cj41'
    playlist = spot.get_playlist_by_id(playlist_id=playlist_id)
    tracks = spot.get_track_artist_list(playlist=playlist)
    print(json.dumps(tracks))
