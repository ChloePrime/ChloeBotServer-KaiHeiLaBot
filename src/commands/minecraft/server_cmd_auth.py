from aiohttp import ClientSession
from khl import Bot, Message, PublicMessage

from src import config, networking
from .._globals import UNIFIED_PREFIX


def init(bot: Bot, session: ClientSession):

    @bot.command(name="server_cmd_auth", prefixes=UNIFIED_PREFIX)
    async def server_cmd_auth(msg: Message, target: str):
        if (not isinstance(msg, PublicMessage)) or (not config.can_send_server_command(msg)):
            return

        if len(msg.mention) == 0:
            await msg.reply(config.messages.server_cmd_auth_needs_at)
            return

        cfg = config.server_command
        for mentioned in msg.mention:
            cfg.authorized.add(int(mentioned))

        cfg.authorized = list(cfg.authorized)
        cfg.save()

        await msg.reply(config.messages.server_cmd_auth_success)
