#!/usr/bin/env python

import random

from apicli import ClientCmdWrapper, run
import salesforce
from data import FAKER


class SFDCTool(object):
    FIELDS = {
        'contact': ('firstname', 'lastname', 'email', 'mailingstreet', 'mailingcity', 'mailingpostalcode'),
        'lead': ('firstname', 'lastname', 'email', 'phone', 'description', 'company'),
    }

    def __init__(self, client):
        self.client = client

    def create_many(self, object_name, count, *fields):
        results = []
        if not fields:
            fields = self.FIELDS.get(object_name.lower(), [])

        for n in range(int(count)):
            attrs = self.random_values(fields)
            results.append(self.client.create(object_name, **attrs))

        return results

    def query_sfids(self, object_type):
        results = self.client.queryAll(object_type, fields=['Id'], where='IsDeleted = False')
        return [r.Id for r in results.records]

        qOpts = self.client.client.generateHeader('QueryOptions')
        qOpts.batchSize = 2000
        self.client.setQueryOptions(qOpts)

        where = 'IsDeleted = False'

        results = self.client.queryAll(select)
        if results.size == 0:
            return []

        ids = [r.Id for r in results.records]
        while not results.done:
            results = self.client.queryAll(results.queryLocator)
            ids += [r.Id for r in results.records]

        return ids

    @staticmethod
    def random_values(fields):
        return {a: getattr(FAKER, a)() for a in fields}

    def random_workout(self, iterations=None):
        sfids = {
            'account': self.query_sfids('Account'),
            'contact': self.query_sfids('Contact'),
            'lead': self.query_sfids('Lead'),
        }

        while iterations is None or iterations > 0:
            object_type = random.choice(sfids.keys())
            rand = random.random()
            if rand < 0.1:
                sfid = random.choice(sfids[object_type])
                print 'delete', object_type, sfid
                self.client.delete(sfid)
                sfids[object_type].remove(sfid)
            elif rand < 0.8:
                sfid = random.choice(sfids[object_type])
                fields = random.sample(self.FIELDS[object_type], 3)
                print 'update', object_type, sfid, fields
                self.client.update(object_type, sfid, **self.random_values(fields))
            else:
                print 'create', object_type
                result = self.create_many(object_type, 1)
                sfids[object_type].append(result[0].id)


def main():
    client = salesforce.create_client()
    client.login()

    tool = SFDCTool(client)
    cli = ClientCmdWrapper(tool)
    run(cli)


if __name__ == '__main__':
    main()
