import datetime
import unittest
import os

from tests.util import env
from pyzaim import ZaimCrawler, ZaimAPI
from pyzaim.exception import *


class TestCrawler(unittest.TestCase):
    def test_initialize(self):

        # reset environment value
        old_env = env.save()
        env.reset()

        # USER ID Exception
        with self.assertRaises(NoUserIDException):
            crawler = ZaimCrawler()
            crawler.close()

        os.environ["USER_ID"]  = old_env.get("USER_ID")

        # USER PASSWORD EXCEPTION
        with self.assertRaises(NoUserPasswordException):
            crawler = ZaimCrawler()
            crawler.close()

        env.recover(old_env)
    
    def test_get_data_10(self):

        #Input Test Data
        today = datetime.date.today()

        api = ZaimAPI()
        for i in range(20):
            api.insert_payment_simple(today,100*(i + 1),"食料品")

        # init crawler
        crawler = ZaimCrawler()

        # assert 
        self.assertEqual(len(crawler.get_data(today.year,today.month)) , 10)
        
        #clear test data
        #get data
        json = api.get_data()

        #delete payment
        for data in json:
            api.delete_payment(data.get("id"))
        
        #close crawler
        crawler.close()


    def test_get_data_20(self):

        #Input Test Data
        today = datetime.date.today()

        api = ZaimAPI()
        for i in range(20):
            api.insert_payment_simple(today,100*(i + 1),"食料品")

        # init crawler
        crawler = ZaimCrawler()

        # assert 
        self.assertEqual(len(crawler.get_data(today.year,today.month,20)) , 20)

        #clear test data
        #get data
        json = api.get_data()

        #delete payment
        for data in json:
            api.delete_payment(data.get("id"))
        
        #close crawler
        crawler.close()


