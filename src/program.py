import asyncio
import logging
import os
import time

from aiohttp import ClientSession
from khl import Bot

from . import config
from . import commands
from .modules import custom_interaction, server_command


def setup_logger():
    log_dir = "./logs/"
    log_name = time.strftime("%Y-%m-%d %H.%M.%S.log", time.localtime())
    log_file = os.path.join(log_dir, log_name)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(filename=log_file, level=logging.INFO)


def init_modules(bot, session):
    for module in (
        custom_interaction,
        server_command
    ):
        module.init(bot, session)


def main():
    # init Program
    setup_logger()
    config.init()
    # init Bot
    bot = Bot(token=config.main.bot.token)

    shared_session = None
    try:
        shared_session = ClientSession()

        commands.init(bot, shared_session)
        init_modules(bot, shared_session)
        # everything done, go ahead now!
        bot.run()
        # now invite the bot to a server, and send '/hello' in any channel
        # (remember to grant the bot with read & send permissions)
    finally:
        if shared_session is not None:
            asyncio.run(shared_session.close())


if __name__ == '__main__':
    main()
