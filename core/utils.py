import os
import time
from functools import wraps
from logging import Logger
from random import random
from typing import Tuple, Dict, Any, Type
from pathlib import Path

import yaml

from logger import logger


def retry_w_jitter(
    exception_classes: Tuple[Type[Exception], ...],
    timeouts: Tuple[int, ...] = (1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89),
    logger_: Logger = logger,
):
    """Декоратор преднозначен для оборачивания функций которые обращаются на удалённые ресурсы.
    При не удачном походе на ресурс декоратор перезапускает функицию поочерёдно через интервалы
    переданные в параметре `timeouts` умноженное на jitter.
    (jitter - это "дрожатель" увеличивающий случайность таймаута перезапроса чтобы все инстансы с программой
    запускающей оборачиваеую функцию не стучались на поднявшийся серевер
    одновременно и не положили его опять)
    Если колчество не удачных попыток исчерпано возбуждаетя исключение причина неудачи.
    ---
    :param exception_classes: Классы ожидаемых ошибок которые тригерят ретрай
    :param timeouts:   Таймауты перед ретраями (в секундах)
    :param logger_:     Логгер
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            final_exception = None
            for timeout in timeouts:
                try:
                    logger_.info(f"Запускаем функцию {func.__name__}")
                    return func(*args, **kwargs)
                except exception_classes as e:
                    # Берём рандомное число от 0 до 1
                    jitter = random()
                    # прибавляем к таймауту чтобы увеличить случайность периодов
                    # между перезапросами
                    sleep_timeout = timeout + jitter * 10
                    logger_.error(f"Ошибка при исполнении функции {func.__name__}.\n")
                    logger_.error(e)
                    logger_.error(f"Следующая попытка через {sleep_timeout} секунд.")
                    time.sleep(sleep_timeout)
                    final_exception = e
            # Если отведённые попытки кончились бросаем ошибку наверх
            raise final_exception

        return wrapper

    return decorator


def get_config(logger_: Logger = logger, filepath: str = None) -> Dict[str, Any]:
    filepath = filepath or os.environ.get('CONFIG_FILE')
    filepath = filepath or os.path.join(Path(__file__).parent.parent, 'config.yaml')
    try:
        with open(filepath, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        return config
    except FileNotFoundError as e:
        raise SystemExit(f"Не найден файл конфига. {filepath} не существует.")
    except PermissionError as e:
        raise SystemExit(f"Не хватает прав на чтение файла конфига. {filepath}")


def import_by_string(module_path):
    """
    Для динамического импорта модулей по строке вида `module.name`
    :param module_path: path.to.module
    """
    module_name, unit_name = module_path.rsplit('.', 1)
    return getattr(__import__(module_name, fromlist=['']), unit_name)