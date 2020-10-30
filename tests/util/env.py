import os
ENV_LIST = ["USER_ID","USER_PASSWORD","CONSUMER_ID","CONSUMER_SECRET","ACCESS_TOKEN","ACCESS_TOKEN_SECRET","OAUTH_VERIFIER"]

def reset():
    for env in ENV_LIST:
        if(os.environ.get(env) is not None):
            os.environ.pop(env)

def save():
    map = {}
    for env in ENV_LIST:
        if(os.environ.get(env) is not None):
            map[env] = os.environ.get(env)
    return map

def recover(map):
    for key in map.keys():
        os.environ[key] = map[key]

