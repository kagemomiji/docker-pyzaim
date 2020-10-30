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

import time
import os

from requests_oauthlib import OAuth1Session

from .exception import *
from . import util

#CONSTANT_VALUE

API_BASE_URL = "https://api.zaim.net/v2"
VERIFY_URL = API_BASE_URL + "/home/user/verify"
MONEY_URL = API_BASE_URL + "/home/money"
PAYMENT_URL = API_BASE_URL + "/home/money/payment"
INCOME_URL = API_BASE_URL + "/home/money/income"
TRANSFER_URL = API_BASE_URL + "/home/money/transfer"
CATEGORY_URL = API_BASE_URL + "/home/category"
GENRE_URL = API_BASE_URL + "/home/genre"
ACCOUNT_URL = API_BASE_URL + "/home/account"
CURRENCY_URL = API_BASE_URL + "/currency"
CALLBACK_URI = "https://www.zaim.net/"

class ZaimAPI:
    def __init__(self):
        self.consumer_id = util.get_env("CONSUMER_ID")
        self.consumer_secret = util.get_env("CONSUMER_SECRET")
        access_token = util.get_env("ACCESS_TOKEN")
        access_token_secret = util.get_env("ACCESS_TOKEN_SECRET")
        oauth_verifier = util.get_env("OAUTH_VERIFIER")

        self.auth = OAuth1Session(
            client_key=self.consumer_id,
            client_secret=self.consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
            callback_uri=CALLBACK_URI,
            verifier=oauth_verifier,
        )
        self._build_id_table()


    def verify(self):
        return self.auth.get(VERIFY_URL).json()

    def get_data(self):
        return self.auth.get(MONEY_URL).json()["money"]

    def insert_payment_simple(
        self,
        date,
        amount,
        genre,
        from_account=None,
        comment=None,
        name=None,
        place=None,
    ):
        genre_id = self.genre_stoi[genre]
        category_id = self.genre_to_category[genre_id]
        if from_account is not None:
            from_account_id = self.account_stoi[from_account]
        else:
            from_account_id = None
        return self.insert_payment(
            date, amount, category_id, genre_id, from_account_id, comment, name, place
        )

    def insert_payment(
        self,
        date,
        amount,
        category_id,
        genre_id,
        from_account_id=None,
        comment=None,
        name=None,
        place=None,
    ):
        data = {
            "mapping": 1,
            "category_id": category_id,
            "genre_id": genre_id,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
        }
        if from_account_id is not None:
            data["from_account_id"] = from_account_id
        if comment is not None:
            data["comment"] = comment
        if name is not None:
            data["name"] = name
        if place is not None:
            data["place"] = place
        return self.auth.post(PAYMENT_URL, data=data)

    def update_payment_simple(
        self,
        data_id,
        date,
        genre,
        amount,
        from_account=None,
        comment=None,
        name=None,
        place=None,
    ):
        genre_id = self.genre_stoi[genre]
        category_id = self.genre_to_category[genre_id]
        if from_account is not None:
            from_account_id = self.account_stoi[from_account]
        else:
            from_account_id = None
        return self.update_payment(
            data_id,
            date,
            amount,
            category_id,
            genre_id,
            from_account_id,
            comment,
            name,
            place,
        )

    def update_payment(
        self,
        data_id,
        date,
        amount,
        category_id,
        genre_id,
        from_account_id=None,
        comment=None,
        name=None,
        place=None,
    ):
        data = {
            "mapping": 1,
            "id": data_id,
            "category_id": category_id,
            "genre_id": genre_id,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
        }
        if from_account_id is not None:
            data["from_account_id"] = from_account_id
        if comment is not None:
            data["comment"] = comment
        if name is not None:
            data["name"] = name
        if place is not None:
            data["place"] = place
        return self.auth.put("{}/{}".format(PAYMENT_URL, data_id), data=data)

    def delete_payment(self, data_id):
        return self.auth.delete("{}/{}".format(PAYMENT_URL, data_id))

    def insert_income_simple(
        self, date, category, amount, to_account=None, comment=None, place=None
    ):
        category_id = self.category_stoi[category]
        if to_account is not None:
            to_account_id = self.account_stoi[to_account]
        else:
            to_account_id = None
        return self.insert_income(
            date, category_id, amount, to_account_id, comment, place
        )

    def insert_income(
        self, date, category_id, amount, to_account_id=None, comment=None, place=None
    ):
        data = {
            "mapping": 1,
            "category_id": category_id,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
        }
        if to_account_id is not None:
            data["to_account_id"] = to_account_id
        if comment is not None:
            data["comment"] = comment
        if place is not None:
            data["place"] = place
        return self.auth.post(INCOME_URL, data=data)

    def update_income_simple(
        self, data_id, date, category, amount, to_account=None, comment=None, place=None
    ):
        category_id = self.category_stoi[category]
        if to_account is not None:
            to_account_id = self.account_stoi[to_account]
        else:
            to_account_id = None
        return self.update_income(
            data_id, date, category_id, amount, to_account_id, comment, place
        )

    def update_income(
        self,
        data_id,
        date,
        category_id,
        amount,
        to_account_id=None,
        comment=None,
        place=None,
    ):
        data = {
            "mapping": 1,
            "id": data_id,
            "category_id": category_id,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
        }
        if to_account_id is not None:
            data["to_account_id"] = to_account_id
        if comment is not None:
            data["comment"] = comment
        if place is not None:
            data["place"] = place
        return self.auth.put("{}/{}".format(INCOME_URL, data_id), data=data)

    def delete_income(self, data_id):
        return self.auth.delete("{}/{}".format(INCOME_URL, data_id))

    def insert_transfer_simple(
        self, date, amount, from_account, to_account, comment=None
    ):
        from_account_id = self.account_stoi[from_account]
        to_account_id = self.account_stoi[to_account]
        return self.insert_transfer(
            date, amount, from_account_id, to_account_id, comment
        )

    def insert_transfer(
        self, date, amount, from_account_id, to_account_id, comment=None
    ):
        data = {
            "mapping": 1,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
            "from_account_id": from_account_id,
            "to_account_id": to_account_id,
        }
        if comment is not None:
            data["comment"] = comment
        return self.auth.post(TRANSFER_URL, data=data)

    def update_transfer_simple(
        self, data_id, date, amount, from_account, to_account, comment=None
    ):
        from_account_id = self.account_stoi[from_account]
        to_account_id = self.account_stoi[to_account]
        return self.update_transfer(
            data_id, date, amount, from_account_id, to_account_id, comment
        )

    def update_transfer(
        self, data_id, date, amount, from_account_id, to_account_id, comment=None
    ):
        data = {
            "mapping": 1,
            "id": data_id,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
            "from_account_id": from_account_id,
            "to_account_id": to_account_id,
        }
        if comment is not None:
            data["comment"] = comment
        return self.auth.put("{}/{}".format(TRANSFER_URL, data_id), data=data)

    def delete_transfer(self, data_id):
        return self.auth.delete("{}/{}".format(TRANSFER_URL, data_id))

    def _build_id_table(self):
        self.genre_itos = {}
        self.genre_stoi = {}
        self.genre_to_category = {}
        genre = self._get_genre()["genres"]
        for g in genre:
            self.genre_itos[g["id"]] = g["name"]
            self.genre_stoi[g["name"]] = g["id"]
            self.genre_to_category[g["id"]] = g["category_id"]
        self.category_itos = {}
        self.category_stoi = {}
        category = self._get_category()["categories"]
        for c in category:
            self.category_itos[c["id"]] = c["name"]
            self.category_stoi[c["name"]] = c["id"]
        self.account_stoi = {}
        self.account_itos = {}
        account = self._get_account()["accounts"]
        for a in account:
            self.account_itos[a["id"]] = a["name"]
            self.account_stoi[a["name"]] = a["id"]

    def _get_account(self):
        return self.auth.get(ACCOUNT_URL).json()

    def _get_category(self):
        return self.auth.get(CATEGORY_URL).json()

    def _get_genre(self):
        return self.auth.get(GENRE_URL).json()
