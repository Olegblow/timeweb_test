from celery import Celery
from flask import Flask


def init_celery(app: Flask) -> Celery:
    """Инициализируем настройки celery."""
    celery = Celery(
        app.name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """
        Ссылка по настройке селери для flask.

        https://flask.palletsprojects.com/en/1.1.x/patterns/celery/#configure
        """

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery
