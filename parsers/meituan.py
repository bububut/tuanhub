from BeautifulSoup import BeautifulStoneSoup
from datetime import datetime
from model import *

def parse(page):
    soup = BeautifulStoneSoup(page)
    for deal in soup.findAll('deal'):
        if deal.value.string==u'-':
            continue
        Deal(url=deal.deal_url.string, title=deal.title.string, price=float(deal.price.string),
             orig_price=float(deal.value.string), image=deal.medium_image_url.string,
             start_time=datetime.strptime(deal.find('start_date').string[0:-6], '%Y-%m-%dT%H:%M:%S'),
             end_time=datetime.strptime(deal.find('end_date').string[0:-6], '%Y-%m-%dT%H:%M:%S'),
             bought=int(deal.find('quantity_sold').string)
             )

