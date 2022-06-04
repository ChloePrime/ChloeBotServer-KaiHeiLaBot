import json
import logging
import os
from pathlib import Path

from src.util import dynamics


class Config:

    def __init__(self, path: str, default):
        """
        :param default: should not be dynamic object.
        """
        self._path = path
        self._data = default
        self._inited = True

    def __getattr__(self, item):
        """
        Get attr as if `self` is the json object.
        :param item: prop name
        :return: None if not found
        """
        dynamic_data = dynamics.ensure_dynamic(self._data)
        return getattr(dynamic_data, item)

    def __setattr__(self, key, value):
        if not self._inited or key == "_data":
            super.__setattr__(self, key, value)
            return

        dynamic_data = dynamics.ensure_dynamic(self._data)
        setattr(dynamic_data, key, value)

    def reload(self):
        if os.path.exists(self._path):
            # Load existing config
            with open(self._path, mode="r", encoding="utf-8") as fp:
                self._data = json.load(fp)
        else:
            # Write default config
            logging.info(f"Config {self._path} not found, creating one with default values.")
            self.__mkdirparent()

            with open(self._path, mode="w", encoding="utf-8") as fp:
                json.dump(self._data, fp, indent=4, sort_keys=True, ensure_ascii=False)

    def save(self):
        self.__mkdirparent()

        if os.path.exists(self._path):
            with open(self._path, mode="rb") as fp:
                old = fp.read()
        else:
            old = None

        try:
            # Save json
            with open(self._path, mode="w", encoding="utf-8") as fp:
                json.dump(self._data, fp, indent=4, sort_keys=True, ensure_ascii=False)
        except Exception as ex:
            logging.error(f"Exception when saving config {self._path}", exc_info=ex)
            # Rollback when error happens.
            if old is None:
                return
            with open(self._path, mode="wb") as fp:
                fp.write(old)

    def __mkdirparent(self):
        folder = str(Path(self._path).parent)
        if not os.path.exists(folder):
            os.makedirs(folder)

    # _data: Non-dynamic dict|list
    _path: str
    _inited = False
