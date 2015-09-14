import time
import random

import sqlalchemy
from sqlalchemy import MetaData

import settings
from sfdctool import SFDCTool


class DBAdapter(object):

    def __init__(self):
        self.schema = settings.HCH_DB_SCHEMA
        self.dbengine = sqlalchemy.create_engine(settings.DATABASE_URL, echo=settings.DEBUG)
        self.dbconn = self.dbengine.connect()
        self.dbmeta = MetaData(bind=self.dbconn, schema=self.schema)

    def fqn(self, name):
        return '{}.{}'.format(self.schema, name)

    def table(self, table_name):
        self.dbmeta.reflect(only=[table_name])
        return self.dbmeta.tables[self.fqn(table_name)]

    def insert(self, table_name, **values):
        table = self.table(table_name)
        insert = table.insert().values(**values)
        self.dbconn.execute(insert)

    def update(self, table_name, where=None, **values):
        table = self.table(table_name)
        update = table.update().where(where).values(**values)
        self.dbconn.execute(update)

    def delete(self, table_name, where=None):
        table = self.table(table_name)
        delete = table.delete().where(where)
        self.dbconn.execute(delete)

    def random_row(self, table_name):
        table = self.table(table_name)
        select = table.select().where('id >= random() * (SELECT MAX(id) FROM {})'.format(table.key)).limit(1)
        return self.dbconn.execute(select).fetchone()


def main():
    dba = DBAdapter()

    while True:
        table = random.choice(SFDCTool.FIELDS.keys())
        op = random.random()
        # 10/20/70 delete/create/update
        if op < 0.1:  # delete
            row = dba.random_row(table)
            dba.delete(table, where='id={}'.format(row.id))
        elif op < 0.3:  # create
            fields = SFDCTool.FIELDS[table]
            values = SFDCTool.random_values(fields)
            dba.insert(table, **values)
        else:  # update
            fields = random.sample(SFDCTool.FIELDS[table], 4)
            values = SFDCTool.random_values(fields)
            row = dba.random_row(table)
            dba.update(table, where='id={}'.format(row.id), **values)
        time.sleep(1.0 / settings.HCH_RATE_LIMIT)


if __name__ == '__main__':
    main()
