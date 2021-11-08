from typing import List, Optional
import logging
import re
from api.mattermost.abc import MattermostHttpApiVersion
import psycopg2.errors

from core.utils import retry_w_jitter
from core.sqllib.sql_mattermost import SQLMattermost
from logger import logger
from api.mattermost.v4.models import Post
import config


@retry_w_jitter(exception_classes=(psycopg2.OperationalError,), timeouts=(1, 1, 2, 3, 5,))
def save_filtered_messages_from_channel(
        db_connection: SQLMattermost,
        http_api: MattermostHttpApiVersion,
        channel_id: str,
        key_word: str = None,
        logger_: logging.Logger = logger,
):
    """
    Сохраняет в переданное подключение бд историю сообщений из указанного канала
    содержащие подстроку `key_word`
    ---
    :param db_connection: подключение
    :param http_api:      класс клиент для работы с mattermost API
    :param channel_id:    айдишник канала для обкачки
    :param key_word:      сохраняются только сообщения содержащие эту подстроку
    :param logger_:       логгер
    """
    page = 0
    while True:
        page_posts: List[Post] = []
        logger_.info(
            "Запрашиваем у mm историю сообщений для канала id="
            f"{channel_id}, страница={page}. Фильтруем по подстроке '{key_word}'"
        )
        messages = http_api.get_all_messages_from_channel(
            channel_id=channel_id,
            page=page
        )
        # Проверка на ранний выход
        if ('order' not in messages) or len(messages['order']) == 0:
            logger_.info("Сообщений нет")
            break
        logger_.info(f"Получено {len(messages['order'])}")
        for post_id in messages['order']:
            post = messages['posts'][post_id]

            if (key_word in post['message']) or key_word is None:
                post_to_save = Post(
                        id=post['id'],
                        filter_key=key_word,
                        channel_id=post['channel_id'],
                        user_id=post['user_id'],
                        create_at=post['create_at'],
                        # Тривиальная защита от sql-инъекции
                        message=re.sub('[\'";]', '', post['message']),
                    )
                logger_.info(f"Будет записано собщение: id={post_to_save.id}; message={post_to_save.message}")
                page_posts.append(post_to_save)
        try:
            # Записываем всю пачку сообщений
            if page_posts:
                logger_.info("Сохраняю посты...")
                db_connection.save_messages(page_posts)
                logger_.info("Ок")
        # перехватываем UniqueViolation
        except psycopg2.errors.lookup("23505"):
            # Если в базе уже есть одно из сообщений пачки
            # Записываем сообщения из пачки поштучно
            for post in page_posts:
                try:
                    db_connection.save_messages([post])
                except psycopg2.errors.lookup("23505"):
                    # Дубли игнорим
                    pass
            logger_.info("Ок")
        # переходим к следующей странице
        page += 1

