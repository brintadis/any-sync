from yandex_music import Client
from webapp.model import Playlist, db, Track
from datetime import timedelta


def get_playlist_ya(url):
    """Get full information about playlist by it url and add it into our DB.
    """
    user_name = url.split('/')[4]
    kind_playlist = url.split('/')[-1]
    playlist_playlist = Client().users_playlists(int(kind_playlist), user_name)
    playlist_name = playlist_playlist.title
    owner_name = playlist_playlist.owner['name']
    if playlist_playlist.cover['uri'] is None:
        img_cover = playlist_playlist.cover.items_uri[0].replace('%%', '200x200')
    else:
        img_cover = str(playlist_playlist.cover['uri']).replace('%%', '200x200')
    return save_playlist(playlist_name, owner_name, playlist_playlist.tracks, kind_playlist, img_cover)


def save_playlist(playlist_name, owner_name, tracks, kind_playlist, img_cover):
    new_playlist = Playlist(playlist_name=playlist_name, owner_name=owner_name, kind=kind_playlist, img_cover=img_cover)
    db.session.add(new_playlist)
    db.session.commit()
    for track in tracks:
        # duration = str(track['track']['duration_ms'] * 0.000016)
        # duration = f'{duration[:1]}:{duration[2:4]}'
        duration_ms = track['track']['duration_ms']
        duration = str(timedelta(milliseconds=duration_ms))
        new_track = Track(
            playlist=new_playlist.id, artist=track['track']['artists'][0]['name'],
            track_name=track['track']['title'], duration=duration)
        db.session.add(new_track)
    db.session.commit()
    return new_playlist
