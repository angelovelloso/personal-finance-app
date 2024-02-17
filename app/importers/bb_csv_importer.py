import sys, os
from decimal import Decimal
from datetime import datetime

sys.path.append(os.getcwd())

from app.models import FinancialEntry, Account
from app.database import get_session
import csv
from sqlmodel import select

input_file = 'data/input/extrato_fev_2024.csv'

session = next(get_session())
statement = select(Account).where(Account.account == 'Conta.BB')
results = session.exec(statement)
account = results.one()

print(account)
print(type(account))

with open(input_file, newline='', encoding='cp1252') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')

    columns = next(spamreader)
    
    for row in spamreader:
        entry = FinancialEntry(
            source='Extrato BB',
            entry_date=datetime.strptime(row[0], "%d/%m/%Y").date(),
            report_date=datetime.strptime(row[0], "%d/%m/%Y").date(),
            description=row[2],
            value=Decimal(row[5]),
            account_id=account.id
        )

        print(entry)
        session.add(entry)
        session.commit()