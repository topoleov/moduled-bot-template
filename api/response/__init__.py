"""
Модуль предоставляющий средства для обработки ответов от API
"""
from api.response.fields import DescriptorOwner


class ResponseObject(metaclass=DescriptorOwner):
    """Класс работы с объектами json из ответов от апишек
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return_str = ['<']
        for f in self.fields:
            return_str.append(f"\t{f}: {getattr(self, f)}")
        return_str.append('>')
        return '\n'.join(return_str)