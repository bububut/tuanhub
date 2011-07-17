import urllib2
import logging
from config import *
from model import *

def update():
    logging.basicConfig(#filename='tuanhub.log',
                        format='%(levelname)s %(asctime)s %(message)s',
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        )
    setup_all()
    for site in CFG_site_list:
        logging.info(site[0])
        exec('from parsers.%s import *' % site[1])
        parse()
        session.commit()

if __name__ == '__main__':
    update()
