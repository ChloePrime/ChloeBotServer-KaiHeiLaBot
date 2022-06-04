import json
from typing import Callable


def from_json_str(content, *args, **kwargs):
    obj = json.loads(content, *args, **kwargs)
    return ensure_dynamic(obj)


def from_json_file(fp, *args, **kwargs):
    obj = json.load(fp, *args, **kwargs)
    return ensure_dynamic(obj)


def ensure_dynamic(_obj):
    if isinstance(_obj, dict):
        return DynamicObject(_obj)
    if isinstance(_obj, list):
        return DynamicList(_obj)
    else:
        return _obj


def unwrap(_obj):
    if isinstance(_obj, (DynamicObject, DynamicList)):
        return _obj.delegate

    return _obj


class DynamicObject:
    """
    Dictionary that supports 'object.prop' style.
    """

    def __init__(self, delegate: dict):
        self.delegate = delegate
        self.inited = True

    def __getattr__(self, key):
        try:
            value = self.delegate[key]
        except KeyError:
            raise AttributeError

        return ensure_dynamic(value)

    def __setattr__(self, key, value):
        if not self.inited:
            super.__setattr__(self, key, value)
            return

        unwrapped_value = unwrap(value)
        self.delegate[key] = unwrapped_value
    
    def get(self, key, default=None):
        value = self.delegate.get(key)
        return ensure_dynamic(value) if value is not None else ensure_dynamic(default)

    delegate: dict
    inited = False


class DynamicList:
    def __init__(self, delegate: list):
        self.delegate = delegate

    def __getitem__(self, key):
        return ensure_dynamic(self.delegate[key])

    def __setitem__(self, key, value):
        self.delegate[key] = unwrap(value)

    def __len__(self):
        return len(self.delegate)

    def __iter__(self):
        return (ensure_dynamic(o) for o in self.delegate)

    def sort(self, key: Callable, reverse=False):
        def wrapped_key(item):
            return key(ensure_dynamic(item))

        self.delegate.sort(key=wrapped_key, reverse=reverse)

    delegate: list
