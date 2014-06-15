from time import gmtime, strftime
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, orm

engine = create_engine('mysql://scraper@localhost/first-ever_grabber_data')

meta = MetaData()

table_name = strftime('%d_%m_%Y_%H_%M_%S', gmtime())

# Store Number, Product, Description, Price, Saving, Valid From, Valid To, Image Path
data_table = Table(table_name, meta,
                   Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('site_name', String(254)),
                   Column('title', String(254)),
                   Column('cost', String(254))
                   )

meta.create_all(engine)


class Data(object):
    def __init__(self, site_name, title, cost):
        self.site_name = site_name
        self.title = title
        self.cost = cost


from sqlalchemy.orm import mapper
mapper(Data, data_table)


from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)


session = Session()
