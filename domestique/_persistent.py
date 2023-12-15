import types

persistent = types.SimpleNamespace()
persistent.data = {}

def get_value(key, default=None):

    return persistent.data.get(key, default)


def set_value(key, value):

    persistent.data[key] = value


def has_value(key):

    return key in persistent.data


set_value("id", "")

