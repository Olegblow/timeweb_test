import os
import pytest
import shutil

from services.zipper import create_zip
from services.errors import ParsException
from services.schema import is_url


@pytest.mark.parametrize(
    'parameters',
    (
        ('http:', False),
        ('google.com', False),
        ('http//google', False),
        ('https://google.com', True),
        ('http://google.com/123/', True)
    )
)
def test_is_url(parameters):
    url, result = parameters
    assert is_url(url) == result


def test_error_create_archive():
    path = 'qwe/123'
    name = 'qwe'
    with pytest.raises(ParsException):
        create_zip(path, name)


@pytest.fixture
def create_file():
    path = 'qwe/'
    os.mkdir(path)
    with open(os.path.join(path, 'test_file.txt'), 'w') as f:
        f.write(str(123))
    yield
    shutil.rmtree(path)


def test_create_archive(create_file):
    path = 'qwe'
    name = '123'
    file = f'files/{name}.tar.gz'
    create_zip(path, name)
    assert os.path.isfile(file)
    os.remove(file)
