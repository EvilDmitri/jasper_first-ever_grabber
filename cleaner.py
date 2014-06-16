# coding=utf-8

from time import gmtime, strftime
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, orm

engine = create_engine('mysql://scraper@localhost/first_ever_grabber_data')

meta = MetaData()


def is_old(table):
    print table
    print dir(table)
    return False


def main():
    meta.reflect(engine)
    for table in meta.sorted_tables:

        if is_old(table):
            engine.execute(table.delete)
            print '%s  -- deleted' % table


if __name__ == '__main__':
    main()
