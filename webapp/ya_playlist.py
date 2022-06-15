from yandex_music import Client
from webapp.model import Playlist, db, Track


def get_playlist_ya(url):
    """Get full information about playlist by it url and add it into our DB.
    """
    # url = 'https://music.yandex.ru/users/gurkov.pawel/playlists/1004'
    user_name = url.split('/')[4]
    id_playlist = url.split('/')[-1]
    playlist_playlist = Client().users_playlists(int(id_playlist), user_name)
    playlist_name = playlist_playlist.title
    owner_name = playlist_playlist.owner['name']
    save_playlist(playlist_name, owner_name, playlist_playlist.tracks, id_playlist)


def save_playlist(playlist_name, owner_name, tracks, id_playlist):
    new_playlist = Playlist(playlist_name=playlist_name, owner_name=owner_name)
    db.session.add(new_playlist)
    # db.session.commit()
    for track in tracks:
        new_track = Track(
            playlist=new_playlist, artist=track['track']['artists'][0]['name'],
            track_name=track['track']['title'], duration=track['track']['duration_ms'])
        db.session.add(new_track)
    db.session.commit()
