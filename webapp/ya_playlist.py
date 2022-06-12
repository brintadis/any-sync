from yandex_music import Client
from webapp.model import Playlist, db


def get_playlist_ya():
    url = 'https://music.yandex.ru/users/gurkov.pawel/playlists/1004'
    user_name = url.split('/')[4]
    id_playlist = url.split('/')[-1]
    playlist_playlist = Client().users_playlists(int(id_playlist), user_name)
    playlist_name = playlist_playlist.title
    owner_name = playlist_playlist.owner['name']
    save_playlist(playlist_name, owner_name)


def save_playlist(playlist_name, owner_name):
    new_playlist = Playlist(playlist_name=playlist_name, owner_name=owner_name)
    db.session.add(new_playlist)
    db.session.commit()
