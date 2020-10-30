

class NoConsumerIDException(Exception):
    """EnvironmentValueにCONSUMER_IDが無いときの例外"""
    pass

class NoConsumerSecretException(Exception):
    """EnvironmentValueにCONSUMER_SECRETが無いときの例外"""
    pass

class NoUserIDException(Exception):
    """EnvironmentValueにUSER_IDが無いときの例外"""
    pass

class NoUserPasswordException(Exception):
    """EnvironmentValueにUSER_PASSWORDが無いときの例外"""
    pass

class NoAccessTokenException(Exception):
    """EnvironmentValueにACCESS_TOKENが無いときの例外"""
    pass

class NoAccessTokenSecretException(Exception):
    """EnvironmentValueにACCESS_TOKEN_SECRETが無いときの例外"""
    pass

class NoOAuthVerifierException(Exception):
    """EnvironmentValueにOAUTH_VERIFIERが無いときの例外"""
    pass

MESSAGE_PREFIX = "Set Environment Value: "

EXCEPTION_MAP = { 
        "CONSUMER_ID": NoConsumerIDException( MESSAGE_PREFIX + "CONSUMER_ID"),
        "CONSUMER_SECRET": NoConsumerSecretException( MESSAGE_PREFIX + "CONSUMER_SECRET"),
        "USER_ID": NoUserIDException( MESSAGE_PREFIX + "USER_ID"),
        "USER_PASSWORD": NoUserPasswordException( MESSAGE_PREFIX + "USER_PASSWORD"),
        "OAUTH_VERIFIER": NoOAuthVerifierException( MESSAGE_PREFIX + "OAUTH_VERIFIER"),
        "ACCESS_TOKEN": NoAccessTokenException( MESSAGE_PREFIX + "ACCESS_TOKEN"),
        "ACCESS_TOKEN_SECRET": NoAccessTokenSecretException( MESSAGE_PREFIX + "ACCESS_TOKEN_SECRET")
}

