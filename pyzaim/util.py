import os
from .exception import *

def get_env(key):
    env = os.getenv(key)
    if env == None or env == "":
        raise EXCEPTION_MAP[key]
    return env
