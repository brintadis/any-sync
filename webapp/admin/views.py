from flask import Blueprint, render_template

from webapp.playlist.models import Playlist
from webapp.user.decorators import admin_required
from webapp.user.models import User

blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@blueprint.route("/")
@admin_required
def admin_index():
    title = "Админ панель"
    users = User.query.all()
    users_count = User.query.count()
    playlists_count = Playlist.query.count()

    return render_template(
        "admin/index.html",
        title=title,
        users=users,
        users_count=users_count,
        playlists_count=playlists_count,
    )
