from aiohttp import ClientSession
from khl import Bot, Message

from src import networking
from .._globals import UNIFIED_PREFIX


def init(bot: Bot, session: ClientSession):
    @bot.command(name="bal", prefixes=UNIFIED_PREFIX)
    async def bal(msg: Message, target: str):
        """
        .bal
        查看谁是资本家
        """
        server_cmd = "bal " + target
        await networking.send_server_command(server_cmd, msg, session)
