import os
import datetime
import unittest
import time

from tests.util import env

from pyzaim import ZaimAPI, OauthInitializer
from pyzaim.exception import *



class TestAPIInitializer(unittest.TestCase):

    def test_initialize(self):
        old_env = env.save()
        env.reset()
        with self.assertRaises(NoConsumerIDException):
            api = ZaimAPI()
        os.environ['CONSUMER_ID'] = "consumer_id"

        with self.assertRaises(NoConsumerSecretException):
            api = ZaimAPI()
        os.environ['CONSUMER_SECRET'] = "consumer_secret"

        with self.assertRaises(NoAccessTokenException):
            api = ZaimAPI()
        os.environ['ACCESS_TOKEN'] = "access_token"

        with self.assertRaises(NoAccessTokenSecretException):
            api = ZaimAPI()
        os.environ['ACCESS_TOKEN_SECRET'] = "access_token_secret"

        with self.assertRaises(NoOAuthVerifierException):
            api = ZaimAPI()
        os.environ['OAUTH_VERIFIER'] = "oauth_verifier"
    
        env.recover(old_env)

        api = ZaimAPI()
        json = api.verify()
        self.assertEqual(json.get("me").get("name"), os.getenv("USER_ID").split("@")[0])
   
    def test_payment(self):
        """before test, please create account 'wallet' and 'bank' from WEB UI"""
        api = ZaimAPI()
        #insert data
        today = datetime.date.today()
        self.assertEqual(api.insert_payment_simple(today,1000,"食料品").status_code,200)
        self.assertEqual(api.insert_payment_simple(today,1200,"食料品","wallet").status_code,200)
        self.assertEqual(api.insert_payment_simple(today,1300,"インターネット関連費","wallet","test").status_code,200)
        self.assertEqual(api.insert_payment_simple(today,1300,"旅行","bank","test","北海道旅行").status_code,200)
        self.assertEqual(api.insert_payment_simple(today,1300,"食料品","wallet","test","ぱん","コンビニ").status_code,200)
        #get data
        time.sleep(5)
        json = api.get_data()
        #self.assertEqual(len(json),5)
        # update and delete payment
        for data in json:
            self.assertEqual(api.update_payment_simple(data.get("id"),today,"食料品",data.get("amount")+500).status_code,200)
            time.sleep(1)
            self.assertEqual(api.delete_payment(data.get("id")).status_code,200)
        
    def test_income(self):
        api = ZaimAPI() 
        
        today = datetime.date.today()

        #insert income
        self.assertEqual(api.insert_income_simple(today,"給与所得",1000).status_code,200)
        self.assertEqual(api.insert_income_simple(today,"立替金返済",1000,"wallet").status_code,200)
        self.assertEqual(api.insert_income_simple(today,"臨時収入",10000,"bank","test").status_code,200)
        self.assertEqual(api.insert_income_simple(today,"賞与",100000,"bank","test","会社").status_code,200)

        #get data
        time.sleep(5)
        json = api.get_data()
        #self.assertEqual(len(json),4)

        #update and delete
        for data in json:
            self.assertEqual(api.update_income_simple(data.get("id"),today,"給与所得",data.get("amount") + 1000).status_code,200)
            time.sleep(1)
            self.assertEqual(api.delete_income(data.get("id")).status_code,200)

    def test_transfer(self):
        api = ZaimAPI() 
        
        today = datetime.date.today()

        #insert income
        self.assertEqual(api.insert_transfer_simple(today,1000,"bank","wallet").status_code,200)
        self.assertEqual(api.insert_transfer_simple(today,1000,"bank","wallet","test").status_code,200)

        #get data
        time.sleep(5)
        json = api.get_data()
        #self.assertEqual(len(json),2)

        #update and delete
        for data in json:
            self.assertEqual(api.update_transfer_simple(data.get("id"),today,data.get("amount") + 1000,"wallet","bank").status_code,200)
            time.sleep(1)
            self.assertEqual(api.delete_transfer(data.get("id")).status_code,200)


if __name__ == '__main__':
    unittest.main()
