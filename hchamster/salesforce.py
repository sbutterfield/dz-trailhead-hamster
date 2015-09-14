import os
import logging

from sforce.partner import SforcePartnerClient

import settings

from apicli import ClientCmdWrapper, run


logging.getLogger('suds').setLevel(logging.INFO)


SFPARTNER_WSDL = os.path.join(os.path.dirname(__file__), 'partnerwsdl.xml')
# XXX Slow?
SFPARTNER_CLIENT = SforcePartnerClient(SFPARTNER_WSDL)


class SalesforceSOAPClient(object):
    def __init__(self, username, password, token):
        self.username = username
        self.password = password
        self.token = token
        self.client = SFPARTNER_CLIENT

    def login(self):
        """ login to SFDC """
        self.client.login(self.username, self.password, self.token)

    def queryAll(self, object_name, fields=None, where=''):
        """ Query for object_name in SFDC """
        if fields is None:
            fields = []

        fields = ', '.join(fields)
        if where:
            where = 'WHERE {}'.format(where)

        result = self.client.query('SELECT {} FROM {} {}'.format(fields, object_name, where))
        return result

    def query(self, object_name, fields=None, where=''):
        """ Query for object_name in SFDC """
        if fields is None:
            fields = []

        fields = ', '.join(fields)
        if where:
            where = 'WHERE {}'.format(where)

        result = self.client.query('SELECT {} FROM {} {}'.format(fields, object_name, where))
        return result

    def create(self, object_name, **kwargs):
        record = self.client.generateObject(object_name)
        for field, value in kwargs.iteritems():
            setattr(record, field, value)

        result = self.client.create(record)
        return result

    def update(self, object_name, sfid, **kwargs):
        record = self.client.generateObject(object_name)
        record.Id = sfid
        for field, value in kwargs.iteritems():
            setattr(record, field, value)

        result = self.client.update(record)
        return result

    def delete(self, *sfids):
        return self.client.delete(sfids)


def create_client():
    return SalesforceSOAPClient(settings.SFDC_USERNAME, settings.SFDC_PASSWORD, settings.SFDC_TOKEN)


def main():
    client = create_client()
    client.login()

    cli = ClientCmdWrapper(client)
    run(cli)


if __name__ == '__main__':
    main()
