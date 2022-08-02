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
    from webapp.ya_music.ya_music import create_new_playlist
    create_new_playlist(playlist_ids, token)


# @celery_app.task()
# def yandex_login(email, password, user_id):
#     with flask_app.app_context():
#         from webapp.ya_music.token_ya import yandex_ouath
#         yandex_ouath(email, password, user_id)

