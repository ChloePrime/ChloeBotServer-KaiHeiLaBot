from aiohttp import ClientSession
from khl import Bot

from . import reload_config
from .minecraft import interactions, show_tps, list_players, choose_server, bal, server_cmd_auth
from .debug import print_context, print_msg


def init(bot: Bot, session: ClientSession):
    for cmd in (
            reload_config,
            bal,
            choose_server,
            interactions,
            list_players,
            server_cmd_auth,
            show_tps,
            print_context,
            print_msg,
    ):
        cmd.init(bot, session)
