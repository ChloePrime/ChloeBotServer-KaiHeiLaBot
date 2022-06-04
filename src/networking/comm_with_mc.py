import json
import logging
from http import HTTPStatus
from typing import Any, Optional

from aiohttp import *
from khl import Message

from .protocol.constants import *
from .. import config
from ..util import dynamics

# 临时兼容措施:
# 将开黑啦ID加上此数后作为QQ号/QQ群号传给MC侧。
ID_MASK = 1_000_000_000_000_000_000

# Channel ID -> (Port, Config Name)
server_by_channel: dict[int, tuple[int, str]] = {}


def get_cur_server(inp: Message) -> str:
    channel_id = int(inp.ctx.channel.id)
    selected = server_by_channel.get(channel_id)

    return "@Default" if selected is None else selected[1]


def set_cur_server(inp: Message, server_name: Optional[str], cfg=config.main) -> bool:
    """
    :return: Does the set operation succeed?
    """
    rec = cfg.mc.server_list.get(server_name)

    if rec is None:
        return False

    channel_id = int(inp.ctx.channel.id)
    server_by_channel[channel_id] = (rec.port, server_name)
    return True


def del_cur_server(inp: Message) -> bool:
    """
    :return: Whether there is an override on the server before.
    """
    channel_id = int(inp.ctx.channel.id)

    existed_before = channel_id in server_by_channel.keys()
    del server_by_channel[channel_id]

    return existed_before


def choose_server(inp: Message, cfg=config.main) -> int:
    """
    :return: port of the selected server
    """
    channel_id = int(inp.ctx.channel.id)
    selected = server_by_channel.get(channel_id)

    if selected is not None:
        return selected[0]

    return cfg.mc.default_port


async def send_req(
        source_msg: Message,
        operation: (str, str),
        http_client: ClientSession,
        payload: Optional[list | dict] = None,
        app_config=config.main,
        ret_type="json"
) -> Any | None:
    """
    :return: A dynamic object if nothing goes wrong, elsewhere returns ``None``
    """
    guild = source_msg.ctx.guild
    # Construct request data
    qid = int(source_msg.author.id) + ID_MASK
    qq_group = (-1 if guild is None else int(guild.id)) + ID_MASK
    payload_text = None if payload is None else json.dumps(payload, ensure_ascii=False)
    req = {
        "user": qid,
        "group": qq_group,
        "operation": operation[0],
        "msg": operation[1],
        "msgContext": payload_text
    }
    req_json = json.dumps(req, ensure_ascii=False)
    # send request
    port = choose_server(source_msg, app_config)
    try:
        resp = await http_client.post(f"http://localhost:{port}", data=req_json)
        if resp.status == HTTPStatus.OK:
            # Everything OK, decode the response content.
            if ret_type == "json":
                resp_obj = await resp.json(encoding="utf-8", content_type=None)
                resp_obj = dynamics.ensure_dynamic(resp_obj)
            else:
                resp_obj = await resp.text(encoding="utf-8")
            return resp_obj

        elif config.main.debug:
            # Print response code to chatting when debug mode is on
            await source_msg.reply(f"DEBUG: Server responded {resp.status}")

        elif resp.status == HTTPStatus.FORBIDDEN:
            # Access denied -> NO-OP
            pass

        else:
            # Log other situations
            logging.warning(f"Server responded {resp.status} when executing command.")
    except Exception as err:
        logging.warning(f"Exception executing bot command:\n{err}")
        await source_msg.reply(config.messages.on_cmd_error)

    return None


async def send_server_command(cmd: str, reply_handle: Message, session: ClientSession):
    operation = (REQ_OP_SERVER_COMMAND, cmd)

    resp = await send_req(reply_handle, operation, session, ret_type="str")
    reply = config.messages.server_cmd_success if (resp is None or len(resp) == 0) else resp
    await reply_handle.reply(reply)
