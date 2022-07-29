from celery import Celery


def make_celery(app):
    celery = Celery('tasks', broker='redis://redis:6379/0')
    # celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
