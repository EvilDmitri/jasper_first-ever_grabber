 # -*- coding: utf-8 -*-

from models import Data, session

import json
import logging
import os


from grab.spider import Spider, Task


from grab.tools.logs import default_logging

default_logging(level=logging.DEBUG)

path = os.path.dirname(os.path.abspath(__file__))
URLS_FILE = os.path.join(path, 'urls.txt')

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

    def task_ultimate(self, grab, task):
        lines = grab.xpath_list('//div[@class="mn_srchListSection"]/ul/li')
        for line in lines:
            title = line.getchildren()[0].text_content()
            cost = line.getchildren()[2].text_content().strip().replace(u'\xa0', ' ')
            data = Data(site_name=task.site_name, title=title, cost=cost)
            session.add(data)
        session.commit()


def main():
    bot = FirstSpider()

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