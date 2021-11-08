from weakref import WeakKeyDictionary
from enum import Enum
from typing import Any, Dict
from decimal import Decimal
import re


class DescriptorOwner(type):
    """Мета-класс для добавления кастомного поведения классу
    """

    def __new__(mcs, name, bases, attrs):
        """
        Добавляет атрибутам класса (дескрипторам) свойство label равное имени атрибута
        И заполняет атрибуты `fields` и `required_fields`
        """
        fields = set()  # Список полей у класса инстанса
        required_fields = set()  # Список обязательных полей
        for field_name, attr in attrs.items():

            if isinstance(attr, ResponseObjectField):
                attr.label = field_name  # Назначаем атрибут label дескриптору

                fields.add(field_name)
                if attr.required:
                    required_fields.add(field_name)
        instance = super(DescriptorOwner, mcs).__new__(mcs, name, bases, attrs)
        instance.fields = fields
        instance.required_fields = required_fields
        return instance


class ResponseObjectField:
    """Класс дескриптора реализует логику хранения и валидации значения
    """
    def __init__(self, required=False, nullable=True, **extended_properties):
        self.required = required
        self.nullable = nullable
        self.extended_properties: Dict = extended_properties
        self.data = WeakKeyDictionary()
        self.label = None

    def __set__(self, instance, value):
        """Сеттер дескриптора"""
        # Проверяем что значение не пустое если поле не nullable
        if not value and not self.nullable:
            raise ValueError(
                f"Поле {self.label} в {instance.__class__.__name__} не nullable."
            )
        # Сохраняем отвалидированное значение в дескрипторе
        self.data[instance] = self.__validate(instance, value)

    def __get__(self, instance, owner):
        """Геттер дескриптора"""
        return self.data[instance]

    def __validate(self, instance, value):
        validated_value = None

        ancestors = self.__class__.__mro__
        # Итерируемся через предков в порядке наследования пропустив первые два класса (ResponseObjectField и object)
        # в которых не реализован метод `validate`
        for idx in range(3, len(ancestors) + 1):
            ancestor = ancestors[-idx]

            self.is_valid, validated_value = ancestor.validate(self, instance, value)

            if not self.is_valid:
                # Строим сообщение об ошибке из докстринги метода `validate`
                err_mess = ancestor.validate.__doc__ or ""

                if err_mess:
                    err_mess = err_mess + " но получено {value} типа {value_type}"

                raise ValueError(
                    err_mess.format(
                        field_name=self.label, value=value, value_type=type(value)
                    )
                )
        return validated_value

    def validate(self, instance, value) -> (bool, Any):
        """
        Чтобы использовать этот класс надо реализовать этот метод
        Он должен возвращать два значения:

        :return:
            boolean результат валидации значения,
            и само значение
        :raise: ValueError
        """
        raise NotImplementedError


class IntegerField(ResponseObjectField):
    """Поле для модели типа int"""

    def validate(self, instance, value) -> (bool, Any):
        """Значение не соответствует типу , ожидается `int`"""
        return isinstance(value, int), value


class StringField(ResponseObjectField):
    """Поле для модели типа str"""

    def validate(self, instance, value) -> (bool, Any):
        """Значение не соответствует типу, ожидается `str`"""
        return isinstance(value, str), value


class DecimalField(ResponseObjectField):
    """Поле для модели типа Decimal"""

    def validate(self, instance, value) -> (bool, Any):
        """Значение не соответствует типу, ожидается `Decimal`"""
        return isinstance(value, Decimal), value


class EnumField(ResponseObjectField):
    """Поле которое может хранить одно из нескольких указанных в параметре `available_options` значений
    """

    def validate(self, instance, value) -> (bool, Any):
        """Значение не является одним из допустимых"""
        available_options = self.extended_properties.get("available_options")
        if issubclass(available_options, Enum):
            validation_result = value in set(item.value for item in available_options)
        else:
            validation_result = value in available_options
        return validation_result, value


class SqlSafeStringField(ResponseObjectField):
    """Поле для модели типа str"""

    def validate(self, instance, value) -> (bool, Any):
        """Значение не соответствует типу, ожидается `str`"""
        # Тривиальная защита от sql-инъекции
        return isinstance(value, str), re.sub('[\'";]', '', value)
