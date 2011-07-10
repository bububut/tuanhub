import urllib2
from config import *
from model import *

def update():
    setup_all()
    for site in CFG_site_list:
        print site[0]
        f = urllib2.urlopen(site[1])
        page = f.read()
        exec('from parsers.%s import *' % site[2])
        parse(page)
        session.commit()

if __name__ == '__main__':
    update()
