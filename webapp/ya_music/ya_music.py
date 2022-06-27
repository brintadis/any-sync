import requests
import os
import shutil

from flask import url_for

from random import shuffle
from datetime import timedelta, datetime

from PIL import Image
from yandex_music import Client

from webapp.ya_music.collage_maker import make_collage
from webapp.db import db
from webapp.playlist.models import Playlist, Track


def get_collage_items(list_images):
    """Parse an image list with url equal to `url` and save it.
        \nReturn a `list` of img paths.
    """
    name_num = 1
    img_path_list = []
    for img in list_images:
        resp = requests.get(img, stream=True).raw
        img = Image.open(resp, mode='r')
        path_to_save = f'webapp/images/temp/pict{name_num}.png'
        img.save(path_to_save, 'png')
        img_path_list.append(path_to_save)
        name_num += 1
    return img_path_list


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

        if len(list_images) == 1:
            img_cover = list_images[0]
            print(list_images)

        elif len(list_images) == 2:
            list_images += list_images
            print(list_images)
            shuffle(list_images)

        elif len(list_images) == 3:
            list_images.append(list_images[0])
            print(list_images)

        img_name = f'{user_name}_{kind_playlist}.png'
        cover_image_path = f'webapp/images/collage/{img_name}'
        if len(list_images) != 1:
            make_collage(
                get_collage_items(list_images),
                filename=cover_image_path
            )
            img_cover = url_for('send_media', name=img_name)

        # Remove temp dir with temp imgs.
        if os.path.isdir('webapp/images/temp'):
            shutil.rmtree('webapp/images/temp')
            os.mkdir('webapp/images/temp')

    else:
        img_cover = str(
            playlist_playlist.cover['uri']).replace('%%', '200x200')
        img_cover = f'https://{img_cover}'

    return save_playlist(
        playlist_name,
        owner_name,
        playlist_playlist.tracks,
        kind_playlist,
        img_cover
    )


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
        duration_and_random_date = datetime(1970, 1, 1) + \
            timedelta(milliseconds=duration_ms)
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
