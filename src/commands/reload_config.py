from khl import Bot

from ._globals import *
from .. import config


def init(bot: Bot, *_):

    @bot.command(name="reload", rules=[require_authorized_rule], prefixes=UNIFIED_PREFIX)
    async def reload(msg: Message):
        """
        Reload all configs
        """
        config.reload_all()
        await msg.reply('Reload Complete!')
