from urllib.parse import urlparse


def validate_url(field: str, value: str, error):

    if not is_url(value):
        error(field, f'is not valid url, {value}')


create_schema = {
    'url': {
        'type': 'string',
        'required': True,
        'empty': False,
        'validator': validate_url
    }
}


def is_url(url: str) -> bool:
    """Проверяем является ли строка ссылкой."""
    result = urlparse(url)
    return all((result.scheme, result.netloc))
