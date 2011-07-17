# coding: utf-8

from BeautifulSoup import BeautifulStoneSoup
import urllib2
from datetime import datetime
import re
import json
import logging
from model import *
from config import *

city_url = 'http://open.client.lashou.com/api/cities'
list_url = 'http://open.client.lashou.com/api/detail/city/'

def parse():
    logging.debug('Processing ' + city_url)
    for i in range(CFG_retry):
        try:
            p = urllib2.urlopen(city_url).read()
        except:
            continue
    if not p:
        logging.error('Fail to open ' + city_url)
        return
    soup = BeautifulStoneSoup(p)
    # for city_id in soup.findAll('id'):
    for city_id in ['2419', '2421']:
        # if city_id.string == u'9999':
        #     continue
        #parse_deal(list_url + city_id.string)
        parse_deal(list_url + city_id)

def parse_deal(list_url):
    # pre processing
    logging.debug('Processing ' + list_url)
    for i in range(CFG_retry):
        try:
            p = urllib2.urlopen(list_url).read()
        except:
            continue
    if not p:
        logging.error('Fail to open ' + list_url)
        return
    soup = BeautifulStoneSoup(p)
    # start parssing
    for deal in soup.findAll('url'):
        deal_url = deal.loc.string
        shops = deal.findAll('shop');
        # 无地理信息跳过
        if len(shops) == 0:
            logging.debug('- ' + deal_url)
            continue
        # 已爬取的跳过
        if Deal.get_by(url=deal_url):
            logging.debug('- ' + deal_url)
            continue
        # Create Deal
        logging.debug('+ ' + deal_url)
        deal = deal.data.display
        dd = Deal(url = deal_url,
                  title = deal.title.string,
                  price = float(deal.price.string),
                  orig_price = float(deal.value.string),
                  image = deal.image.string,
                  start_time = datetime.fromtimestamp(int(deal.starttime.string)),
                  end_time = datetime.fromtimestamp(int(deal.endtime.string)),
                  bought = int(deal.bought.string),
                  type = 0,
                  site = u'拉手网',
                  )

        # 爬取经度维度
        for shop in shops:
            ss = Shop(name = shop.find('name').string,
                      tel = shop.tel.string,
                      address = shop.addr.string,
                      latitude = float(shop.latitude.string),
                      longitude = float(shop.longitude.string),
                      )
            ss.deal = dd


