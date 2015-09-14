
from faker import Factory
from faker.providers import BaseProvider


FAKER = Factory.create()


class SalesforceProvider(BaseProvider):
    """ faker provider for common SFDC fields
    """
    def phone(self):
        return FAKER.phone_number()

    def fax(self):
        return FAKER.phone_number()

    def website(self):
        return FAKER.url()

    def firstname(self):
        return FAKER.first_name()

    def lastname(self):
        return FAKER.last_name()

    def mailingstreet(self):
        return FAKER.street_address()

    def mailingcity(self):
        return FAKER.city()

    def mailingpostalcode(self):
        return FAKER.postcode()

    def description(self):
        return FAKER.sentence()

    def name(self):
        return FAKER.company()

FAKER.add_provider(SalesforceProvider)
