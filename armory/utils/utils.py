import functools
import collections
from pydoc import locate


def rsetattr(obj, attr, val):
    print(f"obj: {obj}, {type(obj)}")
    pre, _, post = attr.rpartition(".")
    print(pre, _, post)
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)


def rgetattr(obj, attr, *args):
    print(f"rgetattr {obj}, {attr}")

    def _getattr(obj, attr):
        print(f"_getattr: {obj}, {type(obj)}")
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split("."))


def rhasattr(obj, attr):
    try:
        left, right = attr.split(".", 1)
    except Exception:
        if isinstance(obj, dict):
            return attr in obj
        else:
            return hasattr(obj, attr)
    if hasattr(obj, left):
        return rhasattr(getattr(obj, left), right)
    else:
        return False


def flatten(d, parent_key="", sep="."):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def parse_overrides(overrides):
    if isinstance(overrides, str):
        output = {i.split()[0]: i.split[1] for i in overrides.split(" ")}
    elif isinstance(overrides, dict):
        output = flatten(overrides)
    elif isinstance(overrides, list) or isinstance(overrides, tuple):
        tmp = [i.split("=") for i in overrides]
        output = {i[0]: i[1] for i in tmp}
    else:
        raise ValueError(f"unexpected format for Overides: {type(overrides)}")
    return output


def set_overrides(obj, overrides):
    overrides = parse_overrides(overrides)
    for k, v in overrides.items():
        if rhasattr(obj, k):
            old_val = rgetattr(obj, k)
            print(type(old_val))
            tp = locate(type(old_val).__name__)
            if tp is not None:
                new_val = tp(v)  # Casting to correct type
            else:
                new_val = v
            rsetattr(obj, k, new_val)
