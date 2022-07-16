import os
import shutil
from datetime import datetime, timedelta
from random import shuffle

import requests
from flask import url_for
from flask_login import current_user
from PIL import Image
from yandex_music import Client

from webapp.db import db
from webapp.playlist.models import Playlist, Track
from webapp.ya_music.collage_maker import make_collage


def get_collage_items(list_image_urls):
    """Parse an image list with url equal to `url` and save it.

    Args:
        list_image_urls (_list_): Img urls

    Returns:
        _list_: Return a `list` of img paths.
    """
    name_num = 1
    img_path_list = []
    os.mkdir(f"webapp/images/temp/{current_user.id}/")
    for img in list_image_urls:
        resp = requests.get(img, stream=True).raw
        img = Image.open(resp, mode="r")
        path_to_save = f"webapp/images/temp/{current_user.id}/\
            pict{name_num}.png"
        img.save(path_to_save, "png")
        img_path_list.append(path_to_save)
        name_num += 1
    return img_path_list


def cover_processing(playlist, username, kind_playlist):
    """This function processes the cover url and makes a collage.

    Args:
        playlist: playlist obj from Yandex.
        username (_str_): Username.
        kind_playlist (_str_): Yandex playlist id.

    Returns:
        _str_: return collage url.
    """
    list_image_urls = []
    for cover in playlist.cover.items_uri:
        img_cover_url = cover.replace("%%", "200x200")
        img_cover_url = f"https://{img_cover_url}"
        list_image_urls.append(img_cover_url)

    if len(list_image_urls) == 1:
        img_cover_url = list_image_urls[0]

    elif len(list_image_urls) == 2:
        list_image_urls += list_image_urls
        shuffle(list_image_urls)

    elif len(list_image_urls) == 3:
        list_image_urls.append(list_image_urls[0])

    img_name = f"{username}_{kind_playlist}.png"
    collage_image_path = f"webapp/images/collage/{img_name}"
    if len(list_image_urls) != 1:
        make_collage(
            images=get_collage_items(list_image_urls), filename=collage_image_path
        )
        img_cover_url = url_for("send_media", name=img_name)

    # Remove temp dir with temp imgs.
    if os.path.isdir("webapp/images/temp"):
        shutil.rmtree(f"webapp/images/temp/{current_user.id}")

    return img_cover_url


def get_playlist_ya(url):
    """Get full information about playlist by it url and add it into our DB.

    Args:
        url (_str_): Full url to a yandex playlist.

    Returns:
        function: Return saved playlist function.
    """
    username = url.split("/")[4]
    kind_playlist = url.split("/")[-1]
    playlist = Client().users_playlists(int(kind_playlist), username)
    playlist_name = playlist.title
    owner_name = playlist.owner["name"]

    if playlist.cover["uri"] is None:
        img_cover_url = cover_processing(
            playlist=playlist, username=username, kind_playlist=kind_playlist
        )
    else:
        img_cover_url = str(playlist.cover["uri"]).replace("%%", "200x200")
        img_cover_url = f"https://{img_cover_url}"

    return save_playlist(
        playlist_name=playlist_name,
        owner_name=owner_name,
        tracks=playlist.tracks,
        kind_playlist=kind_playlist,
        img_cover_url=img_cover_url,
    )


def save_playlist(
    playlist_name, owner_name, tracks, kind_playlist, img_cover_url
):  # noqa: E501
    new_playlist = Playlist(
        playlist_name=playlist_name,
        owner_name=owner_name,
        kind=kind_playlist,
        img_cover=img_cover_url,
        user=current_user.id,
        last_update=datetime.today().date()
    )
    db.session.add(new_playlist)
    db.session.commit()

    for track in tracks:
        duration_ms = track["track"]["duration_ms"]
        duration_and_random_date = datetime(1970, 1, 1) + timedelta(
            milliseconds=duration_ms
        )
        duration = duration_and_random_date.strftime("%M:%S")

        img_cover_url = str(track["track"]["cover_uri"]).replace("%%", "200x200")
        img_cover_url = f"https://{img_cover_url}"

        new_track = Track(
            playlist=new_playlist.id,
            artist=track["track"]["artists"][0]["name"],
            track_name=track["track"]["title"],
            duration=duration,
            img_cover=img_cover_url,
        )
        db.session.add(new_track)
    db.session.commit()

    return new_playlist


def create_new_playlist(playlist_ids, client):
    for id in playlist_ids:
        playlist_name = Playlist.query.filter(Playlist.id == int(id)).first()
        new_playlist = client.users_playlists_create(f"{playlist_name.playlist_name}")
        tracks = Track.query.filter(Track.playlist == int(id))
        track_list = []
        for track in tracks:
            track_list.append(f"{track.track_name} {track.artist}")
        revision = 1
        for track_name in track_list:
            resalt_search = client.search(f"{track_name}", type_="all")
            if resalt_search.best is None:
                print(f"Трек {track_name} отсутствует")
            else:
                if resalt_search.best.type == "track":
                    resalt_best_track_id = resalt_search.best.result.id
                    resalt_best_album_id = resalt_search.best.result.albums[0].id
                    client.users_playlists_insert_track(
                        new_playlist.kind,
                        resalt_best_track_id,
                        resalt_best_album_id,
                        revision=revision,
                    )
                    revision += 1
                else:
                    print(f"Трек {track_name} отсутствует")
        revision = 0
