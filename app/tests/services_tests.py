import os

import pytest

from app.services.zipper import create_zip
from app.services.errors import ParsException
from app.services.schema import is_url


def test_is_url():
    url, result = 'http:google.com', True
    assert is_url(url) == result


def test_error_create_archive():
    path = 'qwe/123'
    with pytest.raises(ParsException):
        create_zip(path)
    assert 2 == 2


def test_create_archive(file):
    path = ''

    create_zip(path)
    assert os.path.isfile(path + '/file.tar.gz')
