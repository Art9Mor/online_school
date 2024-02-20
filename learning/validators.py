import re

from rest_framework.exceptions import ValidationError


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        pattern = r'^https://www.youtube.com/watch\?v='
        tmp = dict(value).get(self.field)
        ratio = re.match(pattern, tmp)
        if not ratio:
            raise ValidationError('Недопустимая ссылка.')
