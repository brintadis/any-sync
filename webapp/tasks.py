from celery import Celery
from webapp import create_app
from webapp.ya_music.token_ya import get_token
from webapp.ya_music.ya_music import create_new_playlist

celery_app = Celery('tasks', broker='redis://redis:6379/0')
flask_app = create_app()


@celery_app.task()
def new_playlist(playlist_ids, token):
    with flask_app.app_context:
        create_new_playlist(playlist_ids, token)


@celery_app.task()
def check_qr_code(command_executor_url, session_id, user_id):
    with flask_app.app_context():
        get_token(command_executor_url, session_id, user_id)
