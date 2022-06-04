from typing import Optional

from aiocache import cached
from aiohttp import ClientSession
from khl import Message, Guild

from .. import config
from .. import networking
from ..networking.protocol.constants import *


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


def _get_cache_key(_, res: Guild):
    return res.id


@cached(ttl=120, key_builder=_get_cache_key)
async def _get_guild_name(guild: Guild) -> str:
    """
    Get server name (cached)
    """
    await guild.load()
    return guild.name


async def interact_with_player(
        msg: Message, player_name, text: Optional[str], http_client: ClientSession,
        **payload
):
    guild_name = await _get_guild_name(msg.ctx.guild)

    payload.update(
        userName=msg.author.nickname,
        groupName=guild_name,
        playerName=player_name
    )

    if text is not None:
        payload["text"] = text

    # Set default animation to 0
    if "animation" not in payload:
        payload["animation"] = 0

    req_op = (REQ_OP_USER_COMMAND, USERCMD_INTERACTION)
    resp = await networking.send_req(msg, req_op, http_client, payload=payload)

    action = payload.get("actionOverload")
    player_name = payload.get("playerName")
    feedback = _get_reply_format(action, resp.errorCode)

    reply = feedback.format(action, player_name)
    await msg.reply(reply)
