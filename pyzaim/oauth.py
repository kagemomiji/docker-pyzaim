# -*- coding: utf-8 -*-

######################################################################
#
# pyzaim
#
# Copyright (c) 2019 reeve0930
#
# This software is released under the MIT License.
# https://github.com/reeve0930/pyzaim/blob/master/LICENSE
#
######################################################################

import datetime
import time
import os

from .exception import * 
from .crawler import ZaimCrawler
from . import util

from requests_oauthlib import OAuth1Session

API_BASE_URL = "https://api.zaim.net/v2"
REQUEST_TOKEN_URL = "https://api.zaim.net/v2/auth/request"
AUTHORIZE_URL = "https://auth.zaim.net/users/auth"
ACCESS_TOKEN_URL = "https://api.zaim.net/v2/auth/access"
CALLBACK_URI = "https://www.zaim.net/"


class OauthInitializer():
    def __init__(self):
        self.consumer_id = util.get_env("CONSUMER_ID")
        self.consumer_secret = util.get_env("CONSUMER_SECRET")
        self.oauth_verifier = ""
        self.access_token = ""
        self.access_token_secret = ""
        

    def authentication(self):

        auth = OAuth1Session(
            client_key=self.consumer_id, client_secret=self.consumer_secret, callback_uri=CALLBACK_URI
        )

        auth.fetch_request_token(REQUEST_TOKEN_URL)

        # Redirect user to zaim for authorization
        authorization_url = auth.authorization_url(AUTHORIZE_URL)

        # crawling by ZaimCrawler and get verifier
        crawler = ZaimCrawler()

        try:
            self.oauth_verifier = crawler.get_oauth_verifier(authorization_url)
        finally:
            crawler.close()

        access_token_res = auth.fetch_access_token(
            url=ACCESS_TOKEN_URL, verifier=self.oauth_verifier
        )
        self.access_token = access_token_res.get("oauth_token")
        self.access_token_secret = access_token_res.get("oauth_token_secret")

        print("\n")
        print("access token : {}".format(self.access_token))
        print("access token secret : {}".format(self.access_token_secret))
        print("oauth verifier : {}".format(self.oauth_verifier))


   
    def get_consumer_id(self):
        return self.consumer_id

    def get_consumer_secret(self):
        return self.consumer_secret
    
    def get_access_token(self):
        return self.access_token
    
    def get_oauth_verifier(self):
        return self.oauth_verifier
    
    def get_access_token_secret(self):
        return self.access_token_secret

