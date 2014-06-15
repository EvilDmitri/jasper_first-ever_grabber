from config import URLS

class Grabber():
    def get(self):
        success = 0
        for site_name in URLS:
            if 'discover.com' in site_name:
                task_name = 'XmlGrabber'
            elif 'shop.upromise.com' in site_name:
                task_name = 'ShopGrabber'

            elif site_name in ['shop.amtrakguestrewards.com', 'shop.lifemiles.com']:
                task_name = 'RetailersGrabber'
            # elif 'www.bestbuy.com' in site_name:
            #     grabber = BestbuyGrabber(site_name)
            else:
                task_name = 'UltimateRewardsGrabber'

            # if grabber.grab():
            #     success += 1

        # Now it's time to check if data is changed since last scrape and if so post an email

        return 'OK'




 # -*- coding: utf-8 -*-

from models import Data, session, table_name

import json
import logging
import os
import feedparser
from datetime import datetime

from grab.spider import Spider, Task
from grab.tools import html

from grab.tools.logs import default_logging
from hashlib import sha1

default_logging(level=logging.DEBUG)

path = os.path.dirname(os.path.abspath(__file__))
URLS_FILE = os.path.join(path, 'urls.txt')


RSS_LINK = 'http://pathmark.inserts2online.com/rss.jsp?drpStoreID={0}'

IMAGE_DIR = os.path.join(path, 'images/')

THREADS = 2


class FirstSpider(Spider):
    def __init__(self):
        super(FirstSpider, self).__init__(thread_number=THREADS, network_try_limit=20)

    def task_generator(self):
        with open(URLS_FILE) as json_data:
            data = json.load(json_data)
            sites = data['sites']
            for site in sites:

                if 'discover.com' in site['link']:
                    task_name = 'xml'
                elif 'shop.upromise.com' in site['link']:
                    task_name = 'shop'

                elif site['link'] in ['shop.amtrakguestrewards.com', 'shop.lifemiles.com']:
                    task_name = 'retailers'
                # elif 'www.bestbuy.com' in site_name:
                #     grabber = BestbuyGrabber(site_name)
                else:
                    task_name = 'ultimate'

                yield Task(task_name, url=site['link'], site_name=site['name'])

    def task_xml(self, grab, task):
        lines = grab.xpath_list('//pd')
        for line in lines:
            title = line.attrib['p']
            cost = ''.join([str(float(line.attrib['cbb']) * 100) + '% Cashback'])

            data = Data(site_name=task.site_name, title=title, cost=cost)
            session.add(data)
        session.commit()

    def task_shop(self, grab, task):
        lines = grab.xpath_list('//div[@id="allStores"]/ul/li/a')
        for line in lines:
            title = line.text_content()
            cost = line.tail.strip()
            data = Data(site_name=task.site_name, title=title, cost=cost)
            session.add(data)
        session.commit()

    def task_retailers(self, grab, task):
        lines = grab.xpath_list('//div[@class="merch-full"]/a')
        for line in lines:
            title = line[1].text_content()
            cost = line[2].text_content().strip()
            data = Data(site_name=task.site_name, title=title, cost=cost)
            session.add(data)
        session.commit()


def main():
    bot = FirstSpider()

    # bot.setup_proxylist(proxy_file='proxy.lst')
    bot.setup_grab(hammer_mode=True)

    try:
        bot.run()
    except KeyboardInterrupt:
        pass

    print bot.render_stats()
    print 'All done'


if __name__ == '__main__':
    print 'Start working'
    default_logging(level=logging.DEBUG)
    main()