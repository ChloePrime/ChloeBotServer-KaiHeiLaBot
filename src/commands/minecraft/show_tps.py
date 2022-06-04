import base64
import logging
import os
import tempfile

from aiohttp import ClientSession
from khl import Bot, Message, MessageTypes

from .._globals import UNIFIED_PREFIX
from src import config
from src import networking
from src.networking.protocol.constants import *
from src.util import badgemaker


def _file_to_logo_str(fpath) -> str:
    with open(fpath, mode="rb") as fp:
        b64 = base64.b64encode(fp.read()).decode("utf-8")
        logging.debug(f'badge logo {fpath} encoded to "{b64}"')
        return "data:image/png;base64," + b64


def init(bot: Bot, session: ClientSession):

    good_tps = _file_to_logo_str(config.images.tps.normal)
    potato = _file_to_logo_str(config.images.tps.potato)
    baked_potato = _file_to_logo_str(config.images.tps.baked_potato)

    @bot.command(name="tps", aliases=["好卡的服", "好卡の服"], prefixes=UNIFIED_PREFIX)
    async def show_tps(msg: Message):
        """
        A   > .tps
        Bot > 土豆性能状态: 1.5 tps (666.67 mspt)
        A   > 好卡的服啊
        B   > 土豆熟啦！
        """
        operation = (REQ_OP_USER_COMMAND, USERCMD_TPS)
        tps_info = await networking.send_req(msg, operation, session)

        if tps_info is None:
            return

        tps = tps_info.tps
        mspt = tps_info.mspt

        badge_color = "brightgreen"
        logo = good_tps

        if tps < 10:
            badge_color = "red"
            logo = baked_potato
        elif tps < 15:
            badge_color = "yellow"
            logo = potato

        tps_badge = await badgemaker.make("TPS", "%.2f" % tps, badge_color, session, logo=logo)
        mspt_badge = await badgemaker.make("mspt", "%.2f" % mspt, badge_color, session)
        reply_img = badgemaker.join(tps_badge, mspt_badge, margin=4)

        tmp_file, fpath = tempfile.mkstemp(suffix=".png")
        try:
            # Save image to a file
            with os.fdopen(tmp_file, "wb+") as fp:
                reply_img.save(fp, format="png")

            # Upload and reply
            reply_url = await bot.upload_asset(fpath)
            await msg.ctx.channel.send(reply_url, type=MessageTypes.IMG)
        finally:
            os.remove(fpath)
