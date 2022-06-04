from typing import Optional

from aiohttp import ClientSession
from khl import Bot, Message

from .._globals import UNIFIED_PREFIX
from src import config
from src import networking
from src.networking.protocol.constants import *


def _get_reply_format(action: Optional[str], resp_code: int) -> str:
    if resp_code == PAT_SUCCESS:
        if action is not None and len(action) > 0:
            return config.messages.pat.successful_pat
        else:
            return config.messages.pat.successful_tell
    elif resp_code == PAT_OFFLINE_PLAYER:
        return config.messages.pat.player_is_offline
    else:
        raise ValueError(f".pat got unknown response {resp_code}")


def init(bot: Bot, session: ClientSession):

    @bot.command(
        name="pat",
        aliases=["拍一拍", "戳一戳"],
        prefixes=UNIFIED_PREFIX
    )
    async def pat(msg: Message, player: str, text: str = None):
        await networking.interact_with_player(
            msg, player, text, session,
            animation=ANIM_SHAKE_SCREEN,
            actionOverload="拍了拍",
            soundFx="minecraft:entity.creeper.hurt",
        )

    @bot.command(
        name="prpr",
        aliases=["舔一舔"],
        prefixes=UNIFIED_PREFIX
    )
    async def prpr(msg: Message, player: str, text: str = None):
        await networking.interact_with_player(
            msg, player, text, session,
            actionOverload="舔了舔",
            soundFx="customnpcs:human.girl.villager.heh",
        )

    @bot.command(
        name="tell",
        aliases=["msg", "m"],
        prefixes=UNIFIED_PREFIX
    )
    async def tell(msg: Message, player: str, text: str):
        await networking.interact_with_player(
            msg, player, text, session,
            actionOverload="",
            soundFx="customnpcs:human.female.villager.uhuh",
        )
