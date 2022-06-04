import copy
import json

from aiohttp import ClientSession
from khl import Bot, Message

from .._globals import UNIFIED_PREFIX
from src import config, networking
from src.networking.protocol.constants import *

card_template = json.loads("""
[
  {
    "type": "card",
    "size": "lg",
    "theme": "warning",
    "modules": [
      {
        "type": "header",
        "text": {
          "type": "plain-text",
          "content": "服务器玩家信息"
        }
      },
      {
        "type": "divider"
      },
      {
        "type": "section",
        "accessory": {},
        "text": {
          "type": "paragraph",
          "cols": 3,
          "fields": [
            {
              "type": "kmarkdown",
              "content": "**当前人数**"
            },
            {
              "type": "kmarkdown",
              "content": "**人数上限**"
            },
            {
              "type": "kmarkdown",
              "content": ""
            },
            {
              "type": "kmarkdown",
              "content": "20"
            },
            {
              "type": "kmarkdown",
              "content": "120"
            },
            {
              "type": "kmarkdown",
              "content": ""
            }
          ]
        }
      },
      {
        "type": "divider"
      },
      {
        "type": "header",
        "text": {
          "type": "plain-text",
          "content": "玩家列表"
        }
      },
      {
        "type": "section",
        "accessory": {},
        "text": {
          "type": "paragraph",
          "cols": 3,
          "fields": [
            {
              "type": "kmarkdown",
              "content": "** 昵称**"
            },
            {
              "type": "kmarkdown",
              "content": "** Ping**"
            },
            {
              "type": "kmarkdown",
              "content": "** 位置**"
            }
          ]
        }
      }
    ]
  }
]
""")

record_template = [
    {
        "type": "kmarkdown",
        "content": "玩家名称"
    },
    {
        "type": "kmarkdown",
        "content": ""
    },
    {
        "type": "kmarkdown",
        "content": ""
    }
]


def _insert_record(card: dict, records: list[str]):
    """
    :param records: [str, str, str]
    """
    record_elements = copy.deepcopy(record_template)
    for i in range(len(records)):
        record_elements[i]["content"] = records[i]

    record_list: list = card["modules"][5]["text"]["fields"]
    record_list.extend(record_elements)


def _format_player_ping(ping_in_millis) -> str:
    if ping_in_millis is None:
        return "Unknown"

    return str(ping_in_millis) + "ms"


def _format_player_location(pos_record) -> str:
    if pos_record is None:
        return "Unknown"

    raw_world_name = pos_record.wname
    world_name = config.messages.world_names.get(raw_world_name, raw_world_name)

    # return f"{world_name}的({pos_record.x:.0f}, {pos_record.y:.0f}, {pos_record.z:.0f})"
    return world_name


def init(bot: Bot, session: ClientSession):
    @bot.command(name="list", aliases=["服务器状态", "土豆状态", "破推头状态"], prefixes=UNIFIED_PREFIX)
    async def list_players(msg: Message):
        # Query info from Minecraft
        operation = (REQ_OP_USER_COMMAND, USERCMD_LIST_PLAYER)
        resp = await networking.send_req(msg, operation, session)

        # Prepare card
        cards = copy.deepcopy(card_template)
        card = cards[0]

        # Insert server info
        server_info_section = card["modules"][2]["text"]["fields"]
        server_info_section[3]["content"] = str(len(resp.entries))
        server_info_section[4]["content"] = str(resp.capacity)

        # Insert sorted player list
        player_list = resp.entries
        player_list.sort(key=(lambda rec: rec.name.lower()))

        joined_column = [
            "\n".join(rec.name for rec in player_list),
            "\n".join(_format_player_ping(rec.get("ping")) for rec in player_list),
            "\n".join(_format_player_location(rec.get("loc")) for rec in player_list)
        ]
        _insert_record(card, joined_column)

        # Serialize and reply
        await msg.reply(cards)
