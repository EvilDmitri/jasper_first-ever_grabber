# coding=utf-8

from time import gmtime, strftime, strptime, mktime
from datetime import datetime
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, orm

engine = create_engine('mysql://scraper@localhost/first_ever_grabber_data')

meta = MetaData()

now_is = datetime.datetime.now()


def is_old(table):
    old_date = datetime.strptime(table, '%d_%m_%Y_%H_%M_%S')
    print now_is - old_date
    if (now_is - old_date).days > 30:
        return True
    else:
        return False


def main():
    meta.reflect(engine)
    for table in meta.sorted_tables:

        if is_old(table):
            engine.execute(table.delete)
            print '%s  -- deleted' % table


if __name__ == '__main__':
    main()
