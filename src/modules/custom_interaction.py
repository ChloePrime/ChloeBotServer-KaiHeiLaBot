from typing import Optional, Callable

from aiohttp import ClientSession
from khl import Bot, Message, MessageTypes
from .. import config
from .. import networking
from ..networking.protocol.constants import *


def _tokenize(msg: str) -> (str, str):
    action = ""
    target = None

    strlen = len(msg)
    for i0 in range(0, strlen):
        i = strlen - i0 - 1
        char = msg[i]
        if char.isspace() or (not char.isascii()):
            action = msg[0:(i + 1)].strip()
            target = msg[(i + 1):]
            break

    return action, target


def _parse(msg: str) -> Optional[tuple[str, str, dict]]:
    action, target = _tokenize(msg)
    if target is None or len(action) == 0:
        return None

    if action[0].isascii():
        # English Action
        fixed_action = (action + "d") if action.endswith('e') else action + "ed"
    else:
        # 动作内容为中文开头
        fixed_action = (action + "了" + action) if len(action) == 1 else action + "了"

    payload = {
        "playerName": target,
        "actionOverload": fixed_action
    }
    return action, target, payload


def _make_handler(session: ClientSession) -> Callable:
    async def on_message(msg: Message):
        # Check whether this is a custom interaction
        # by identifying its prefix.
        required_prefix = config.main.bot.interaction_prefix
        if not msg.content.startswith(required_prefix):
            return

        input_cmd = msg.content[1:].strip()
        params = _parse(input_cmd)

        if params is None:
            return
        _, player_name, payload = params

        await networking.interact_with_player(
            msg, player_name, None, session,
            animation=ANIM_NONE,
            soundFx="minecraft:entity.experience_orb.pickup",
            **payload
        )

    return on_message


def init(bot: Bot, session: ClientSession):
    bot.client.register(MessageTypes.TEXT, _make_handler(session))
