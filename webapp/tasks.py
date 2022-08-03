"""
Celery tasks
"""
from create_celelry_app import make_celery
from webapp import create_app

flask_app = create_app()
# flask_app.config.update(CELERY_CONFIG={
#     'broker_url': 'redis://localhost:6379',
#     'result_backend': 'redis://localhost:6379',
# })
celery_app = make_celery(flask_app)


@celery_app.task()
def new_playlist(playlist_ids, token):
    """
    Creating new playlist using celery
    """
    from webapp.ya_music.ya_music import create_new_playlist
    create_new_playlist(playlist_ids, token)
