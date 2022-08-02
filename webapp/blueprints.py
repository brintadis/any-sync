from webapp.admin.views import blueprint as admin_blueprint
from webapp.playlist.views import blueprint as playlist_blueprint
from webapp.user.views import blueprint as user_blueprint


def init_blueprints(app):
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(playlist_blueprint)
    app.register_blueprint(user_blueprint)
