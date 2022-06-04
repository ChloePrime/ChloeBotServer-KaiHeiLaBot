import logging

from khl import User

from src.util import dynamics
from .config import Config
from . import defaults
from . import runtime_configs

main = Config("./config/main.json", defaults.main)
messages = Config("./config/messages.json", defaults.messages)
images = Config("./config/images.json", defaults.images)
config_list = [main, messages, images, runtime_configs.server_command]


def is_authorized(usr: User) -> bool:
    def ensure_auth_list_is_set():
        alist = dynamics.unwrap(main.authorized_users)
        if isinstance(alist, list):
            main.authorized_users = set(alist)

    ensure_auth_list_is_set()
    auth_list = main.authorized_users
    return int(usr.id) in auth_list


def init():
    logging.info("Loading config...")

    for cfg in config_list:
        cfg.reload()

    logging.info("Complete!")


def reload_all():
    logging.info("Reloading config...")

    for cfg in config_list:
        cfg.reload()

    logging.info("Complete!")
