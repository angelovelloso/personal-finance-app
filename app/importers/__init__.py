from importers.bb_csv_checking_importer import BBCheckingCSVImporter
from importers.c6_csv_credit_importer import C6CreditCSVImporter


importers = [
    {
        'name': 'Banco do Brasil - Extrato de Conta Corrente - CSV',
        'id': 'bb_csv_checking',
        'class': BBCheckingCSVImporter,
        'account': 'Conta.BB'
    },    
    {
        'name': 'Sicoob - Fatura de Cartão de Crédito - PDF'
    },    
    {
        'name': 'Inter - Fatura de Cartão de Crédito - PDF'
    },    
    {
        'name': 'C6 - Fatura de Cartão de Crédito - CSV',
        'id': 'c6_csv_credit',
        'class': C6CreditCSVImporter,
        'account': 'Cartao.C6'
    }
]

importers_list = [importers[x]['name'] for x in range(len(importers))]
