import os

from celery import Celery
from celery.result import AsyncResult
from flask import abort
from flask import Flask
from flask import request
from flask import Response
from flask import send_file
from flask.views import MethodView

from services import create_schema
from services import init_celery
from services import parser_site
from services import validate_data


app = Flask(__name__)
RABBITMQ_USER = os.getenv('RABBITMQ_DEFAULT_USER', '')
RABBITMQ_PASS = os.getenv('RABBITMQ_DEFAULT_PASS', '')
RABBITMQ_VHOST = os.getenv('RABBITMQ_DEFAULT_VHOST', '')
RABBITMQ_HOST = os.getenv('RABBIT_HOST', '')
RABBIT_URL = f'{RABBITMQ_USER}:{RABBITMQ_PASS}{RABBITMQ_HOST}5672/{RABBITMQ_VHOST}'
app.config['CELERY_BROKER_URL'] = f'amqp://{RABBIT_URL}'
app.config['CELERY_RESULT_BACKEND'] = f'rpc://{RABBIT_URL}'
celery: Celery = init_celery(app)


#  хэндлеры. TODO вынести в отдельный файл
#  -----------------------------------------------------------------------------

class TaskHandler(MethodView):
    """
    Хэндлер для создания и проверки статуса таска.

    ID - идентификатор задачи.
    """

    def get(self, task_id:str) -> Response:
        result = AsyncResult(task_id, app=celery).state
        response = {'status': result}
        if result == 'SUCCESS':
            url = f'{request.host_url}get_archive/{task_id}'
            response.update(url=url)
        return response

    def post(self) -> Response:
        data = request.json
        data = validate_data(data, create_schema)
        task = task_pars.delay(data['url'])
        return {'id': task.id}


@app.route('/get_archive/<task_id>')
def get_archive_handler(task_id) -> Response:
    """Хэндлер возвращает архив."""
    file_name = f'{task_id}.tar.gz'
    path = os.path.join('files', file_name)
    if not os.path.isfile(path):
        abort(404)
    return send_file(path, as_attachment=True, attachment_filename=file_name)


#  flask routing
#  -----------------------------------------------------------------------------

task_handler = TaskHandler.as_view('tasks')
app.add_url_rule('/api/v1/task/<task_id>', view_func=task_handler, methods=['GET'])
app.add_url_rule('/api/v1/task', view_func=task_handler, methods=['POST'])


#  task celery
#  ----------------------------------------------------------------------------

@celery.task
def task_pars(site_url: str) -> None:
    parser_site(site_url, task_pars.request.id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
