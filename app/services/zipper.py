import logging
import os
import shutil

from services.errors import ParsException


log = logging.getLogger(__name__)


def create_zip(path: str, name: str) -> None:
    """Архивируем все созданные данные."""
    if not os.path.exists(path):
        log.debug('Dir path %s, does not exist.', path)
        raise ParsException
    shutil.make_archive(f'files/{name}', 'gztar', path)
