from app.models import Account
from sqlmodel import select

def test_create_account(session):
    new_account = Account(
        account='BancoBrasil-CC',
        description='Conta Corrente no Banco do Brasil - pix: CPF'
    )
    session.add(new_account)
    session.commit()

    account = session.scalar(select(Account).where(Account.account == 'BancoBrasil-CC'))

    assert account.account == 'BancoBrasil-CC'