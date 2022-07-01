from flask import Blueprint, render_template

from webapp.user.models import User
from webapp.user.decorators import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_index():
    return 'Привет админ'


@blueprint.route('/user-playlists')
@admin_required
def admin_playlists():
    title = 'Плейлисты пользователей'
    users = User.query.all()

    return render_template(
        'admin/all_users_playlists.html',
        title=title,
        users=users
    )
