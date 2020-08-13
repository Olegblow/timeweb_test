import logging
import os
import tempfile

from pywebcopy import save_website

from services.zipper import create_zip


log = logging.getLogger(__name__)


def parser_site(url: str, task_id: str) -> None:
    parser = Parser(url, task_id)
    log.info('Parsing web site: %s .', url)
    parser.pars()


class Parser:
    def __init__(self, url: str, task_id: str):
        self.__url = url
        self.__id = task_id
        self.__create_temp_dir()

    def __create_temp_dir(self) -> None:
        """
        Создаем временную директорю где будет хранится файлы.

        C/tmp/pars/<task_id>
        """
        path = f'pars/{self.__id}'
        path = os.path.join(tempfile.gettempdir(), path)
        os.makedirs(path)
        self.__path = path

    def pars(self) -> None:
        save_website(url=self.__url, project_folder=self.__path, zip_project_folder=False)
        create_zip(self.__path, self.__id)
