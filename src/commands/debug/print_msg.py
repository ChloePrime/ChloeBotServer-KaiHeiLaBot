from khl import Bot, Message, MessageTypes

from src.commands._globals import *


def init(bot: Bot, *args):
    listening = [False]

    @bot.command(name="printmsg", help="打印接下来的一条消息", prefixes=UNIFIED_PREFIX, rules=[debug_rule])
    async def print_message(msg: Message):
        """
        打印接下来的一条消息
        """
        await msg.reply("Listening!")
        listening[0] = True

    async def on_chat(msg: Message):
        if not listening[0]:
            return
        listening[0] = False

        await msg.reply(f"content={msg.content},extra={msg.extra}")

    for msg_type in MessageTypes:
        if msg_type == MessageTypes.SYS:
            continue
        bot.client.register(msg_type, on_chat)
