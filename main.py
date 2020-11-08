#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import argparse
import sys
import datetime
from dateutil.relativedelta import relativedelta

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

def crawl_data_from(frym,toym=datetime.date.today()):
    crawler = ZaimCrawler(20)
    data = []
    m = frym;
    try:
        while((toym -m ).days > 0):
            data.extend(crawler.get_data(m.year,m.month, False))
            m = m + relativedelta(months=1)
        if (toym.month == m.month):
            data.extend(crawler.get_data(m.year,m.month, False))
    except NoSuchElementException as e:
        pass
    finally:
        crawler.close()
    return data


def init_parser():
    str_today = datetime.date.today().strftime('%Y%m')
    # parse argument
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')
    api_parser = subparsers.add_parser('api', help='api help')
    api_group = api_parser.add_mutually_exclusive_group()
    
    api_group.add_argument("-o","--oauth", help="""
        get acccess token/access token secret/oauth verifier.
        please set ENV value CONSUMER_ID/CONSUMER_SECRET/USER_ID/USER_PASSWORD
        """,action="store_true")

    api_group.add_argument("-g","--get", help="""
        get zaim data by api.
        please set ENV value CONSUMER_ID/CONSUMER_SECRET/ACCESS_TOKEN/ACCESS_TOKEN_SECRET/OAUTH_VERIFIER
        """,action="store_true")
    api_parser.set_defaults(func=api_func)

    crawler_parser = subparsers.add_parser('crawler', help='crawler help')
    crawler_group = crawler_parser.add_mutually_exclusive_group()
    crawler_group.add_argument("c",nargs='?', type=str,default=str_today,metavar=('yyyymm'),help="""
        get zaim data by crawler.
        please set ENV value USER_ID/USER_PASSWORD
    """)
    crawler_group.add_argument("-f","--fr",type=str,metavar=('yyyymm'),help="""
       get zaim data by crawler from yyyymm to this month
       please set ENV value USER_ID/USER_PASSWORD
    """)
    crawler_parser.set_defaults(func=crawler_func)
    return parser
 
def api_func(args):
    if args.oauth:
        # Oauth Mode
        oinit = OauthInitializer()
        oinit.authentication()
        sys.exit()
    elif(args.get):
        # API Mode
        api = ZaimAPI()
        json = api.get_data()
        print("{'values':" + str(json) + "}")

def crawler_func(args):

    if(args.fr is not None and len(args.fr) >= 1):
        try:
            frym = datetime.datetime.strptime(args.fr,'%Y%m').date()
            json = crawl_data_from(frym)
            pass
        except ValueError as e:
            print("Error: " + args.fr + " is not yyyymm format")

    elif(args.c is not None and len(args.c) >= 0):
        # Crawler Mode
        try:
            ym = datetime.datetime.strptime(args.c,'%Y%m')
            json = crawl_data(ym)
            pass
        except ValueError as e:
            print("Error: " + args.c + " is not yyyymm format")
            sys.exit()        
    print("{'values':" + str(json) + "}")



if __name__ == "__main__":
   
    parser = init_parser()
    args = parser.parse_args()
    args.func(args)
    


    