from khl import Message

from .config import Config

server_command_default = {
    # List[int]
    "authorized": []
}
server_command = Config("./data/server_cmd.json", server_command_default)


def can_send_server_command(msg: Message):
    # list to set
    if not isinstance(server_command.authorized, set):
        server_command.authorized = set(server_command.authorized)
    return int(msg.author_id) in server_command.authorized
