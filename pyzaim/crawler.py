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

import urllib.parse

import chromedriver_binary
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

from .exception import NoUserIDException, NoUserPasswordException
from . import util

class ZaimCrawler:

    # BASE_WINDOW_HEIGHT is height of driver which obtain 10 records  
    WINDOW_WIDTH = 480
    MIN_WINDOW_HEIGHT = 270
    MIN_RECORD_NUM = 10
    AUTH_URL="https://auth.zaim.net/"
    HOME_URL="https://zaim.net/home"

    def __init__(self, timeout = 10):

        #get environment value
        user_id = util.get_env("USER_ID")
        password = util.get_env("USER_PASSWORD")

        #set chrome options
        options = ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9223")
        options.add_argument("--headless")

        #create chrome driver
        self.driver = Chrome(options=options)

        #print("Start Chrome Driver.")
        #print("Login to Zaim.")

        self.driver.get(self.AUTH_URL)
        time.sleep(3)

        self.driver.find_element_by_id("UserEmail").send_keys(user_id)
        self.driver.find_element_by_id("UserPassword").send_keys(password, Keys.ENTER)

        for i in range(timeout):
            time.sleep(1)
            if(self.driver.current_url == self.HOME_URL):
                #print("Login Success.")
                break

        if(self.driver.current_url != self.HOME_URL):
            #print(self.driver.current_url)
            self.driver.close()
            # for ommit chrome <defunct>
            self.driver.quit()
            raise TimeoutError

    def get_data(self, year, month, record_num=10, progress=True):
        #check data_num under 10 or not
        if (record_num < self.MIN_RECORD_NUM):
            record_num = self.MIN_RECORD_NUM
        month = str(month).zfill(2)
        #print("Get Data of {}/{}.".format(year, month))

        # First load page for get height of a line
        self.driver.get("https://zaim.net/money?month={}{}".format(year, month))
        time.sleep(1)

        table = self.driver.find_element_by_xpath("//*[starts-with(@class, 'SearchResult-module__list___')]")
        lines = table.find_elements_by_xpath("//*[starts-with(@class, 'SearchResult-module__body___')]")

        line_height = int(lines[0].value_of_css_property('height').replace("px",""))

        # load page again for getting record
        self.driver.set_window_size(self.WINDOW_WIDTH, self.MIN_WINDOW_HEIGHT + line_height*(record_num - self.MIN_RECORD_NUM ))
        self.driver.get("https://zaim.net/money?month={}{}".format(year, month))
        time.sleep(1)

        table = self.driver.find_element_by_xpath("//*[starts-with(@class, 'SearchResult-module__list___')]")
        lines = table.find_elements_by_xpath("//*[starts-with(@class, 'SearchResult-module__body___')]")

        #print("Found {} data.".format(len(lines)))
        if progress:
            pbar = tqdm(total=len(lines))

        data = []
        for line in reversed(lines):
            items = line.find_elements_by_tag_name("div")

            item = {}
            item["id"] = (
                items[0]
                .find_element_by_tag_name("i")
                .get_attribute("data-url")
                .split("/")[2]
            )
            item["count"] = (
                items[1]
                .find_element_by_tag_name("i")
                .get_attribute("title")
                .split("（")[0]
            )
            date = items[2].text.split("（")[0]
            item["date"] = datetime.datetime.strptime(
                "{}年{}".format(year, date), "%Y年%m月%d日"
            )
            item["category"] = (
                items[3].find_element_by_tag_name("span").get_attribute("data-title")
            )
            item["genre"] = items[3].find_elements_by_tag_name("span")[1].text
            item["amount"] = int(items[4].find_element_by_tag_name("span").text.strip("¥").replace(",", ""))
            m_from = items[5].find_elements_by_tag_name("img")
            if len(m_from) != 0:
                item["from_account"] = m_from[0].get_attribute("data-title")
            m_to = items[6].find_elements_by_tag_name("img")
            if len(m_to) != 0:
                item["to_account"] = m_to[0].get_attribute("data-title")
            item["type"] = (
                "transfer" if "from_account" in item and "to_account" in item else "payment" if "from_account" in item else "income" if "to_account" in item else None
            )
            item["place"] = (
                items[7].find_element_by_tag_name("span").text
            )
            item["name"] = (
                items[8].find_element_by_tag_name("span").get_attribute("title")
            )
            item["comment"] = (
                items[9].find_element_by_tag_name("span").get_attribute("title")
            )
            data.append(item)
            if progress:
                pbar.update(1)
        if progress:
            pbar.close()
        return data
    
    def get_oauth_verifier(self,authorization_url):
        self.driver.get(authorization_url)
        time.sleep(3)
        #print(self.driver.page_source)
        agree_button = self.driver.find_element_by_name("agree")
        agree_button.send_keys(Keys.ENTER)
        time.sleep(3)
        #print(self.driver.page_source)
        callback = self.driver.find_element_by_class_name("callback").get_attribute("textContent")
        #print(callback)
        parameter = urllib.parse.parse_qs(callback)
        return parameter.get("oauth_verifier")[0]


    def close(self):
        self.driver.close()
        # for omit chrome <defunct>
        self.driver.quit()