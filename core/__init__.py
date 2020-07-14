from __future__ import absolute_import, unicode_literals

import os
import inspect
import dotenv
from .celery import app as celery_app


try:
    inspect_file = inspect.getfile(inspect.currentframe())
    env_path = os.path.dirname(os.path.abspath(inspect_file))
    env_file = "{}/../.env".format(env_path,)

    if os.path.exists(env_file):
        dotenv.load_dotenv(env_file)
except Exception as e:
    pass


def get_env(name, default=None):
    if name in os.environ:
        return os.environ[name] if os.environ[name] != 'None' else None

    return default


def get_env_bool(name, default=False):
    value = get_env(name, default)

    if value is None:
        return None

    return value == 'True'


from core.handlers import *  # noqa

__all__ = ('celery_app', 'get_env', 'get_env_bool')
