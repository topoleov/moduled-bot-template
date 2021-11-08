# -*- coding: utf-8 -*-

class MessageTypes:
    """
    Описание типов инцидентов, при которых срабатывают оповещения(используется в формировании сообщений
    """
    new_issue = "new_issue"
    new_status = "new_status"
    new_status_mattermost = "new_status_mattermost"
    new_status_mattermost_without_comment = "new_status_mattermost_without_comment"
    new_comment = "new_comment"
    delete = "delete"
    new_priority = "new_priority"
    clones = "clones"
