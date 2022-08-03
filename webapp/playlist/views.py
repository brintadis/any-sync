"""
Playlist views
"""
from datetime import datetime
from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

from webapp.db import db
from webapp.playlist.forms import PlaylistLinkForm
from webapp.playlist.models import Playlist, Track
from webapp.spotify.spotify import get_playlist_by_id
from webapp.ya_music.ya_music import get_playlist_ya

blueprint = Blueprint("playlist", __name__, url_prefix="/playlist")


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def search_playlist_by_url():
    """View for search playlist by url

    Returns:
        HTML page with playlist-link form.
    """
    title = "AnySync"
    url_form = PlaylistLinkForm()

    if url_form.validate_on_submit():
        if "spotify" in url_form.link.data:
            new_playlist = get_playlist_by_id(url_form.link.data)
            return redirect(url_for("playlist.playlist", playlist_id=new_playlist.id))
        if "yandex" in url_form.link.data:
            new_playlist = get_playlist_ya(url_form.link.data)
            return redirect(url_for("playlist.playlist", playlist_id=new_playlist.id))

    return render_template("playlist/search_playlist_by_url.html", page_title=title, form=url_form)


@blueprint.route("/playlists")
@login_required
def all_playlists():
    """View for all playlists

    Returns:
        HTML page with all users playlists.
    """
    title = "Список плейлистов"
    playlists = Playlist.query.all()

    return render_template(
        "playlist/playlists.html", page_title=title, playlists=playlists
    )


@blueprint.route("/playlist/<playlist_id>", methods=["GET", "POST"])
@login_required
def playlist(playlist_id):
    """View for playlist by id

    Returns:
        HTML page with tracks by playlist id.
    """
    title = "Треклист"
    current_playlist = Playlist.query.filter(Playlist.id == playlist_id).first()
    track_list = Track.query.filter(Track.playlist == playlist_id)

    return render_template(
        "playlist/playlist.html",
        page_title=title,
        track_list=track_list,
        current_playlist=current_playlist,
    )


@blueprint.route("/playlist_user/<user_id>", methods=["GET", "POST"])
@login_required
def playlist_user(user_id):
    """View for playlists by user id

    Returns:
        HTML page with playlists by user id
    """
    title = "Мои плейлисты"
    playlists = Playlist.query.filter(Playlist.user == user_id)
    return render_template(
        "playlist/playlist_user.html",
        page_title=title,
        playlists=playlists,
        user_id=user_id,
    )


@blueprint.route("/delete_playlist/<playlist_id>")
@login_required
def delete_playlist(playlist_id):
    """View for deleting playlist from the db

    Args:
        playlist_id: playlist id

    Returns:
        redirect to a user profile page
    """
    playlist_to_delete = Playlist.query.get(int(playlist_id))
    Track.query.filter(Track.playlist == int(playlist_id)).delete()
    db.session.delete(playlist_to_delete)
    db.session.commit()

    return redirect(url_for("user.profile"))


@blueprint.route("/delete_track_from_playlist/<track_id>")
@login_required
def delete_track(track_id):
    """View for deleting playlist from the db

    Args:
        track_id: track_id id

    Returns:
        redirect to the playlist page
    """
    track_to_delete = Track.query.get(int(track_id))
    playlist_id = track_to_delete.playlist
    playlist_to_update = Playlist.query.get(track_to_delete.playlist)
    playlist_to_update.last_update = datetime.today()

    db.session.delete(track_to_delete)
    db.session.commit()

    return redirect(url_for("playlist.playlist", playlist_id=playlist_id))
