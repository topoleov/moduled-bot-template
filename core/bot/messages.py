# -*- coding: utf-8 -*-
from core.bot.languages import Languages


class Icons:
    """
    Класс с иконками для формирования сообщений
    """
    new_icon = "\U0001F195"
    blue_icon = "\U0001F535"
    orange_icon = "\U0001F7E0"
    fire_icon = "\U0001F525"
    deleted_icon = "\U0000274C"
    green_icon = "\U0001F7E2"
    right_arrow_icon = "\U000027A1"
    up_arrow_icon = "\U00002B06"


class BotErrorMessages:
    """
    Класс в котором прописаны сообщения с ошибками
    (ограничения_на_количество_файлов, ошибка_отправки, ошибка_загрузки)
    Формат сообщения:
    event_name = {
        Language.selected_language_1: str = text_1,
        Language.selected_language_2: str = text_1,
    }
    """
    upload_limit_message = {
        Languages.russian: """\nВнимание!!! Сообщение содержит более 5 файлов !!!"""
                           """\nMattermost не может отправить все файлы!!!"""
                           """\nПожалуйста проверьте оригинал сообщения!!!""",
    }
    upload_error = {
        Languages.russian: """\nНе удалось загрузить файл {0}\nОшибка: {1}"""
    }


class BotMessages:
    """
    Класс в котором прописаны сообщения для определенных случаев
    (новое_сообщение, изменение_статуса, и т.д.)
    Формат сообщения:

    event_name

    event_name = {
        Language.selected_language_1: str = text_1,
        Language.selected_language_2: str = text_1,
    }
    """
    new_issue = {
        Languages.russian:
            """{0} ДАТА: {1} ({2} - {3})\n"""
            """ОРГАНИЗАЦИЯ: {4}\n"""
            """СТАТУС: {5}\n"""
            """НАЗВАНИЕ: {6} {7}\n"""
            """ОПИСАНИЕ: {8}\n"""}

    new_status = {
        Languages.russian:
            """ДАТА: {0} ({1} - {2})\n"""
            """ОРГАНИЗАЦИЯ: {3}\n"""
            """{4} СТАТУС: {5}\n"""
            """НАЗВАНИЕ: {6} {7}\n"""}

    new_status_mattermost = {
        Languages.russian:
            """"{0} ({1} - {2})\n"""
            """ОРГАНИЗАЦИЯ: {3}\n"""
            """НАЗВАНИЕ: {4}\n"""
            """ДАТА: {5}\n"""
            """СТАТУС: {6}\n"""
            """ОПИСАНИЕ: {7}\n"""
            """КОММЕНТАРИЙ: {8}"""}

    new_status_mattermost_without_comment = {
        Languages.russian:
            """{0} ({1} - {2})\n"""
            """ОРГАНИЗАЦИЯ: {3}\n"""
            """НАЗВАНИЕ: {4}\n"""
            """ДАТА: {5}\n"""
            """СТАТУС: {6}\n"""
            """ОПИСАНИЕ: {7}"""}

    new_comment = {
        Languages.russian:
            """ДАТА: {0} ({1} - {2})\n"""
            """ОРГАНИЗАЦИЯ: {3}\n"""
            """СТАТУС: {4}\n"""
            """НАЗВАНИЕ: {5} {6}\n"""
            """{7} КОММЕНТАРИЙ: {8}\n"""}

    delete = {
        Languages.russian:
            """ДАТА: {0}\n"""
            """ОРГАНИЗАЦИЯ: {1}\n"""
            """НАЗВАНИЕ: {2} {3}\n""" +
            """{4} УДАЛЕН!"""}

    new_priority = {
        Languages.russian:
        # url/name (old_priority right_arrow new_priority - issue_type
        # issue_summary
            """{0} ({1} {2} {3} - {4})\n"""
            """НАЗВАНИЕ: {5}\n"""}

    clone = {
        Languages.russian:
            """{0} СОЗДАН КЛОН: {1}\n"""
            """НАЗВАНИЕ: {2}"""}


