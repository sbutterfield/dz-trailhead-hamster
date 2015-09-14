import os

DEBUG = True


DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost/hchamster')

HCH_DB_SCHEMA = os.environ.get('HCH_SCHEMA', 'hch')
HCH_RATE_LIMIT = float(os.environ.get('HCH_RATE_LIMIT', '10'))

SFDC_USERNAME = os.environ.get('SFDC_USERNAME')
SFDC_PASSWORD = os.environ.get('SFDC_PASSWORD')
SFDC_TOKEN = os.environ.get('SFDC_TOKEN')
