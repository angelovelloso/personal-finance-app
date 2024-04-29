import csv
from io import BytesIO
from models import NewFinancialEntryCreate
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal

class C6CreditCSVImporter:

    def __init__(self, uploaded_file, file_details : dict, account_name : str):
        
        self.source_file = uploaded_file
        self.file_content = BytesIO(self.source_file)
        
        csv_reader = csv.reader(self.file_content.read().decode('utf-8').splitlines())
        _ = next(csv_reader) #Skip column names

        self.parsed_data = list()
        
        for row in csv_reader:

            splited = row[0].split(';')

            entry_date = datetime.strptime(splited[0], "%d/%m/%Y").date()

            if splited[5] != 'Única':
                report_date = entry_date + relativedelta(months=int(splited[5].split('/')[0]))
            else:
                report_date = entry_date

            entry = NewFinancialEntryCreate(
                source=f'c6_csv_credit_importer: {file_details['filename']}',
                entry_date=entry_date,
                report_date=report_date,
                description=f'{splited[4]} - Parcela {splited[5]}',
                value=Decimal(splited[8]),
                account=account_name
            )

            self.parsed_data.append(entry)