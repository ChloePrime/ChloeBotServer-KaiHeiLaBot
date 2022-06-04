from khl import Bot

from .._globals import *
from src import config, networking


def init(bot: Bot, *_):

    @bot.command(name="server", rules=[require_authorized_rule], prefixes=UNIFIED_PREFIX)
    async def choose_server(msg: Message, server_name: str = ""):
        """
        Choose minecraft server for current KHL channel.
        """
        messages = config.messages

        if len(server_name) == 0:
            # Query current server
            cur_server = networking.get_cur_server(msg)
            reply = messages.get_cur_server.format(cur_server)
            await msg.reply(reply)
            return

        # Set to default
        if server_name == "-reset":
            networking.del_cur_server(msg)
            reply = messages.del_cur_server

            await msg.reply(reply)
            return

        # Set current server
        success = networking.set_cur_server(msg, server_name)
        reply_format: str = messages.set_cur_server if success else messages.set_cur_server_failed
        await msg.reply(reply_format.format(server_name))
