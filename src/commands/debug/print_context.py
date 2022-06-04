from khl import Bot, Message

from src.commands._globals import *


def init(bot: Bot, *args):

    @bot.command(name="printctx", help="打印当前聊天发送者和所在服务器的信息", prefixes=UNIFIED_PREFIX, rules=[debug_rule])
    async def print_context(msg: Message):
        """
        打印当前聊天发送者和所在服务器的信息
        """
        sender = msg.author
        guild = msg.ctx.guild
        await sender.load()
        await guild.load()

        debug_info = f"""User Info:
id: {sender.id}
username: {sender.username}
nickname: {sender.nickname}
identify_num: {sender.identify_num}
status: {sender.status}
roles: {sender.roles}

Guild Info:
id: {guild.id}
name: {guild.name}
topic: {guild.topic}
master_id: {guild.master_id}
icon: {guild.icon}
notify_type: {guild.notify_type}
region: {guild.region}
enable_open: {guild.enable_open}
open_id: {guild.open_id}
default_channel_id: {guild.default_channel_id}
welcome_channel_id: {guild.welcome_channel_id}"""
        await msg.reply(debug_info)
