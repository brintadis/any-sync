from celery import Celery
from webapp.ya_music.token_ya import get_token
from webapp.ya_music.ya_music import create_new_playlist
from yandex_music import Client
from flask_login import current_user

celery_app = Celery('tasks', broker='redis://redis:6379/0')


@celery_app.task()
def new_playlist(playlist_ids):
    token = current_user.yandex_token
    client = Client(token).init()
    create_new_playlist(playlist_ids, client)


@celery_app.task()
def check_qr_code(command_executor_url, session_id, user_id):
    get_token(command_executor_url, session_id, user_id)
