from webapp import create_app
from webapp.ya_playlist import get_playlist_ya

app = create_app()
with app.app_context():
    get_playlist_ya()
