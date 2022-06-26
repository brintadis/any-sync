import requests

from PIL import Image

from webapp.db import db
from webapp.playlist.models import Playlist, Track

from yandex_music import Client
from datetime import timedelta, datetime


def get_collage_items(list_images):
    name_num = 1
    for i in list_images:
        resp = requests.get(i, stream=True).raw
        img = Image.open(resp, mode='r')
        img.save(f'images/pict{name_num}.png', 'png')
        name_num += 1


def get_playlist_ya(url):
    """Get full information about playlist by it url and add it into our DB.
    """
    user_name = url.split('/')[4]
    kind_playlist = url.split('/')[-1]
    playlist_playlist = Client().users_playlists(int(kind_playlist), user_name)
    playlist_name = playlist_playlist.title
    owner_name = playlist_playlist.owner['name']

    if playlist_playlist.cover['uri'] is None:
        list_images = []
        for cover in playlist_playlist.cover.items_uri:
            img_cover = cover.replace('%%', '200x200')
            img_cover = f'https://{img_cover}'
            list_images.append(img_cover)

        get_collage_items(list_images)

    else:
        img_cover = str(playlist_playlist.cover['uri']).replace('%%', '200x200')
        img_cover = f'https://{img_cover}'

    return save_playlist(playlist_name, owner_name, playlist_playlist.tracks, kind_playlist, img_cover)


def save_playlist(playlist_name, owner_name, tracks, kind_playlist, img_cover):
    new_playlist = Playlist(
        playlist_name=playlist_name,
        owner_name=owner_name,
        kind=kind_playlist,
        img_cover=img_cover
    )
    db.session.add(new_playlist)
    db.session.commit()

    for track in tracks:
        duration_ms = track['track']['duration_ms']
        duration_and_random_date = datetime(1970, 1, 1) + timedelta(milliseconds=duration_ms)
        duration = duration_and_random_date.strftime("%M:%S")

        img_cover = str(track['track']['cover_uri']).replace('%%', '200x200')
        img_cover = f'https://{img_cover}'

        new_track = Track(
            playlist=new_playlist.id,
            artist=track['track']['artists'][0]['name'],
            track_name=track['track']['title'],
            duration=duration, img_cover=img_cover
        )
        db.session.add(new_track)
    db.session.commit()

    return new_playlist
