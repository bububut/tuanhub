# coding: utf-8

from BeautifulSoup import BeautifulStoneSoup
import urllib2
from datetime import datetime
import re
import json
import logging
from model import *
from config import *

city_url = 'http://www.meituan.com/api/v1/divisions'
list_url = 'http://www.meituan.com/api/v1/%s/deals'

def parse():
    logging.debug('Processing ' + city_url)
    for i in range(CFG_retry):
        try:
            p = urllib2.urlopen(city_url).read()
        except:
            continue
    if p:
        soup = BeautifulStoneSoup(p)
        #for city_id in soup.findAll('id'):
        #    parse_deal(list_url % city_id.string)
        for city_id in ['beijing', 'shanghai']:
            parse_deal(list_url % city_id)
    else:
        logging.error('Fail to open ' + city_url)

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
    # start processing
    for deal in soup.findAll('deal'):
        deal_url = deal.deal_url.string
        # 抽奖活动跳过
        if deal.value.string==u'-':
            logging.debug('- ' + deal_url)
            continue
        # 无地理信息跳过
        if deal.deal_url.string[7:10]==u'www':
            logging.debug('- ' + deal_url)
            continue
        # 已爬取的跳过
        if Deal.get_by(url=deal_url):
            logging.debug('- ' + deal_url)
            continue
        # Create Deal
        logging.debug('+ ' + deal_url)
        dd = Deal(url = deal.deal_url.string,
                  title = deal.title.string,
                  price = float(deal.price.string),
                  orig_price = float(deal.value.string),
                  image = deal.medium_image_url.string,
                  start_time = datetime.strptime(deal.find('start_date').string[0:-6], '%Y-%m-%dT%H:%M:%S'),
                  end_time = datetime.strptime(deal.find('end_date').string[0:-6], '%Y-%m-%dT%H:%M:%S'),
                  bought = int(deal.find('quantity_sold').string),
                  type = 0,
                  #city = 'shanghai',
                  site = u'美团网',
                  )

        # 爬取经度维度
        p = urllib2.urlopen(deal_url).read()
        m = re.search(r"Biz.map\('map-canvas', ([\S ]+)\);",p)
        #if not m:
         #   continue
        jj = json.loads(m.group(1))
        for marker in jj['markers']:
            ss = Shop(latitude = marker['position'][0],
                      longitude = marker['position'][1],
                      )
            ss.deal = dd


