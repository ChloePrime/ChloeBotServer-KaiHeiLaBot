from typing import Callable

from aiohttp import ClientSession
from khl import Bot, MessageTypes, Message

from src import config
from src.networking import *

PREFIX = '/'


def _make_handler(session: ClientSession) -> Callable:
    async def on_message(msg: Message):
        if not msg.content.startswith(PREFIX):
            return

        if not config.can_send_server_command(msg):
            return

        mc_command_body = msg.content[len(PREFIX):]
        await send_server_command(mc_command_body, msg, session)

    return on_message


def init(bot: Bot, session: ClientSession):
    bot.client.register(MessageTypes.KMD, _make_handler(session))
