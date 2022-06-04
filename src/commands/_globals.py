from khl import Message

from .. import config

UNIFIED_PREFIX = ['.', '。']


def debug_rule(_) -> bool:
    return config.main.debug


def require_authorized_rule(msg: Message):
    return config.is_authorized(msg.author)
