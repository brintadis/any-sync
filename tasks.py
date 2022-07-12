from celery import Celery
# from webapp import create_app
from webapp.ya_music.ya_music import create_new_playlist

celery_app = Celery('tasks', broker='redis://redis:6379/0')
# flask_app = create_app()


@celery_app.task(serializer='json')
def new_playlist(playlist_ids, client):
    create_new_playlist(playlist_ids, client)
