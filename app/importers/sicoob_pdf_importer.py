import tabula
from pdfquery import PDFQuery
import pandas as pd

import sys, os, re
from decimal import Decimal
from datetime import datetime

sys.path.append(os.getcwd())

from app.models import FinancialEntry, Account
from app.database import get_session
import csv
from sqlmodel import select


pdf_path = '/home/angelo/my_git/financeiro-pessoal/data/input/fatura_sicoob_fev.pdf'

def extract_page_sicoob(file, page_num, vertical_top, vertical_bottom):

    print(f'Extraindo página {page_num}.')

    df_left = tabula.read_pdf(
        file,
        encoding='cp1252',
        area=[vertical_top, 0, vertical_bottom, 50],
        relative_area=True,
        columns=[66, 220], 
        lattice=True, 
        pages=page_num,
        pandas_options={
            'names': ['date', 'description', 'value']
        },
        output_format='dataframe')
    
    df_right = tabula.read_pdf(
        file,
        encoding='cp1252',
        area=[vertical_top, 50, vertical_bottom, 100],
        relative_area=True,
        columns=[340, 510], 
        lattice=True, 
        pages=page_num,
        pandas_options={
            'names': ['date', 'description', 'value']
        },
        output_format='dataframe')
    
    if len(df_right) > 0:
        return pd.concat([df_left[0], df_right[0]])
    else:
        return df_left[0]

pdf = PDFQuery(pdf_path)
pdf.load()

total_pages = pdf.doc.catalog['Pages'].resolve()['Count']
print(f'Número de páginas: {total_pages}')

extracted_dfs = list()

# Get pdf important info
start_page_vertical_start_label = pdf.pq('LTTextLineHorizontal:contains("LANÇAMENTOS - SICOOBCARD")')[0]
start_page = [ ancestor for ancestor in start_page_vertical_start_label[0].iterancestors('LTPage') ][0]
start_page_vertical_start = 100*(1 - ((float(start_page_vertical_start_label.get('y0')) - 2) / float(start_page.get('y1'))))

start_page_vertical_end_label = pdf.pq(f'LTTextLineHorizontal:contains("Página {start_page.get("pageid")}")')[0]
start_page_vertical_end = 100*(1 - ((float(start_page_vertical_end_label.get('y1')) + 2) / float(start_page.get('y1'))))

end_page_vertical_end_label = pdf.pq('LTTextLineHorizontal:contains("TOTAL DE")')[0]
end_page = [ ancestor for ancestor in end_page_vertical_end_label[0].iterancestors('LTPage') ][0]
end_page_vertical_end = 100*(1 - ((float(end_page_vertical_end_label.get('y1')) + 2) / float(end_page.get('y1'))))
end_page_vertical_start = 5


months = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN',
    'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']

vencimento_label = pdf.pq('LTTextLineHorizontal:contains("VENCIMENTO")').text().replace('VENCIMENTO ', '')
vencimento_date = datetime(
    int(re.findall(r'[0-9]{4}', vencimento_label)[0]),
    (months.index(re.findall(r'[a-zA-Z]{3}', vencimento_label)[0]) + 1),
    int(re.findall(r'[0-9]{2}', vencimento_label)[0])
)

pdf.file.close()

# Extract first page
extracted_dfs.append(
    extract_page_sicoob(
        pdf_path,
        start_page.get('pageid'), 
        start_page_vertical_start, 
        start_page_vertical_end
))

# Intermediate pages?

# Extract last page
extracted_dfs.append(
    extract_page_sicoob(
        pdf_path,
        end_page.get('pageid'), 
        end_page_vertical_start, 
        end_page_vertical_end
))

all_entries = pd.concat(extracted_dfs)

all_entries_clean = all_entries[~all_entries['date'].isna()]

# Start o save in database
session = next(get_session())
statement = select(Account).where(Account.account == 'Cartao.SICOOB')
results = session.exec(statement)
account = results.one()

print(account)

for index, row in all_entries_clean.iterrows():

    entry_value = Decimal(row['value'].replace('.', '').replace(',', '.').replace('R$ ', ''))
    entry_month = int(months.index(re.findall(r'[a-zA-Z]{3}', row['date'])[0]) + 1)
    entry_day = int(re.findall(r'[0-9]{2}', row['date'])[0])

    if entry_month > vencimento_date.month:
        entry_year = int(vencimento_date.year-1)
    else:
        entry_year = int(vencimento_date.year)

    print(f"era {row['value']}, ficou {entry_value}")

    entry = FinancialEntry(
        source='sicoob_pdf_importer',
        entry_date=datetime(entry_year, entry_month, entry_day).date(),
        report_date=datetime(entry_year, entry_month, entry_day).date(),
        description=row['description'],
        value=entry_value,
        account_id=account.id
    )

    print(entry)
    session.add(entry)
    session.commit()