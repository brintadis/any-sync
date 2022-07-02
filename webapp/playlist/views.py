from flask import Blueprint
from flask import render_template, redirect
from flask_login import login_required

from webapp.playlist.models import Playlist, Track
from webapp.playlist.forms import PlaylistLinkForm

from webapp.ya_music.ya_music import get_playlist_ya
from webapp.spotify.spotify import get_playlist_by_id

blueprint = Blueprint('playlist', __name__, url_prefix='/playlist')


@blueprint.route("/", methods=['GET', 'POST'])
@login_required
def test():
    title = "AnySync"
    url_form = PlaylistLinkForm()

    if url_form.validate_on_submit():
        if 'spotify' in url_form.link.data:
            new_playlist = get_playlist_by_id(url_form.link.data)
            return redirect(f'playlist/{new_playlist.id}')
        elif 'yandex' in url_form.link.data:
            new_playlist = get_playlist_ya(url_form.link.data)
            return redirect(f'playlist/{new_playlist.id}')

    return render_template(
        'playlist/test.html',
        page_title=title,
        form=url_form
    )


@blueprint.route("/playlists")
def all_playlists():
    title = "Список плейлистов"
    playlists = Playlist.query.all()

    return render_template(
        'playlist/playlists.html',
        page_title=title,
        playlists=playlists
    )


@blueprint.route("/playlist/<playlist_id>", methods=['GET', 'POST'])
def playlist(playlist_id):
    title = 'Треклист плейлиста'
    current_playlist = Playlist.query.filter(
        Playlist.id == playlist_id
        ).first()
    track_list = Track.query.filter(Track.playlist == playlist_id)

    return render_template(
        'playlist/playlist.html',
        page_title=title,
        track_list=track_list,
        current_playlist=current_playlist
    )


@blueprint.route("/playlist_user/<user_id>", methods=['GET', 'POST'])
@login_required
def playlist_user(user_id):
    title = "Мои плейлисты"
    playlists = Playlist.query.filter(Playlist.user == user_id)
    return render_template(
        'playlist/playlist_user.html',
        page_title=title,
        playlists=playlists,
        user_id=user_id
    )
