# -*- coding: utf-8 -*-
"""
Обходит историю сообщений из указанных каналов, ищет сообщения которые ещё не сохранены и сохраняет их
"""
import logging
import sys
import time

import psycopg2

from core.bot.mm_history_bot import save_filtered_messages_from_channel
from core.sqllib.sql_mattermost import SQLMattermost
from api.mattermost import get_api_client_for_version
import config
from logger import logger


def main():
    """
    Логика необходимая для выполнения перед запуском основного скрипта
    """
    logger.info("Стартую")
    mm_db = SQLMattermost(
        db_name=config.DATABASE_NAME,
        db_username=config.DATABASE_USERNAME,
        db_password=config.DATABASE_PASSWORD,
        db_host=config.DATABASE_HOST,
        db_port=config.DATABASE_PORT,
    )
    # Создаём таблицы
    logger.info("Пытаюсь создать таблицы в бд...")
    for t in range(5):
        try:
            mm_db.create_tables()
            break
        except psycopg2.OperationalError as e:
            logger.error(e)
            logger.error(f"Пока нет подключения к БД. Следующая попытка через: {t} сек.")
            time.sleep(t)
        logger.error("Создать таблицы не удалось")
        sys.exit("Ошибка при созании таблиц")

    logger.info("ОК, таблицы созданы.")

    # Забираем, фильтруем по подстроке историю
    # сообщений из указанных каналов и сохраняем их в БД
    logger.info(f"Начинаю поиск и сохранение сообщений "
                f"содержащих подстраку `{config.MATTERMOST_LISTEN_CHANNELS}`")

    # Селектим апи-клиент под нужную версию
    mm_http_api = get_api_client_for_version(version=config.MATTERMOST_API_VERSION)
    for channel_id in config.MATTERMOST_LISTEN_CHANNELS:
        save_filtered_messages_from_channel(
            db_connection=mm_db,
            http_api=mm_http_api,
            channel_id=channel_id,
            key_word=config.MATTERMOST_FILTER_MESSAGES_CONTAINS
        )
    logger.info("Сообщения сохранены")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(e)
