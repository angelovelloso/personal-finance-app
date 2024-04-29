import sys, os

sys.path.append(os.getcwd())

from app.settings import Settings
from sling import Sling

tables = [
    'account',
    'category',
    'financialentry'
    ]

for table in tables:
    config = {
                'source': {
                    'conn': Settings().DB_URL_COMPLETE,
                    'stream': f"select * from {table}"
                },
                'target': {
                    'object':  f'file://{os.getcwd()}/data/output/{table}.csv',
                },
                'mode': 'full-refresh'
            }

    Sling(**config).run()