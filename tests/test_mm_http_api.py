import unittest
import functools

import config
from api.mattermost import get_api_client_for_version
from core.sqllib.sql_mattermost import SQLMattermost
from api.mattermost.v4.models import Post


def cases(cases):
    """
    Декоратор для добавления сразу нескольких кейсов для декорируемого теста.
    Тест будет прогнан с каждым из переданных в декоратор кейсов.
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in cases:
                new_args = args + (c if isinstance(c, tuple) else (c,))
                f(*new_args)
        return wrapper
    return decorator


class MatterMostHttpApiMethodsTestCase(unittest.TestCase):
    mm_db = SQLMattermost(
        db_name=config.DATABASE_TEST_NAME,
        db_username=config.DATABASE_USERNAME,
        db_password=config.DATABASE_PASSWORD,
        db_host=config.DATABASE_HOST,
        db_port=config.DATABASE_PORT,
    )
    MM_HTTP_API_V: int = 4
    mm_http_api = get_api_client_for_version(MM_HTTP_API_V)

    def setUp(self) -> None:
        self.mm_db.create_tables()
        self.mm_db.delete_all_messages()

    def tearDown(self) -> None:
        self.mm_db.delete_all_messages()

    @cases(({'channel_id': 'rzocsdofoirp3mccwhgo8ddu5e', 'contains': '@mario'},))
    def test_get_messages_from_channel(self, case):
        """Убеждаемся что можем корректно получить историю сообщений из указанного канала"""
        messages = self.mm_http_api.get_all_messages_from_channel(
            channel_id=case['channel_id'],
        )
        return self.assertTrue('order' in messages and len(messages['order']) > 0)

    @cases([
        Post(id='19kdn6rgmp83dgkiryduyj8a6y212',
             filter_key='@mario',
             channel_id='rzocsdofoirp3mccwhgo8ddu5e',
             channel_display_name='test',
             user_id='f7hu5bczbtftdnmgzu7hkcwxse',
             sender_name='@mario',
             create_at=1635513995501,
             message='testtextttest29',),
    ])
    def test_save_message(self, case):
        """Сохранение одного сообщения"""
        self.mm_db.save_message(
            case
        )

    @cases([[
        Post(id='19kdn6rgmp83dgkiryduyj8a6y212',
             filter_key='@mario',
             channel_id='rzocsdofoirp3mccwhgo8ddu5e',
             channel_display_name='test',
             user_id='f7hu5bczbtftdnmgzu7hkcwxse',
             sender_name='@mario',
             create_at=1635513995501,
             message='testtextttest29', ),
        Post(id='19kdn6rgmp83dgkiryduyj8a6y2133',
             filter_key='@mario',
             channel_id='rzocsdofoirp3mccwhgo8ddu5e',
             channel_display_name='test',
             user_id='f7hu5bczbtftdnmgzu7hkcwxse',
             sender_name='@mario',
             create_at=1635513995581,
             message='ololo', ),
    ]])
    def test_save_messages(self, case):
        """Сохранение пачки сообщений"""
        self.mm_db.save_messages(case)
