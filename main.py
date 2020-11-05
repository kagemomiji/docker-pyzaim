#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import argparse
import sys
import datetime
from selenium.common.exceptions import NoSuchElementException

from pyzaim import OauthInitializer, ZaimCrawler, ZaimAPI

def crawl_data(ym = datetime.date.today()):
    crawler = ZaimCrawler()
    try:
        data = crawler.get_data(ym.year, ym.month, False)
        return data
    except NoSuchElementException as e:
        print("Error: No Zaim Data in " + ym.strftime('%Y/%m'))
        sys.exit()
    finally:
        crawler.close()

def init_parser():
    str_today = datetime.date.today().strftime('%Y%m')
    # parse argument
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-o","--oauth", help="""
        get acccess token/access token secret/oauth verifier.
        please set ENV value CONSUMER_ID/CONSUMER_SECRET/USER_ID/USER_PASSWORD
        """,action="store_true")
    group.add_argument("-c","--crawler", nargs='?',const=str_today,type=str ,metavar=('yyyymm'),help="""
        get zaim data by crawler.
        please set ENV value USER_ID/USER_PASSWORD
    """)
    group.add_argument("-a","--api", help="""
        get zaim data by api.
        please set ENV value CONSUMER_ID/CONSUMER_SECRET/ACCESS_TOKEN/ACCESS_TOKEN_SECRET/OAUTH_VERIFIER
        """,action="store_true")
    return parser
 
if __name__ == "__main__":
   
    parser = init_parser()
    args = parser.parse_args()

    if args.oauth:
        # Oauth Mode
        oinit = OauthInitializer()
        oinit.authentication()
        sys.exit()
    elif(args.api):
        # API Mode
        api = ZaimAPI()
        json = api.get_data()
    elif(args.crawler is not None and len(args.crawler) >= 0):
        # Crawler Mode
        try:
            ym = datetime.datetime.strptime(args.crawler,'%Y%m')
            json = crawl_data(ym)
            pass
        except ValueError as e:
            print("Error: " + args.crawler + " is not yyyymm format")
            sys.exit()
    else:
        # if no option print usage and exit program
        parser.print_help()
        sys.exit() 
        
    print("{\"values\":" + str(json) + "}")


    


    