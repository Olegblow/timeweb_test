import os

import pytest

from app.main import app as create_app


@pytest.fixture
def test_file_archive():
    file_path = 'files/123.tar.gz'
    with open(file_path, 'w+'):
        pass
    yield
    os.remove(file_path)


@pytest.fixture
def app():
    app = create_app
    return app


def test_get_archive_404(client):
    url = 'get_archive/123'
    assert client.get(url).status_code == 404


def test_get_archive_200(client, test_file_archive):
    url = 'get_archive/123'
    assert client.get(url).status_code == 200


@pytest.mark.parametrize(
    'parameters',
    (
        #  (data, status),
        ({'q': 'q'}, 500),
        ({'url': ''}, 500),
        ({'url': 'http:'}, 500),
    )
)
def test_create_task_handler(client, parameters):
    url = '/api/v1/task'
    data, status = parameters
    res = client.post(url, data=data)
    assert res.status_code == status


def test_get_task_status(client):
    url = '/api/v1/task/123'
    res = client.get(url)
    assert res.status_code == 200
